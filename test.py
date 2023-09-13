"""import gradio as gr

def greet(input_one, input_two):
    # Check if all questions have been answered
    if input_one is None or input_two is None:
        raise gr.Error("Cannot divide by zero!")
        #return "Error: Please answer all questions."
    
with gr.Blocks() as demo:
    title = gr.Markdown("# This is the title of my application")
    description = gr.Markdown("This is a description of my application")
    disclaimer = gr.Markdown("**Disclaimer: This is a disclaimer for my application**")
    #need to set a different label here
    question = "Some based question"
    input_block_one = gr.inputs.Radio(choices=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], label=question)
    input_block_two = gr.inputs.Radio(choices=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"], label=question)
    inputs = [input_block_one, input_block_two]
    output = gr.Textbox(label="This is going to be the plot later")
    greet_btn = gr.Button("Submit")
    greet_btn.click(fn=greet, inputs= [labelling] + inputs, outputs=output, api_name="Submit")

demo.launch()"""
"""from random import shuffle

combined_questions = [1,2,3,4,5]
shuffle(combined_questions)

print(combined_questions)"""


print(5 / 2 )


