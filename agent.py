"""
agent.py (2-agent version, stabilized + timings)
- Planner Agent: outputs JSON that includes a natural-language planner_message + optional tool call
- Executor Agent: generates the final natural-language answer using plan + tool output + memory

Runs locally with Ollama. Stores memory locally in memory.json.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

from tools import TOOLS_REGISTRY, list_tools


# -----------------------------
# Ollama client (local LLM)
# -----------------------------
def ollama_chat(
    messages: List[Dict[str, str]],
    model: str = "llama3.2:1b",
    temperature: float = 0.2,
    base_url: str = "http://localhost:11434",
    timeout_s: int = 45,
    num_predict: int = 300,
) -> str:
    """
    Calls Ollama's local chat endpoint.
    - timeout_s prevents Streamlit from "hanging forever"
    - num_predict caps output length so each agent responds quickly
    """
    url = f"{base_url}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
        },
        "stream": False,
    }
    r = requests.post(url, json=payload, timeout=timeout_s)
    r.raise_for_status()
    return r.json()["message"]["content"]


# -----------------------------
# Local memory (JSON file)
# -----------------------------
DEFAULT_MEMORY = {"profile": {"name": None, "preferences": {}}, "notes": []}


def load_memory(path: str = "memory.json") -> Dict[str, Any]:
    if not os.path.exists(path):
        return json.loads(json.dumps(DEFAULT_MEMORY))
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory: Dict[str, Any], path: str = "memory.json") -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


# -----------------------------
# Prompts
# -----------------------------
PLANNER_SYSTEM = """You are the PLANNER agent for a local, offline assistant.
Goal: decide what to do next and whether to call ONE local tool.

Rules:
- Ask 1–2 clarifying questions ONLY if truly needed.
- If a tool helps, choose exactly one tool for this turn.
- If the user is asking for help deciding between options,
  you MUST use the "pros_cons" tool.
- Keep planner_message short and human-friendly.
- Output ONLY valid JSON with the schema below. No extra text.
- You are offline. Do not claim internet access.
"""

EXECUTOR_SYSTEM = """You are the EXECUTOR agent for a local, offline assistant.
Goal: produce the final helpful response to the user.

Rules:
- Use the plan, tool output (if any), and memory context.
- Keep the answer short, friendly, and practical.
- If planner included clarifying questions, ask them clearly (as questions).
- You are offline. Do not claim internet access.
"""

PLANNER_JSON_FORMAT = """Output ONLY JSON in this schema:

{
  "planner_message": "Short natural-language explanation of what you will do (2–5 sentences).",
  "plan": ["step 1", "step 2", "step 3"],
  "clarifying_questions": ["question 1", "question 2"],
  "tool": "<one of: {tool_names}> or null",
  "args": {"arg1":"value1", "arg2":"value2"}
}

