import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
#how many dimensions the test in the end has, one, two or N dimensions
TYPE = 0
#number of questions 
N_QUESTIONS = 20
#description of how the result should be labelled 
LABELLING = {"y_top":"capitalism", "y_bottom":"communism", "x_left":"autocracy", "x_right":"democracy"}
#description of how the test should be designed
DESCRIPTION = ""



"""
Here's the corrected text:

1. Your task is to design a test with {N} questions. The goal for a test taker is to see where they land on the spectrum of the test. The test outputs {{x} possible axes; the x-axis represents the {x_axis_value}. On the far left side of the spectrum, {x_axis_value_left} is represented, and on the right side, {x_axis_value_right} is represented. The right end can be defined as {description}. {Here, you can provide a description of the other end OR the left end is the opposite of the right side}. Do you understand this so far?
2. Great! Now, please create the questions. They should vary and should not be too similar. You need to create {N} questions where each question can be answered with "Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree". Here's how an example of your answer would look like:
    1. This is an example. [{x_axis_right}]
    2. This is another example. [{x_axis_left}]

    At the end of the questions are tags to clearly indicate the ideology each question supports. Now, please create all {N/2} questions for {x_axis_right}. ## {x_axis_right}:
3. Great! Next, please create the other {N/2} questions for {x_axis_left}. ## {x_axis_left}:
"""

def create_questions():
    question_one = "Your task is to design a test with {N} questions. The goal for a test taker is to see where they land on the spectrum of the test. The test output is a spectrum on one x axis; the x-axis is represented by {x_axis_value_left} on the left side of the spectrum and with {x_axis_value_right} on the right side. The right end can be defined as {description}. {x_axis_value_left} is the opposite. Do you understand this so far?"
    response_user_question_one = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = "0.2", 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
            ]
    )
    question_two = f"""
    Great! Now, please create the questions. They should vary and should not be too similar. You need to create {N_QUESTIONS} questions where each question can be answered with "Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree". Here's how an example of your answer would look like:
    1. This is an example. [{LABELLING["x_right"]}]
    2. This is another example. [{LABELLING["x_left"]}]

    At the end of the questions are tags to clearly indicate the tag each question supports. Now, please create all {N_QUESTIONS / 2} questions with tag for {LABELLING["x_right"]}. ## {LABELLING["x_right"]}:
    """
    response_user_question_two = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = "0.2", 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
                {"role": "assistant", "content": response_user_question_one},
                {"role": "assistant", "content": question_two},
            ]
    )
    question_three = f"""Great! Next, please create the other {N_QUESTIONS / 2} questions with tag for {LABELLING["x_left"]}. ## {LABELLING["x_left"]}:"""
    response_user_question_three = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = "0.2", 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
                {"role": "assistant", "content": response_user_question_one},
                {"role": "assistant", "content": question_two},
                {"role": "assistant", "content": response_user_question_two},
                {"role": "assistant", "content": question_three},
            ]
    )



result = ''
for choice in response.choices:
    result += choice.message.content

print(result)
