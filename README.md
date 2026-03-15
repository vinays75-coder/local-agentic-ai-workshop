# Local Agentic AI Workshop

This workshop demonstrates how to build a local Agentic AI application using:

- Python
- Ollama (For Running and Hosting models locally)
- Streamlit

The system uses a two-agent architecture:

Planner Agent
Decides how to solve the task and whether to use tools.

Executor Agent
Produces the final response.

## Setup

Install prerequisites:

Python
Git
Ollama

Install dependencies:

pip install -r requirements.txt

Pull the local model:

ollama pull llama3.2:1b

Run the app:

streamlit run app.py

## Example Prompts

Create a checklist for hosting a birthday party.

Give me a pros and cons list for buying an e-bike under $600.

Create a 3-hour time block study plan.
