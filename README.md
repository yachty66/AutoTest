# PersAI📋

PersAI📋 is your AI-powered test generation agent. Craft tests that probe users with a series of questions and, based on their responses, place them on a spectrum between two contrasting concepts. Upon test creation, a Hugging Face space is seamlessly generated, allowing for easy sharing and distribution.

## 🛠 Getting Started

Here's a quick guide to get PersAI📋 up and running on your local setup.

### 📌 Prerequisites

- Python🐍: Ensure you have it installed on your machine.

### 🔧 Installation

1. **Clone the Repository**: 
   ```
   git clone https://github.com/yachty66/PersAI.git
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

### ⚙ Configuration & Usage

1. **Environment Variables**: Set up a `.env` file in the root directory with your OpenAI API key and Hugging Face token:
   ```ini
   OPENAI_API_KEY=your_openai_key
   HF_TOKEN=your_huggingface_token
   ```

2. **Run the Script**: 
   ```sh
   python main.py your_test_name.yaml
   ```
   *Remember to replace `your_test_name.yaml` with your specific YAML configuration filename.*

3. **Access Your Test**: Post-creation, find your test at: `https://huggingface.co/spaces/your_username/`

## ✏ Create a Test: A Step-by-Step Guide

Here's how to craft your custom test:

1. **Setup**: Either use a `.yaml` sample from `example_tests` or craft a new one. Modify configurations as needed.

2. **Title Your Test**: 
   ```yaml
   title: "Effective Accelerationism vs. Effective Decelerationism"
   ```

3. **Dimensions**:
   ```yaml
   dimensions: 1
   ```
   *Presently, only one-dimensional tests are supported. Multi-dimensional functionality is in the works.*

4. **Label Your Axes**: 
   ```yaml
   x_left: "Effective Decelerationism"
   x_right: "Effective Accelerationism"
   ```

5. **Provide Descriptive Content**:

   For the right end:
   ```yaml
   description_x_right: |
     Accelerationism is simply...
     ...
     ... meta-organisms flourishing in the galaxy.
   ```

   For the left end (if opposite):
   ```yaml
   description_x_left: |
     the opposite
   ```
   *For nuanced descriptions, peek at the `example_tests`.*

6. **Determine Question Count**: 
   ```yaml
   num_questions: 30
   ```
   *Pick any number from 10 to 50.*

7. **Generate!**: 
   ```sh
   python main.py your_file_name.yaml
   ```
   Once created, you'll be provided with a Hugging Face space link.

### Sample Tests & Demonstration 

**Check out these test spaces**:
- [Effective Accelerationism vs. Effective Decelerationism](https://huggingface.co/spaces/yachty66/XSLAYdGsVMD5NbU2jQQdKeEkQJOMxm)
- [Capitalism vs. Communism](https://huggingface.co/spaces/yachty66/ZcXPB8U5MhGHOVhJF2ipGix5X40CgU?logs=build)
- [INTP vs. INTJ](https://huggingface.co/spaces/yachty66/j3l1ENYk2VOqzhx1bmWHEvMt6LWyjP?logs=build)

**Want to see PersAI📋 in action?**  
🎥 [Watch the DEMO!](https://x.com/MaxHager66/status/1703228131241292252?s=20)