# AutoTest🧪

AutoTest is a test generator leveraging OpenAI's GPT-4 model. With it, you can create a test that presents users with a set of questions. Based on their answers, users are positioned on a spectrum defined by two opposing concepts. Following the test creation, a Hugging Face space is automatically generated, allowing you to share and distribute your test. It's an innovative way to gauge opinions and positions in a fun, interactive manner! 🎉

## 🛠 Getting Started

Follow these steps to set up AutoTest on your local machine.

### 📌 Prerequisites

Ensure you have Python🐍 installed. [Download Python here](https://www.python.org/downloads/).

### 🔧 Installation

1. **Clone the Repository**: 

   ```
   git clone <repository_link>
   ```

2. **Install Required Packages**:

   ```sh
   pip install -r requirements.txt
   ```

### ⚙ Configuration & Usage

1. **Environment Variables**: Create a `.env` file in the root directory and provide your OpenAI API key and Hugging Face token:

   ```ini
   OPENAI_API_KEY=your_openai_key
   HF_TOKEN=your_huggingface_token
   ```

2. **Run the Script**: Use the following command to generate a test:

   ```sh
   python main.py your_test_name.yaml
   ```

   *Replace `your_test_name.yaml` with the name of your YAML configuration file.*

3. **Customization**: Adjust `auto_test_config.yaml` to modify test parameters.

4. **Access the Test**: Once generated, your test will be available at: `https://huggingface.co/spaces/your_username/your_test_name`

## ✏ Create a Test: Step-by-Step Guide

To create a custom test:

1. **Set Up Configuration File**:
   - Create a `.yaml` file or use a sample from the `example_tests` directory.
   - Adjust configurations as per your requirements.

2. **Test Title**:
   
   ```yaml
   title: "Effective Accelerationism vs. Effective Decelerationism"
   ```

3. **Dimensions**:

   ```yaml
   dimensions: 1
   ```

   *Note: Only single dimensional tests are supported currently. Multi-dimensional support is in the pipeline.*

4. **Define Axis Ends**:

   ```yaml
   x_left: "Effective Decelerationism"
   x_right: "Effective Accelerationism"
   ```

5. **Provide Descriptions**:

   For the right end:

   ```yaml
   description_x_right: |
     Accelerationism is simply...
     ...
     ... a hundred trillion meta-organisms flourishing in the galaxy.
   ```

   For the left end (if it's the opposite):

   ```yaml
   description_x_left: |
     the opposite
   ```

   *For more detailed descriptions, refer to `example_tests`.*

6. **Set Number of Questions**:

   ```yaml
   num_questions: 30
   ```

   *You can choose any number between 10 and 50.*

7. **Generate the Test**:

   Run the script with your YAML file:

   ```sh
   python main.py your_file_name.yaml
   ```

   Upon successful creation, a link to the Hugging Face space will be displayed.

---

Emojis can add a touch of fun to documents and make them more engaging. However, it's important not to overdo it to ensure the content remains professional and easy to read.