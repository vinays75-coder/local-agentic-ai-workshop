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
| Tool                        | Verification Command              | Common Problems                    | Troubleshooting                                                            | (Run from Terminal)
| --------------------------- | --------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| **Python**                  | `python --version`        | `python` command not found         | Try:<br>`python3 --version\n`<br>Restart terminal after installation |
| **Git**                     | `git --version`           | Git not recognized                 | Restart terminal or reinstall Git                                          |
| **Ollama**                  | `ollama --version`        | Ollama command not found           | Restart terminal after installation                                        |
| **Ollama Model**            | `ollama pull llama3.2:1b` | Model not downloaded               | Ensure Ollama is installed correctly                                       |
| **Python Path (Mac/Linux)** | `which python`            | Python installed but command fails | Ensure Python is added to PATH                                             |


## Example Prompts

Create a checklist for hosting a birthday party.

Give me a pros and cons list for buying an e-bike under $600.

Create a 3-hour time block study plan.
