# Project Title

This project is a test generator that uses OpenAI's GPT-4 model to create a test with a set of questions. The test output is a spectrum on one x-axis, represented by two opposing concepts. The user's responses to the questions determine where they land on this spectrum.

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

## Code Overview

The main functions in the code are:

- `main(name)`: This is the main function that runs the program. It loads the configuration, generates the test, saves the data, and deploys the test to Hugging Face Spaces.

- `load_config()`: This function loads the configuration from a YAML file.

- `create_one_dimension_test(description, num_questions, labelling)`: This function creates a test with one dimension.

- `parse_questions(string)`: This function parses the questions from a string.

- `deploy_gradio(name)`: This function deploys the Gradio interface to Hugging Face Spaces.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.
License

This project is licensed under the MIT License - see the LICENSE.md file for details.