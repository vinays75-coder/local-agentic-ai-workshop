"""
tools.py
A tiny set of safe, local "tools" the agent can call.

Non-technical workshop-friendly design:
- Each tool is a plain Python function.
- A registry maps tool_name -> function.
- All tools run locally (no cloud).
"""

from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, Callable, List


def tool_calculator(expression: str) -> str:
    """Evaluate a simple math expression safely."""
    allowed = set("0123456789+-*/(). % ")
    if any(ch not in allowed for ch in expression):
        return "Sorry — I can only calculate basic math with digits and + - * / ( ) . %"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "I couldn't evaluate that expression. Try something like: (1200/12) * 0.8"


def tool_checklist(topic: str, items: int = 10) -> str:
    """Produce a checklist template."""
    items = max(3, min(int(items), 25))
    lines = [f"Checklist: {topic}"]
    for i in range(1, items + 1):
        lines.append(f"- [ ] Item {i}")
    return "\n".join(lines)


def tool_pros_cons(decision: str) -> str:
    """A simple pros/cons worksheet template."""
    return (
        f"Decision: {decision}\n\n"
        "Pros:\n"
        "- \n- \n- \n\n"
        "Cons:\n"
        "- \n- \n- \n\n"
        "Notes / Next step:\n"
        "- "
    )


def tool_timeblock_plan(goal: str, hours: int = 3, start_time: str | None = None) -> str:
    """Create a simple time-block plan for the next N hours."""
    hours = max(1, min(int(hours), 8))
    now = _dt.datetime.now()
    if start_time:
        try:
            hh, mm = start_time.split(":")
            now = now.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
        except Exception:
            pass

    blocks = []
    for i in range(hours):
        start = now + _dt.timedelta(hours=i)
        end = start + _dt.timedelta(hours=1)
        blocks.append(f"{start.strftime('%I:%M %p')}–{end.strftime('%I:%M %p')}: {goal} (focus block {i+1})")
    return "\n".join(blocks)


TOOLS_REGISTRY: Dict[str, Callable[..., str]] = {
    "calculator": tool_calculator,
    "checklist": tool_checklist,
    "pros_cons": tool_pros_cons,
    "timeblock_plan": tool_timeblock_plan,
}


def list_tools() -> List[str]:
    return sorted(TOOLS_REGISTRY.keys())
