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

# 🔧 Workshop Prerequisites

| S.No | Software / Tool                      | Purpose                                                    | Download Link                                        | Approx Install Time | Notes                                                                     |
| ---- | ------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------- | ------------------- | ------------------------------------------------------------------------- |
| 1    | **Python (3.10+)**                   | Programming language used to build the agent system        | [Download Python](https://www.python.org/downloads/) | ~10 mins            | Install Python **3.10 or above** and ensure **“Add to PATH”** is selected |
| 2    | **Ollama**                           | Runs local LLM models such as Llama locally on your laptop | [Download Ollama](https://ollama.com/download)       | ~5 mins             |                          |
| 3    | **Git**                              | Used to clone the workshop repository from GitHub          | [Download Git](https://git-scm.com/downloads)        | ~5 mins             |                                 |
| 4    | **Visual Studio Code (Recommended)** | Lightweight editor for Python development                  | [Download VS Code](https://code.visualstudio.com/)   | ~5 mins             | Install the **Python extension (Recommended)**                                          |

# Verify Installation
| Tool                        | Verification Command (Run from Terminal)              | Common Problems                    | Troubleshooting                                                            |
| --------------------------- | --------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| **Python**                  | `python --version`        | `python` command not found         | Try:<br>`python3 --version\n`<br>Restart terminal after installation |
| **Git**                     | `git --version`           | Git not recognized                 | Restart terminal or reinstall Git                                          |
| **Ollama**                  | `ollama --version`        | Ollama command not found           | Restart terminal after installation                                        |
| **Ollama Model**            | `ollama pull llama3.2:1b` | Model not downloaded               | Ensure Ollama is installed correctly                                       |
| **Python Path (Mac/Linux)** | `which python`            | Python installed but command fails | Ensure Python is added to PATH                                             |
# Steps for Executing the Workshop Content
| S.No | Command to Execute                                                          | Approx Time | Remarks                                                |
| ---- | --------------------------------------------------------------------------- | ----------- | ------------------------------------------------------ |
| 1    | `git clone https://github.com/vinays75-coder/local-agentic-ai-workshop.git` | ~10 sec     | Clone the workshop repository                          |
| 2    | `cd local-agentic-ai-workshop`                                              | ~2 sec      | Navigate to the project folder                         |
| 3    | `python -m venv .venv`                                                      | ~10 sec     | Create a Python virtual environment                    |
| 4a   | **Windows**<br>`\.venv\Scripts\activate`                                    | ~2 sec      | Activate the virtual environment on Windows            |
| 4b   | **Mac / Linux**<br>`source .venv/bin/activate`                              | ~2 sec      | Activate the virtual environment on Mac or Linux       |
| 5    | `pip install -r requirements.txt`                                           | ~2–3 mins   | Install required Python libraries                      |
| 6    | `ollama pull llama3.2:1b`                                                   | ~1–2 mins   | Download the local LLM model required for the workshop |
| 7    | `streamlit run app.py`                                                      | ~5 sec      | Launch the Streamlit application                       |


## Example Prompts

Create a checklist for hosting a birthday party.

Give me a pros and cons list for buying an e-bike under $600.

Create a 3-hour time block study plan.
