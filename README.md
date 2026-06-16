# aiagent
A Python CLI tool that wraps Google Gemini with an agentic loop, enabling it to list files, read source code, write fixes, and run programs autonomously. Built as part of the Boot.dev "Build an AI Agent in Python" course.

# AI Coding Agent

An autonomous AI coding agent built in Python, powered by Google Gemini. Given a natural language prompt, it plans and executes a series of tool calls to inspect, modify, and run code in a local codebase — all on its own.

## Features

- List files and directories within a working directory
- Read file contents (with truncation for large files)
- Write or overwrite files
- Execute Python files with optional arguments
- Iterative agentic loop — the agent keeps acting until the task is done or a max iteration limit is hit
- Sandboxed — all file and execution operations are restricted to the working directory

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended)
- A [Google Gemini API key](https://aistudio.google.com/)

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>

2. Install dependency:
   uv sync
   
3. Create a .env file with your API key:
   GEMINI_API_KEY=your_key_here

4.Run
  uv run main.py "Your prompt here" 
  || 
  Add --verbose to see token counts and tool call responses: uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20" --verbose

## How It Works

The agent runs in a loop, calling Gemini with a system prompt and a set of available tools.

1. Gemini receives the user's prompt and the available tools.
2. Gemini decides which tool(s) to call.
3. The agent executes the requested tool(s).
4. The results are returned to Gemini.
5. The process repeats until Gemini returns a final response or the maximum iteration limit is reached.

### Project Structure

```text
.
├── main.py                # Entry point and agentic loop
├── call_function.py       # Tool dispatch
├── prompts.py             # System prompt
├── config.py              # Configuration and constants
│
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
```

### Agent Workflow

```text
User Prompt
     │
     ▼
  Gemini
     │
     ├── Calls Tool
     ▼
 Agent
     │
     ├── Executes Tool
     ▼
 Tool Result
     │
     ▼
  Gemini
     │
     └── Repeat until final response
```
