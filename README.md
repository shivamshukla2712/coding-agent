# coding-agent

A CLI coding agent powered by Google Gemini that can read, write, and execute code on your behalf. By default it operates on the `./calculator` project as its working directory.

## How it works

The agent uses Gemini 2.5 Flash with function-calling to iteratively plan and execute steps:

1. You provide a natural-language prompt
2. The agent calls tools (list files, read files, write files, run Python) until it has a final answer
3. The final response is printed to stdout

Available tools:

| Tool | Description |
|------|-------------|
| `get_files_info` | List files and directories |
| `get_file_content` | Read a file's contents |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file with optional arguments |

## Prerequisites

- Python 3.8+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd shivam-coding-agent

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

## Usage

```bash
python main.py "<your prompt>"
```

**Options:**

| Flag | Description |
|------|-------------|
| `--verbose` | Print token counts, function call arguments, and raw responses |

**Examples:**

```bash
# Ask the agent to explain the calculator project
python main.py "What does the calculator app do?"

# Ask it to fix a bug
python main.py "Fix the bug in calculator.py where division by zero isn't handled"

# Ask it to add a feature
python main.py "Add a square root operation to the calculator"

# Verbose mode to see every function call
python main.py "List all the files in the project" --verbose
```

## Project structure

```
shivam-coding-agent/
├── main.py                  # Entry point and agent loop
├── config.py                # Model name and limits
├── prompts.py               # System prompt
├── functions/
│   ├── call__function.py    # Dispatches tool calls
│   ├── get_file_info.py     # List files tool
│   ├── get_file_content.py  # Read file tool
│   ├── write_file.py        # Write file tool
│   └── run_python_file.py   # Execute Python tool
└── calculator/              # Default working directory for the agent
    └── main.py
```

## Configuration

| Variable | Location | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | `.env` | Your Gemini API key |
| `model_name` | `config.py` | Gemini model to use (default: `gemini-2.5-flash`) |
| `MAX_CHARS` | `config.py` | Max characters returned from file reads (default: `10000`) |
| `working_directory` | `functions/call__function.py` | Directory the agent operates in (default: `./calculator`) |
