import os

from requests import head
import openai
from dotenv import load_dotenv
import re
import gradio as gr
from random import shuffle
import matplotlib.pyplot as plt
import numpy as np
import argparse
import yaml

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

#N_QUESTIONS = 0
LABELLING = {"x_left":"", "x_right":""}
INPUT_INFO = []
#DESCRIPTION = ""
DISCLAIMER = "**Caution! The questions from the test are AI generated and have not been validated by qualified persons. Therefore, interpret the test at your own risk.**"

def create_chat_completion(question, previous_messages):
    return openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.0,
        messages=previous_messages + [{"role": "user", "content": question}]
    )

def create_test_one_dimension(description, labelling, num_questions):
    questions = [
        f"""Your task is to design a test with {num_questions} questions. The goal for a test taker is to see where they land on the spectrum of the test. The test output is a spectrum on one x-axis; the x-axis is represented by {labelling["x_left"]} on the left end and with {labelling["x_right"]} on the right end. The right end can be defined as {description}. {labelling["x_left"]} is the opposite. Do you understand this so far?""",
        f"""Great! Now, please create the questions. They should vary and should not be too similar. You need to create {num_questions} questions where each question can be answered with "Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree". Here's how an example of your answer would look like:
        1. This is an example. [{labelling["x_right"]}]
        2. This is another example. [{labelling["x_left"]}]
        At the end of the questions are tags to clearly indicate the tag each question supports. Now, please create all {num_questions / 2} questions with tag for {labelling["x_right"]} and make them not to similar. ## {labelling["x_right"]}:""",
        f"""Great! Next, please create the other {num_questions / 2} questions with tag for {labelling["x_left"]}. ## {labelling["x_left"]}:""",
        f"""Great! Next, please create a short appropriate title for the test.""",
        f"""Great! Next, please create a appropriate description for the test. The user should be able to know what to expect from the test."""
    ]
    responses = []
    previous_messages = [{"role": "system", "content": "You are are a professional test writer."}]
    for question in questions:
        response = create_chat_completion(question, previous_messages)
        responses.append(response.choices[0].message["content"])
        previous_messages.append({"role": "assistant", "content": responses[-1]})
    return responses[0], responses[1], responses[3], responses[4]

#create_questions_one_dimension()
#above should have created questions
#need to parse them 
def parse_questions(string):
    lines = string.strip().split("\n")
    questions = []
    for line in lines:
        match = re.match(r"^\d+\.\s+(.*)\s+\[(.*)\]$", line)
        if match:
            question, tag = match.groups()
            questions.append({question: tag})
    return questions

def validate_form(*inputs):
    global INPUT_INFO
    score_map = {
        "Strongly Agree": 2,
        "Agree": 1,
        "Neutral": 0,
        "Disagree": -1,
        "Strongly Disagree": -2
    }
    x_right = 0
    x_left = 0
    for input_index in range(len(inputs)):
        checkbox = inputs[input_index]
        tag = INPUT_INFO[input_index]["tag"]
        key = [k for k, v in LABELLING.items() if v == tag][0]
        if key == "x_right":
            x_right += score_map[checkbox]
        else:
            x_left += score_map[checkbox]
        if checkbox is None:
            raise gr.Error("Cannot divide by zero!")
    final = x_right + x_left
    fig, ax = plt.subplots()
    ax.hlines(1, -10, 10, linestyles='solid')
    ax.plot(final, 1, 'ro')
    ax.set_xticks([-10, 0, 10])
    ax.set_xticklabels([LABELLING["x_left"], 'Neutral', LABELLING["x_right"]])
    ax.get_yaxis().set_visible(False)
    return plt

#create the gradio best on questions 
def create_gradio(title, description, questions_x_left_formatted, questions_x_right_formatted):
    global INPUT_INFO

    combined_questions = questions_x_left_formatted + questions_x_right_formatted
    shuffle(combined_questions)

    with gr.Blocks() as demo:
        title = gr.Markdown(f"# {title}")
        description = gr.Markdown(description)
        disclaimer = gr.Markdown(DISCLAIMER)
        inputs = []

        for question_dict in combined_questions:
            question = list(question_dict.keys())[0]
            tag = list(question_dict.values())[0]
            checkbox = gr.inputs.Radio(choices=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], label=question)
            inputs.append(checkbox)
            input_dict = {"question": question, "tag": tag}
            INPUT_INFO.append(input_dict)

        submit_button = gr.Button("Submit")
        plot = gr.Plot(label="Plot")
        submit_button.click(fn=validate_form, inputs=inputs, outputs=[plot], api_name="Submit")
        demo.launch()

def deploy_gradio(name):
    os.system("gradio deploy")    

class Config:
    def __init__(self, description, x_left, x_right, num_questions):
        self.description = description
        self.labelling = {"x_left": x_left, "x_right": x_right}
        self.num_questions = num_questions

def load_config():
    with open('auto_test_config.yaml') as f:
        args = yaml.safe_load(f)

    if args['dimensions'] == 2 or args['dimensions'] == 3:
        raise ValueError("This functionality is not implemented yet but stay tuned for future updates")

    if not 1 <= args['num_questions'] <= 50:
        raise ValueError("Number of questions must be between 10 and 50")
    
    description = args["description"]
    x_left = args["x_left"]
    x_right = args["x_right"]
    num_questions = args["num_questions"]
    labelling = {"x_left": x_left, "x_right": x_right}

    return description, num_questions, labelling

def main():
    global LABELLING
    description, num_questions, labelling = load_config()
    LABELLING = labelling
    # Call the function to create test one dimension
    questions_x_right, questions_x_left, title, description = create_test_one_dimension(description, labelling, num_questions)
    questions_x_right_formatted = parse_questions(questions_x_right)
    questions_x_left_formatted = parse_questions(questions_x_left)

    # Create the gradio 
    create_gradio(title, description, questions_x_right_formatted, questions_x_left_formatted)

if __name__ == "__main__":
    main()