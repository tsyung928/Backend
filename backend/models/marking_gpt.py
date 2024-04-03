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

def chain_of_thought(student_work, rubrics, description) :
    return (
    "The essay below needs to be evaluated according to the accompanying scoring rubric."
    "Adopt a Chain of Thought approach for your evaluation, carefully considering each criterionmentioned in the rubric."
    "Your analysis should logically step through the evaluation, addressing the quality of the essay's argumentation, structure, clarity, and any other criteria specified in the rubric. "
    "Conclude by summarizing the total score based on the criteria evaluations and providing detailed, constructive feedback."
    "Ensure your analysis is adaptable and thoroughly evaluating all aspects as outlined in the provided rubric. "
    "This is the description of the assignment: "+ description + "These are the marking rubrics: " + rubrics + "This is the student's work: " + student_work+
    "The final output should be in the following format:\n "
    "1. Score: [Your Score Here] \n"
    "2. Explanation: [Your Explanation Here]")




def gpt_mark(student_work, rubrics, description):
    # Process the student's work with GPT-3
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": "You are a English Teacher, skilled in marking English essays. You will be given a piece of student work, score the work based on the rubric provided and explain the reasoning behind the score.  You should give out marks in numerical numbers only according to the rubrics provided, and give score explanations. You should not provided another other details except the marks and score explanations"},
        #     {"role": "user", "content": "This is the description of the assignment: "+ description + "These are the marking rubrics: " + rubrics + "This is the student's work: " + student_work+ "Please provide your response in the following format:\n 1. Score: [Your Score Here] \n2. Explanation: [Your Explanation Here]"}
        # ]
        messages=[
            {"role": "system", "content": "You are a English Teacher, skilled in marking English essays. You will be given a piece of student work, score the work based on the rubric provided and explain the reasoning behind the score.  You should give out marks in numerical numbers only according to the rubrics provided, and give score explanations. You should not provided another other details except the marks and score explanations"},
            {"role": "user", "content": chain_of_thought(student_work, rubrics, description)}
        ]
    )
    return completion.choices[0].message.content

