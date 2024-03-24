import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

def gpt_mark(student_work, rubrics, description):
    # Process the student's work with GPT-3
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a English Teacher, skilled in marking English essays. You will be given a piece of student work, score the work based on the rubric provided and explain the reasoning behind the score.  You should give out marks according to the rubrics provided, and give score explanations. You should not provided another other details except the marks and score explanations"},
            {"role": "user", "content": "This is the description of the assignment: "+ student_work + "These are the marking rubrics: " + rubrics + "This is the student's work: " + student_work+ "Please provide your response in the following format:\n 1. Score: [Your Score Here] \n2. Explanation: [Your Explanation Here]"}
        ]
    )
    return completion.choices[0].message.content

