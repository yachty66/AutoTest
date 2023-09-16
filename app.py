import gradio as gr
from random import shuffle
import matplotlib.pyplot as plt
import pickle

DISCLAIMER = "**Caution! The questions from the test are AI generated and have not been validated by qualified persons. Therefore, interpret the test at your own risk.**"

def validate_form(*inputs):
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

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
title = data["title"]
description = data["description"]
questions_x_right_formatted = data["questions_x_right_formatted"]
questions_x_left_formatted = data["questions_x_left_formatted"]
LABELLING = data["LABELLING"]
INPUT_INFO = data["INPUT_INFO"]
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

