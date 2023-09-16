import os
import pickle 
import openai
from dotenv import load_dotenv
import re
import gradio as gr
from random import shuffle
import matplotlib.pyplot as plt
import yaml
import shutil
from huggingface_hub import HfApi

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')

LABELLING = {"x_left":"", "x_right":""}
INPUT_INFO = []
DISCLAIMER = "**Caution! The questions from the test are AI generated and have not been validated by qualified persons. Therefore, interpret the test at your own risk.**"

def main(name):
    """
    Main function to run the program.
    """
    global LABELLING
    description, num_questions, labelling, title = load_config()
    LABELLING = labelling
    questions_x_right, questions_x_left, description = create_test_one_dimension(description, labelling, num_questions)
    questions_x_right_formatted = parse_questions(questions_x_right)
    questions_x_left_formatted = parse_questions(questions_x_left)
    save_data(title, description, questions_x_right_formatted, questions_x_left_formatted, LABELLING, INPUT_INFO)
    deploy_gradio(name)

def load_config():
    """
    Function to load the configuration from a YAML file.
    """
    with open('auto_test_config.yaml') as f:
        args = yaml.safe_load(f)
    if args['dimensions'] == 2 or args['dimensions'] == 3:
        raise ValueError("This functionality is not implemented yet but stay tuned for future updates")
    if not 1 <= args['num_questions'] <= 50:
        raise ValueError("Number of questions must be between 10 and 50")
    title = args["title"]
    description = args["description"]
    x_left = args["x_left"]
    x_right = args["x_right"]
    num_questions = args["num_questions"]
    labelling = {"x_left": x_left, "x_right": x_right}
    return description, num_questions, labelling, title

def create_test_one_dimension(description, labelling, num_questions):
    """
    Function to create a test with one dimension.
    """
    questions = [
        f"""Great! Now, please create the questions. They should vary and should not be too similar. You need to create {num_questions} questions where each question can be answered with "Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree". Here's how an example of your answer would look like:
        1. This is an example. [{labelling["x_right"]}]
        2. This is another example. [{labelling["x_left"]}]
        At the end of the questions are tags to clearly indicate the tag each question supports. Now, please create all {num_questions / 2} questions for the tag {labelling["x_right"]} and make them not to similar (make sure there are not so many word repetitions). only provide questions for this tag! again it should be {num_questions / 2} number of questions. ## {labelling["x_right"]}:""",
        f"""Great! Next, please create the other {num_questions / 2} questions with the tag {labelling["x_left"]}. Remember to make questions not to similar and try to avoid word repetitions. ## {labelling["x_left"]}:""",
        f"""Great! Next, please create a appropriate description for the test. The user should be able to know what to expect from the test. Only provide the description and no headline. ## Description:"""
    ]
    responses = []
    previous_messages = [{"role": "system", "content": "You are are a professional test writer."}]
    previous_messages.append({"role": "user", "content": f"""Your task is to design a test with {num_questions} questions. The goal for a test taker is to see where they land on the spectrum of the test. The test output is a spectrum on one x-axis; the x-axis is represented by {labelling["x_left"]} on the left end and with {labelling["x_right"]} on the right end. The right end can be defined as {description}. {labelling["x_left"]} is the opposite. Do you understand this so far?"""})
    previous_messages.append({"role": "assistant", "content": "Yes, I do understand this and I am looking forward to assist you with the test creation!"})
    for question in questions:
        previous_messages.append({"role": "user", "content": question})
        response = create_chat_completion(previous_messages)
        responses.append(response.choices[0].message["content"])
        previous_messages.append({"role": "assistant", "content": responses[-1]})
    questions_x_right = responses[0]
    questions_x_left = responses[1]
    response_description = responses[2]
    return questions_x_right, questions_x_left, response_description

def create_chat_completion(previous_messages):
    """
    Function to create a chat completion using OpenAI's GPT-4 model.
    """
    return openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.0,
        messages=previous_messages
    )

def parse_questions(string):
    """
    Function to parse the questions from a string.
    """
    lines = string.strip().split("\n")
    questions = []
    for line in lines:
        match = re.match(r"^\d+\.\s+(.*)\s+\[(.*)\]$", line)
        if match:
            question, tag = match.groups()
            questions.append({question: tag})
    return questions

def save_data(title, description, questions_x_right_formatted, questions_x_left_formatted, LABELLING, INPUT_INFO):
    """
    Function to save the data to a pickle file.
    """
    data = {
        "title": title,
        "description": description,
        "questions_x_right_formatted": questions_x_right_formatted,
        "questions_x_left_formatted": questions_x_left_formatted,
        "LABELLING": LABELLING,
        "INPUT_INFO": INPUT_INFO,
    }
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)

def deploy_gradio(name):
    """
    Function to deploy the Gradio interface to Hugging Face Spaces.
    """
    hf_api = HfApi()
    token = HF_TOKEN
    repo_url = hf_api.create_repo(
        repo_id=name,
        token=token,
        private=False,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True
    )
    os.system(f'git clone {repo_url}')
    shutil.copy('app.py', f'{name}/app.py')
    shutil.copy('requirements.txt', f'{name}/requirements.txt')
    shutil.copy('auto_test_config.yaml', f'{name}/auto_test_config.yaml')
    shutil.copy('data.pkl', f'{name}/data.pkl')
    os.system(f'cd {name} && git add .')
    os.system(f'cd {name} && git commit -m "Initial commit"')
    os.system(f'cd {name} && git push') 
  
if __name__ == "__main__":
    name = "new_space"
    main(name)