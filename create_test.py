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

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

#how many dimensions the test in the end has, one, two or N dimensions
TYPE = 0
#number of questions 
N_QUESTIONS = 2
#description of how the result should be labelled 
LABELLING = {"y_top":"capitalism", "y_bottom":"communism", "x_left":"Effective Decelerationism", "x_right":"Effective Accelerationism"}
INPUT_INFO = []
#description for right side of x_axis on how the test should be designed
DESCRIPTION = """
Accelerationism is simply the self-awareness of capitalism, which has scarcely begun. ("We haven't seen anything yet.")

1. The overarching goal for humanity is to preserve the light of consciousness.
2. Technology and market forces (technocapital) are accelerating in their power and abilities.
3. This force cannot be stopped.
4. Technocapital can usher in the next evolution of consciousness, creating unthinkable next-generation lifeforms and silicon-based awareness.
5. New forms of consciousness by definition will make sentience more varied and durable. We want this.
6. Technology is leverage. As it advances, it becomes easier to extinquish all conscious life in our corner of the universe.
Attempting to stall progress isn't risk free.
7. Society and the individual's context within it are rapidly changing, which leads to greater societal instability and mind viruses. (deterritorialisation and reterritorialisation).
8. Those who are the first to usher in and control the hyper-parameters of AI/technocapital have immense agency over the future of consciousness.
9. HUMANS HAVE AGENCY RIGHT NOW. WE CAN AFFECT THE ADVENT OF THE
INFLECTION IN THIS PROCESS.
10. Effective Accelerationism, e/acc, is a set of ideas and
practices that seek tomaximize the probability of the
technocapital singularity, and subsequently, the ability for
emergent consciousness to flourish. There is much work to be done in defining cause areas, motivations,
and philosophy. Please join us on #eacc twitter, and let's work
towards a hundred trillion meta-organisms flourishing in the galaxy.
"""

def create_test_one_dimension():
    question_one = f"""Your task is to design a test with {N_QUESTIONS} questions. The goal for a test taker is to see where they land on the spectrum of the test. The test output is a spectrum on one x-axis; the x-axis is represented by {LABELLING["x_left"]} on the left end and with {LABELLING["x_right"]} on the right end. The right end can be defined as {DESCRIPTION}. {LABELLING["x_left"]} is the opposite. Do you understand this so far?"""
    question_two = f"""
    Great! Now, please create the questions. They should vary and should not be too similar. You need to create {N_QUESTIONS} questions where each question can be answered with "Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree". Here's how an example of your answer would look like:
    1. This is an example. [{LABELLING["x_right"]}]
    2. This is another example. [{LABELLING["x_left"]}]

    At the end of the questions are tags to clearly indicate the tag each question supports. Now, please create all {N_QUESTIONS / 2} questions with tag for {LABELLING["x_right"]} and make them not to similar. ## {LABELLING["x_right"]}:
    """
    answer_one = "Yes, I understand. I am looking forward helping you with the design of the test!"
    response_one = openai.ChatCompletion.create(
        model="gpt-4",
        temperature = 0.0, 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
                {"role": "assistant", "content": answer_one},
                {"role": "user", "content": question_two},
            ]
    )
    response_one_content = response_one.choices[0].message["content"]
    question_three = f"""Great! Next, please create the other {N_QUESTIONS / 2} questions with tag for {LABELLING["x_left"]}. ## {LABELLING["x_left"]}:"""
    response_two = openai.ChatCompletion.create(
        model="gpt-4",
        temperature = 0.0, 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
                {"role": "assistant", "content": answer_one},
                {"role": "user", "content": question_two},
                {"role": "assistant", "content": response_one_content},
                {"role": "user", "content": question_three},
            ]
    )
    #get title for test
    response_two_content = response_one.choices[0].message["content"]
    question_four = f"""Great! Next, please create a short appropriate title for the test."""
    response_three = openai.ChatCompletion.create(
        model="gpt-4",
        temperature = 0.0, 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
                {"role": "assistant", "content": answer_one},
                {"role": "user", "content": question_two},
                {"role": "assistant", "content": response_one_content},
                {"role": "user", "content": question_three},
                {"role": "assistant", "content": response_two_content},
                {"role": "user", "content": question_four},
            ]
    )
    title = response_three.choices[0].message["content"]

    #get description for the test
    question_five = f"""Great! Next, please create a appropriate description for the test. The user should be able to know what to expect from the test."""
    response_four = openai.ChatCompletion.create(
        model="gpt-4",
        temperature = 0.0, 
        messages=[
                {"role": "system", "content": "You are are a professional test writer."},
                {"role": "user", "content": question_one},
                {"role": "assistant", "content": answer_one},
                {"role": "user", "content": question_two},
                {"role": "assistant", "content": response_one_content},
                {"role": "user", "content": question_three},
                {"role": "assistant", "content": response_two_content},
                {"role": "user", "content": question_four},
                {"role": "assistant", "content": title},
                {"role": "user", "content": question_five},
            ]
    )
    description = response_four.choices[0].message["content"]
    return response_one.choices[0].message["content"], response_two.choices[0].message["content"], title, description

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
    global input_info
    print("inputs in validate form:")
    print(inputs)    
    #calculate the score 
    x_right = 0
    x_left = 0
    final = 0
    for i in range(len(inputs)):        
        checkbox = inputs[i]
        tag = INPUT_INFO[i]["tag"]
        key = [k for k, v in LABELLING.items() if v == tag][0]
        if key == "x_right":
            if checkbox == "Strongly Agree":
                x_right += 2
            elif checkbox == "Agree":
                x_right += 1
            elif checkbox == "Neutral":
                x_right += 0
            elif checkbox == "Disagree":
                x_right -= 1
            elif checkbox == "Strongly Disagree":
                x_right -= 2
        else:
            if checkbox == "Strongly Agree":
                x_left += 2
            elif checkbox == "Agree":
                x_left += 1
            elif checkbox == "Neutral":
                x_left += 0
            elif checkbox == "Disagree":
                x_left -= 1
            elif checkbox == "Strongly Disagree":
                x_left -= 2
        final = x_right + x_left
        if checkbox is None:
            raise gr.Error("Cannot divide by zero!")
    fig, ax = plt.subplots()
    ax.hlines(1, -10, 10, linestyles='solid')
    ax.plot(final, 1, 'ro')
    ax.set_xticks([-10, 0, 10])
    ax.set_xticklabels([LABELLING["x_left"], 'Neutral', LABELLING["x_right"]])
    ax.get_yaxis().set_visible(False)
    return plt

