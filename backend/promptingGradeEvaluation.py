import numpy as np
import pandas as pd

def load_data(file_path):
    """Load data from a CSV file."""
    data = pd.read_csv(file_path)
    return data['gpt_score'], data['human_grade']

def calculate_mae_rmse(gpt_scores, human_grades):
    """Calculate MAE and RMSE between GPT scores and human grades."""
    mae = np.mean(np.abs(gpt_scores - human_grades))
    rmse = np.sqrt(np.mean((gpt_scores - human_grades) ** 2))
    return mae, rmse

# Paths to CSV files for each prompting technique
file_paths = {
    'Zero Shot': './PromptingGradeEvaluation/ZeroShot.csv',
    'Few Shot': './PromptingGradeEvaluation/FewShot.csv',
    'Chain Of Thought': './PromptingGradeEvaluation/ChainOfThought.csv'
}

# calculate MAE and RMSE
results = {}
for tech, path in file_paths.items():
    gpt_scores, human_grades = load_data(path)
    mae, rmse = calculate_mae_rmse(gpt_scores, human_grades)
    results[tech] = {'MAE': mae, 'RMSE': rmse}

# Print results
for tech, metrics in results.items():
    print(f"Prompting Technique {tech}: MAE = {metrics['MAE']}, RMSE = {metrics['RMSE']}")


