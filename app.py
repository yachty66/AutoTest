import os
from requests import head
import openai
from dotenv import load_dotenv
import re
import gradio as gr
from random import shuffle
import matplotlib.pyplot as plt
import yaml
import shutil
import pickle
from huggingface_hub import HfApi

#load_dotenv()

#HF_TOKEN = os.getenv('HF_TOKEN')
DISCLAIMER = "**Caution! The questions from the test are AI generated and have not been validated by qualified persons. Therefore, interpret the test at your own risk.**"

def validate_form(*inputs):
    #global INPUT_INFO
    score_map = {
        "Strongly Agree": 2,
        "Agree": 1,
        "Neutral": 0,
        "Disagree": -1,
        "Strongly Disagree": -2
    }
    x_right = 0
    x_left = 0
    number_questions = len(inputs)
    for input_index in range(number_questions):
        checkbox = inputs[input_index]
        if checkbox is None:
            raise gr.Error("You forgot a checkbox!")
        tag = INPUT_INFO[input_index]["tag"]
        key = [k for k, v in LABELLING.items() if v == tag][0]
        if key == "x_right":
            x_right += score_map[checkbox]
        else:
            x_left += score_map[checkbox]
    final = x_right + (-x_left)
    fig, ax = plt.subplots()
    ax.hlines(1, 2*(-number_questions), 2*number_questions, linestyles='solid')
    ax.plot(final, 1, 'ro')
    ax.set_xticks([2*(-number_questions), 0, 2*number_questions])
    ax.set_xticklabels([LABELLING["x_left"], 'Neutral', LABELLING["x_right"]])
    ax.get_yaxis().set_visible(False)
    return plt

#def create_gradio(title, description, questions_x_left_formatted, questions_x_right_formatted):
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
# Assign loaded data to variables
title = data["title"]
description = data["description"]
questions_x_right_formatted = data["questions_x_right_formatted"]
questions_x_left_formatted = data["questions_x_left_formatted"]
LABELLING = data["LABELLING"]
INPUT_INFO = data["INPUT_INFO"]
#global INPUT_INFO
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

"""def deploy_gradio(name):
    # Initialize the HfApi class
    hf_api = HfApi()
    # Define your token
    token = HF_TOKEN
    # Create a new huggingface repo
    repo_url = hf_api.create_repo(
        repo_id=name,
        token=token,
        private=False,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True
    )
    # Clone the repository
    os.system(f'git clone {repo_url}')
    # Copy the files into the repository
    shutil.copy('app.py', f'{name}/app.py')
    shutil.copy('requirements.txt', f'{name}/requirements.txt')
    shutil.copy('auto_test_config.yaml', f'{name}/auto_test_config.yaml')
    # Add the files to the repository
    os.system(f'cd {name} && git add .')
    # Commit the changes
    os.system(f'cd {name} && git commit -m "Initial commit"')
    # Push the changes
    os.system(f'cd {name} && git push')"""

#global LABELLING
#global INPUT_INFO
# Load data from pickle file

#create_gradio(title, description, questions_x_right_formatted, questions_x_left_formatted)


