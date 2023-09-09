import gradio as gr

"""def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    input_block = gr.inputs.CheckboxGroup(choices=["USA", "Japan", "Pakistan"])
    demo.add(input_block)

demo.launch()"""
def greet(name):
    #here i am going to do calcs later 
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    #need to set a different label here
    #input_block = gr.inputs.CheckboxGroup(choices=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"])
    input_block = gr.inputs.Radio(choices=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"])
    output = gr.Textbox(label="This is going to be the plot later")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet, inputs=input_block, outputs=output, api_name="Submit")

demo.launch()