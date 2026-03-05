"""
app.py
Run with:
    streamlit run app.py

Shows (Debug Mode):
- Planner Agent (Natural Language)
- Planner Agent (Structured JSON) [optional]
- Tool Output
- Executor Agent (Natural Language)
- Timings panel (at the end)
- Appends disclaimer to all outputs
"""

import streamlit as st
from agent import agent_reply, agent_reply_with_full_trace

DISCLAIMER = "\n\n---\n**AI Generated Content please check it**"

st.set_page_config(page_title="Local Agentic AI Chat", page_icon="🤖", layout="centered")

st.title("🤖 Local Agentic AI Chat (Offline)")
st.caption("Runs fully on your laptop using a local Ollama model. No cloud, no API keys.")

# ===============================
# Sidebar Settings
# ===============================
with st.sidebar:
    st.header("Settings")

    model = st.text_input("Ollama model", value="llama3.2:1b")
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)

    debug_mode = st.checkbox("Show Agent Trace (Planner + Tool + Executor)", value=True)
    show_structured_json = st.checkbox("Show Planner structured JSON", value=True)
    show_planner_raw = st.checkbox("Show Planner raw output (advanced)", value=False)

    st.divider()
    st.markdown("### Local Memory")
    st.markdown("Preferences are stored in `memory.json` on your machine.")

# ===============================
# Chat Session State
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I’m your Local Life Concierge. What are we planning today?"}
    ]

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ===============================
# Chat Input
# ===============================
user_text = st.chat_input("Type your message…")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking locally…"):
            try:
                if debug_mode:
                    trace = agent_reply_with_full_trace(
                        user_text=user_text,
                        model=model,
                        temperature=float(temperature),
                    )

                    planner_output = trace.get("planner_output", {}) or {}
                    planner_message = (planner_output.get("planner_message", "") or "").strip()
                    tool_result = trace.get("tool_result", None)
                    executor_answer = trace.get("executor_answer", "")
                    timings = trace.get("timings", {}) or {}

                    # ---------------------------
                    # Planner (Natural Language)
                    # ---------------------------
                    st.markdown("## 🧠 Planner Agent (Natural Language)")
                    st.write(planner_message if planner_message else "(No planner_message returned)")

                    # Optional Structured JSON
                    if show_structured_json:
                        st.markdown("### Planner Agent (Structured JSON)")
                        st.json(planner_output)

                    # Optional Raw JSON
                    if show_planner_raw:
                        st.markdown("### Planner Agent (Raw Output)")
                        st.code(trace.get("planner_raw", ""), language="json")

                    # ---------------------------
                    # Tool Output
                    # ---------------------------
                    st.markdown("---")
                    st.markdown("## 🛠 Tool Output")
                    st.write(tool_result if tool_result else "(No tool used)")

                    # ---------------------------
                    # Executor Output
                    # ---------------------------
                    final_output = executor_answer + DISCLAIMER

                    st.markdown("---")
                    st.markdown("## ✅ Executor Agent (Natural Language)")
                    st.write(final_output)

                    # ---------------------------
                    # Timings (LAST)
                    # ---------------------------
                    st.markdown("---")
                    st.markdown("## ⏱ Timings")

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Planner (s)", timings.get("planner_seconds", "—"))
                    c2.metric("Tool (s)", timings.get("tool_seconds", "—"))
                    c3.metric("Executor (s)", timings.get("executor_seconds", "—"))
                    c4.metric("Total (s)", timings.get("total_seconds", "—"))

                    answer_for_history = final_output

                else:
                    answer = agent_reply(
                        user_text=user_text,
                        model=model,
                        temperature=float(temperature),
                    )

                    final_output = answer + DISCLAIMER
                    st.write(final_output)
                    answer_for_history = final_output

            except Exception as e:
                answer_for_history = (
                    "I hit an error calling the local model.\n\n"
                    "Checklist:\n"
                    "1) Is Ollama installed?\n"
                    "2) Is it running? Try: `ollama serve`\n"
                    "3) Did you pull the model? Try: `ollama pull llama3.2:1b`\n\n"
                    f"Error: {e}"
                )
                st.write(answer_for_history)

    st.session_state.messages.append({"role": "assistant", "content": answer_for_history})