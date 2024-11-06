import argparse
import os
import random
import re
import subprocess
import time
import uuid
import yaml
import openai
from dataclasses import dataclass, field
from typing import List, Tuple

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the data structure for a problem statement
@dataclass
class Problem:
    id: str
    statement: str
    score: float = 0.0
    mutations: List[str] = field(default_factory=list)

# Load problem statements from problems.txt
def load_problems(file_path: str) -> List[Problem]:
    problems = []
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines():
                problem_statement = line.strip()
                problem_id = str(uuid.uuid4())
                problems.append(Problem(id=problem_id, statement=problem_statement))
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        exit(1)
    return problems

# Mutation strategies
def mutate_problem(problem: Problem, mutation_type: str, prompt: str) -> str:
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"{prompt}: {problem.statement}",
            max_tokens=200
        )
        mutated_statement = response.choices[0].text.strip()
        problem.mutations.append(mutated_statement)
        return mutated_statement
    except Exception as e:
        print(f"Error during mutation: {e}")
        return problem.statement

# Evaluate problem statement quality using OpenAI's GPT model
def evaluate_problem(problem: Problem) -> float:
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"Rate the quality of the following problem statement on a scale from 0 to 1. The higher the score, the better the quality. Problem statement: {problem.statement}",
            max_tokens=50
        )
        score = float(response.choices[0].text.strip())
        score = max(0.0, min(score, 1.0))
        return score
    except Exception as e:
        print(f"Error during problem evaluation: {e}")
        return random.uniform(0, 1)

# Save processed problems to a YAML file (leaderboard)
def save_leaderboard(problems: List[Problem], leaderboard_path: str):
    leaderboard = {problem.id: {"statement": problem.statement, "score": problem.score} for problem in problems}
    with open(leaderboard_path, 'w') as file:
        yaml.dump(leaderboard, file)

# Function to process problems in rounds
def process_round(problems: List[Problem], num_problems: int, top_k: int, mutate_on_start: bool, mutation_type: str, prompt: str) -> List[Problem]:
    selected_problems = random.sample(problems, num_problems)

    for problem in selected_problems:
        if mutate_on_start:
            mutated_statement = mutate_problem(problem, mutation_type, prompt)
            problem.statement = mutated_statement
        problem.score = evaluate_problem(problem)

    sorted_problems = sorted(selected_problems, key=lambda p: p.score, reverse=True)
    return sorted_problems[:top_k]

# Argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Problem Processing and Mutation System")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random operations")
    parser.add_argument("--agent", type=str, required=True, help="Specify the AI agent to use (e.g., gpt-4)")
    parser.add_argument("--num_rounds", type=int, default=5, help="Number of processing rounds")
    parser.add_argument("--num_problems", type=int, default=10, help="Number of problems to process per round")
    parser.add_argument("--topk_problems", type=int, default=5, help="Number of top problems to retain each round")
    parser.add_argument("--mutate_on_start", action="store_true", help="Flag to apply mutation at the start of each round")
    return parser.parse_args()

def main():
    args = parse_arguments()

    random.seed(args.seed)

    problems = load_problems("problems/problems.txt")

    mutation_type = "rephrase"
    prompt = "Rephrase this problem statement for clarity"

    all_round_problems = []
    for _ in range(args.num_rounds):
        round_problems = process_round(problems, args.num_problems, args.topk_problems, args.mutate_on_start, mutation_type, prompt)
        all_round_problems.extend(round_problems)

    save_leaderboard(all_round_problems, "leaderboard.yaml")

if __name__ == "__main__":
    main()
