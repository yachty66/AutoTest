# AutoTest

This project is a test generator that uses OpenAI's GPT-4 model to create a test with a set of questions. The test output is a spectrum on one x-axis, represented by two opposing concepts. The user's responses to the questions determine where they land on this spectrum. Once the test is generated a huggingface space with the test is generated where i.e. it will be publicly available and you can share the test with others or do whatever you want with it.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download Python here.

### Installing

1. Clone the repository to your local machine.
2. Install the required packages using pip:

```sh
pip install -r requirements.txt
```

### Usage

1. Set up your environment variables. You need to provide your OpenAI API key and Hugging Face token. You can do this in a .env file:

```python
OPENAI_API_KEY=your_openai_key
HF_TOKEN=your_huggingface_token
```

2. Run the main.py script with the name of your test as an argument:

```python
python main.py your_test_name
```

3. The script will generate a test based on the configuration in auto_test_config.yaml. You can modify this file to customize your test.

4. The generated test will be deployed to Hugging Face Spaces. You can view it at https://huggingface.co/spaces/your_username/your_test_name.

## Example

Following a step by step approach for how it would like if you would create a test by yourself. For creating a test everything whats necessary to fill out is the scaffold of a yaml file. examples of such .yaml files can be found in the `example_tests` directory.

1. Start with creating a .yaml and give her any name you want. The best is if you just copy and paste a sample yaml file from `example_tests` into the root directory.

1. In the next step give the test a name. The name should be representive for the test you wanna create. Lets say we choose the following test title:

```yaml
title: "Effective Accelerationism vs. Effective Decelerationism"
```

2. In the next step the dimensions of the test need to be set. For now the only possible option to set is `1`:

```yaml
dimensions: 1
```

I.e. the test exists of results which can be mapped on one x-axis i.e. it exist two possible outputs. later at 🧪AutoTest we plan to support also with two and N dimensions, so stay tuned for this!

3. In the next step you need to define the the name of each x-axis end. In our case we choose the left end of the x-axis to be named Effective Decelerationism and the right end Effective Accelerationism:

```yaml
x_left: "Effective Decelerationism"
x_right: "Effective Accelerationism"
```

4. in the next step step it is necessary to provide the description for the test. The logic here is that the description needs to be provided for both ends of the axis. first the description for the right side:

```yaml
description_x_right: |
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
  9. HUMANS HAVE AGENCY RIGHT NOW. WE CAN AFFECT THE ADVENT OF THE INFLECTION IN THIS PROCESS.
  10. Effective Accelerationism, e/acc, is a set of ideas and practices that seek to maximize the probability of the technocapital singularity, and subsequently, the ability for emergent consciousness to flourish. There is much work to be done in defining cause areas, motivations, and philosophy. Please join us on #eacc twitter, and let's work towards a hundred trillion meta-organisms flourishing in the galaxy.
```

and than for the left site. in the case the left side is just the opposite what is mostly the case for one dimensional tests than you have to do the following:

```yaml
description_x_left: |
  the opposite
```

if you want to add more context you can do this but keep it short similar to the `description_x_right` example. see the examples in `example_tests` for that.

5. The last configuration step is to set the number of questions. this can be a number between 10 and 50 both numbers inclusive. this setting defines of how many questions the test will exist off. In the following example we set this number to 30:

```yaml
num_questions: 30
```

Alright now everything is defined and the app for creating the test is ready to be called. You need to call the python script together with the name of your yaml file you just created. in this example we are calling the yaml file `accelerationism_vs_decelerationism.yaml` so we are going to run the following command:

`python main.py accelerationism_vs_decelerationism.yaml`

It takes up to a few minutes until the test is created but once the test is done and deployed you see a link to the hugginface space for the link. you can use this test now to embedd it on your website or just share it like it is to your friends. 