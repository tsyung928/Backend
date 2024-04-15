import csv
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def read_essays_from_csv(file_path):
    examples = []
    with open(file_path, newline='', encoding='utf-8', errors='replace') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            examples.append({
                "student_work": row["student_work"],
                "essay_question_description": row["essay_question_description"],
                "human_graded_score": row["human_graded_score"],
                "human_graded_comments": row["human_graded_comments"],
                "scoring_rubric": row["scoring_rubric"]
            })
    return examples

def few_shot(examples, student_work, rubrics, description):
    prompt = "Below are examples of how essays are evaluated based on their content, structure, and adherence to the provided rubric. Each example includes the essay question, a piece of student work, the score given by a human grader, the grader's comments, and the scoring rubric.\n\n"
    for example in examples:
        prompt += "Essay Question: {}\nStudent Work: {}\nScore: {}\nExplanation: {}\nRubric: {}\n---\n".format(
            example["essay_question_description"],
            example["student_work"],
            example["human_graded_score"],
            example["human_graded_comments"],
            example["scoring_rubric"]
        )
    prompt += "Essay Question: {}\nStudent Work: {}\nRubric: {}\nPlease score the following essay and provide your explanation based on the rubric provided.\n"
    "The final output should follow the exact format below:\n "
    "Score: [Your Score Here] \n"
    "Explanation: [Your Explanation Here]".format(
        description, student_work, rubrics
    )
    return prompt

def chain_of_thought(student_work, rubrics, description) :
    return (
    "The essay below needs to be evaluated according to the accompanying scoring rubric."
    "Adopt a Chain of Thought approach for your evaluation, carefully considering each criterionmentioned in the rubric."
    "Your analysis should logically step through the evaluation, addressing the quality of the essay's argumentation, structure, clarity, and any other criteria specified in the rubric. "
    "Conclude by summarizing the total score based on the criteria evaluations and providing detailed, constructive feedback."
    "Ensure your analysis is adaptable and thoroughly evaluating all aspects as outlined in the provided rubric. "
    "This is the description of the assignment: "+ description + "These are the marking rubrics: " + rubrics + "This is the student's work: " + student_work+
    "The final output should follow the EXACT format below:\n "
    "Score: [Your Score Here] \n"
    "Explanation: [Your Explanation Here]")

def zero_shot(student_work, rubrics, description):
    return ("This is the description of the assignment: "+ description +
            "These are the marking rubrics: " + rubrics +
            "This is the student's work: " + student_work +
            "Please provide your response in the following format:\n "
            "Score: [Your Score Here] \n"
            "Explanation: [Your Explanation Here]"
    )

def gpt_mark(student_work, rubrics, description):
    # Process the student's work with GPT-3
    examples = read_essays_from_csv("sampleEssayForFewShot.csv")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": "You are a English Teacher, skilled in marking English essays. You will be given a piece of student work, score the work based on the rubric provided and explain the reasoning behind the score.  You should give out marks in numerical numbers only according to the rubrics provided, and give score explanations. You should not provided another other details except the marks and score explanations"},
        #     {"role": "user", "content": few_shot(examples, student_work, rubrics, description)}
        # ]
        messages=[
            {"role": "system",
             "content": "You are a English Teacher, skilled in marking English essays. You will be given a piece of student work, score the work based on the rubric provided and explain the reasoning behind the score.  You should give out marks in numerical numbers only according to the rubrics provided, and give score explanations. You should not provided another other details except the marks and score explanations"},
            {"role": "user", "content": few_shot(examples, student_work, rubrics, description)}
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