#create the gradio best on questions 
def create_gradio(title, description, questions, questions_x_left_formatted, questions_x_right_formatted):
    global INPUT_INFO
    title = title 
    description = description
    disclaimer = "**Caution! The questions from the test are AI generated and have not been validated by qualified persons. Therefore, interpret the test at your own risk.**"
    combined_questions = questions_x_left_formatted + questions_x_right_formatted
    shuffle(combined_questions)
    #create items inside the block where with respective weighting        
    with gr.Blocks() as demo:
        title = gr.Markdown(f"# {title}")
        description = gr.Markdown(description)
        disclaimer = gr.Markdown(disclaimer)
        inputs = []
        for i in combined_questions:
            question = list(i.keys())[0]
            tag = list(i.values())[0]
            checkbox = gr.inputs.Radio(choices=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], label=question)
            inputs.append(checkbox)
            input_dict = {"question": question, "tag": tag}
            INPUT_INFO.append(input_dict)            
        greet_btn = gr.Button("Submit")
        print("inputs:")
        print(inputs)
        plot = gr.Plot(label="Plot")
        greet_btn.click(fn=validate_form, inputs=inputs, outputs=[plot], api_name="Submit")
        demo.launch()

def deploy_gradio():
    os.system("gradio deploy")    

def cli():
    """
    assistant: hey. you are here to let AI create an test for you! i highly encourage you to first read the readme so that you are getting the most out of creating your test. if you havent, head over to [this](link) page. first you need to define say how many dimensions your test will have:

    [one dimension]
    [two dimensions]
    [N dimension]

    user: two dimensions

    assistant: this functionality is not implemented yet but stay tuned for future updates 

    user: one dimension

    assistant: great choice! next Label the ends of your x-axis with the corresponding names of the spectra you want to test for.

    [x_left]

    user: Effective Decelerationism

    assistant: [x_right]

    user: Effective Accelerationism

    assistant: great! in the next step please describe your test. based on this description questions for the test are generated. again, if you havent read the [readme](link) so far, now you should to not mess up the description!:

    user: description

    assistant: Well! almost done! in the last step you need to define of how many questions your test exists of. the number can range between 10 and 50:

    user: 54

    assistant: number to high, please repeat:

    user: 2

    assistant: number to low, please repeat:

    user: 12

    assistant: okay. your test is getting deployed. once deployment is complete a link with your test is shared to you. wait a bit.

    🎉link     
    """
    pass

def main():
    #depending on which option is given here the test creates 
    # Call the function to create test one dimension
    questions_x_right, questions_x_left, title, description = create_test_one_dimension()
    questions_x_right_formatted = parse_questions(questions_x_right)
    questions_x_left_formatted = parse_questions(questions_x_left)
    # Parse the questions
    # Create the gradio 
    create_gradio(title, description, questions_x_right_formatted, questions_x_right_formatted, questions_x_left_formatted)

if __name__ == "__main__":
    main()
