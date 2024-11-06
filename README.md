# Problem Processing and Mutation System

## Overview
This Python application automates the processing and mutation of problem statements from `problems.txt`. It supports mutation strategies using OpenAI’s GPT models and tracks processed problems in a leaderboard format.

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/problem-mutation-system.git
   cd problem-mutation-system

2. Install dependencies:
   pip install -r requirements.txt

3. Set your OpenAI API key:
   export OPENAI_API_KEY="your-api-key"

## Usage
Run the main script:
   python process_problems.py --agent "gpt-4" --num_rounds 5 --num_problems 10 --topk_problems 5 --mutate_on_start

## Testing
Run the unit tests:
   pytest tests/test_process_problems.py