Rules:
- plan should be short (3–6 steps).
- clarifying_questions must be 0–2 items.
- If no tool needed: tool=null and args={}.
- JSON only. No markdown. No extra text.
"""


# -----------------------------
# Planner JSON parsing (defensive)
# -----------------------------
def parse_planner_json(text: str) -> Dict[str, Any]:
    """
    Returns a normalized dict. If parsing fails, returns a safe fallback
    that still allows Executor to proceed.
    """
    try:
        obj = json.loads(text.strip())
        if not isinstance(obj, dict):
            raise ValueError("Planner output was not a JSON object.")
    except Exception:
        # Fallback: planner couldn't or didn't output JSON
        return {
            "planner_message": "I will respond directly without a tool.",
            "plan": [],
            "clarifying_questions": [],
            "tool": None,
            "args": {},
            "_raw": text,
        }

    # normalize keys + types
    obj.setdefault("planner_message", "")
    obj.setdefault("plan", [])
    obj.setdefault("clarifying_questions", [])
    obj.setdefault("tool", None)
    obj.setdefault("args", {})

    if not isinstance(obj["planner_message"], str):
        obj["planner_message"] = str(obj["planner_message"])

    if not isinstance(obj["plan"], list):
        obj["plan"] = []
    if not isinstance(obj["clarifying_questions"], list):
        obj["clarifying_questions"] = []
    if not isinstance(obj["args"], dict):
        obj["args"] = {}

    # enforce limits
    obj["clarifying_questions"] = obj["clarifying_questions"][:2]
    obj["plan"] = obj["plan"][:6]

    return obj


def execute_tool(tool: str, args: Dict[str, Any]) -> str:
    fn = TOOLS_REGISTRY[tool]
    try:
        return fn(**args)
    except TypeError:
        return "Tool call arguments didn't match. Try simpler inputs."
    except Exception:
        return "Tool failed unexpectedly. Try a different approach."


# -----------------------------
# Memory updates (robust)
# -----------------------------
def maybe_update_memory(user_text: str, memory: Dict[str, Any]) -> bool:
    updated = False
    raw = user_text.strip()
    lower = raw.lower()

    needle = "my name is "
    if needle in lower:
        idx = lower.find(needle) + len(needle)
        name = raw[idx:].strip()
        if name:
            memory.setdefault("profile", {}).setdefault("name", None)
            memory["profile"]["name"] = name
            updated = True

    needle2 = "remember that i "
    if needle2 in lower:
        idx = lower.find(needle2) + len(needle2)
        pref = raw[idx:].strip()
        if pref:
            memory.setdefault("profile", {}).setdefault("preferences", {})
            key = f"pref_{len(memory['profile']['preferences']) + 1}"
            memory["profile"]["preferences"][key] = pref
            updated = True

    return updated


# -----------------------------
# Agent 1: Planner
# -----------------------------
def planner_agent(
    user_text: str,
    memory: Dict[str, Any],
    model: str,
) -> Tuple[Dict[str, Any], str]:
    tool_names = ", ".join(list_tools())
    profile = memory.get("profile", {})
    prefs = profile.get("preferences", {})
    name = profile.get("name")

    context = {"name": name, "preferences": prefs, "available_tools": list_tools()}

    messages = [
        {"role": "system", "content": PLANNER_SYSTEM},
        {"role": "system", "content": f"Local user context: {json.dumps(context)}"},
        {"role": "system", "content": PLANNER_JSON_FORMAT.replace("{tool_names}", tool_names)},
        {"role": "user", "content": user_text},
    ]

    planner_raw = ollama_chat(messages, model=model, temperature=0.0, num_predict=220)
    plan_obj = parse_planner_json(planner_raw)

    # Validate tool strictly
    tool = plan_obj.get("tool", None)
    if tool is not None and tool not in TOOLS_REGISTRY:
        plan_obj["tool"] = None
        plan_obj["args"] = {}

    return plan_obj, planner_raw


# -----------------------------
# Agent 2: Executor
# -----------------------------
def executor_agent(
    user_text: str,
    memory: Dict[str, Any],
    planner_output: Dict[str, Any],
    tool_result: Optional[str],
    model: str,
    temperature: float,
) -> str:
    profile = memory.get("profile", {})
    prefs = profile.get("preferences", {})
    name = profile.get("name")

    payload = {
        "planner_message": planner_output.get("planner_message", ""),
        "plan": planner_output.get("plan", []),
        "clarifying_questions": planner_output.get("clarifying_questions", []),
        "tool_used": planner_output.get("tool", None),
        "tool_result": tool_result,
        "memory": {"name": name, "preferences": prefs},
    }

    messages = [
        {"role": "system", "content": EXECUTOR_SYSTEM},
        {"role": "system", "content": f"Planner + tool context: {json.dumps(payload)}"},
        {"role": "user", "content": user_text},
    ]

    return ollama_chat(messages, model=model, temperature=temperature, num_predict=350)


# -----------------------------
# Main public function
# -----------------------------
def agent_reply(
    user_text: str,
    memory_path: str = "memory.json",
    model: str = "llama3.2:1b",
    temperature: float = 0.2,
    max_tool_calls: int = 1,
) -> str:
    trace = agent_reply_with_full_trace(
        user_text=user_text,
        memory_path=memory_path,
        model=model,
        temperature=temperature,
        max_tool_calls=max_tool_calls,
    )
    return trace["executor_answer"]


def agent_reply_with_full_trace(
    user_text: str,
    memory_path: str = "memory.json",
    model: str = "llama3.2:1b",
    temperature: float = 0.2,
    max_tool_calls: int = 1,
) -> Dict[str, Any]:
    """
    Returns a full trace so Streamlit can show:
    - Planner raw output
    - Planner parsed JSON
    - Tool result
    - Executor final response
    - Timings (planner/tool/executor/total)
    """
    t_total_start = time.perf_counter()

    memory = load_memory(memory_path)

    if maybe_update_memory(user_text, memory):
        save_memory(memory, memory_path)

    # --- Planner timing ---
    t_planner_start = time.perf_counter()
    planner_output, planner_raw = planner_agent(user_text, memory, model=model)
    t_planner_end = time.perf_counter()

    # --- Tool timing ---
    tool_result = None
    tool = planner_output.get("tool", None)
    args = planner_output.get("args", {}) or {}

    t_tool_start = time.perf_counter()
    if tool and max_tool_calls > 0:
        tool_result = execute_tool(tool, args)
    t_tool_end = time.perf_counter()

    # --- Executor timing ---
    t_exec_start = time.perf_counter()
    executor_answer = executor_agent(
        user_text=user_text,
        memory=memory,
        planner_output=planner_output,
        tool_result=tool_result,
        model=model,
        temperature=temperature,
    )
    t_exec_end = time.perf_counter()

    # Save conversation
    memory.setdefault("notes", []).append({"user": user_text, "assistant": executor_answer})
    memory["notes"] = memory["notes"][-50:]
    save_memory(memory, memory_path)

    t_total_end = time.perf_counter()

    timings = {
        "planner_seconds": round(t_planner_end - t_planner_start, 3),
        "tool_seconds": round(t_tool_end - t_tool_start, 3),
        "executor_seconds": round(t_exec_end - t_exec_start, 3),
        "total_seconds": round(t_total_end - t_total_start, 3),
    }

    return {
        "executor_answer": executor_answer,
        "planner_output": planner_output,
        "planner_raw": planner_raw,
        "tool_result": tool_result,
        "timings": timings,
    }