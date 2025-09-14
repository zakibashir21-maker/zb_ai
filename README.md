# zb_ai

A simple passive-aggressive roasting chatbot using OpenAI's GPT-3.5-turbo API.

## Description

This project contains a Python chatbot (`my_chatbot.py`) that interacts with users via the command line. The bot responds to user prompts with passive-aggressive roasts, powered by OpenAI's GPT-3.5-turbo model.

### Features
- Loads the OpenAI API key from a local `credentials.txt` file (not tracked in git)
- Prompts the user for input and responds with a roast
- Exits when the user types "goodbye" or "exit"

## Setup

1. Create a `credentials.txt` file in the project directory and paste your OpenAI API key inside.
2. Install dependencies:
   - openai

## Usage

Run the chatbot:
```bash
python my_chatbot.py
```

## Requirements

- Python 3.7+
- openai

## Security
- The API key is loaded from `credentials.txt` and this file is excluded from git via `.gitignore`.

## License
See `LICENSE` for details.
