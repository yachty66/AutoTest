import os
from dotenv import load_dotenv
from huggingface_hub import HfApi
import shutil

load_dotenv()

hf_token = os.getenv('HF_TOKEN')



def deploy_gradio(name):
    # Initialize the HfApi class
    hf_api = HfApi()

    # Define your token
    token = hf_token

    # Create a new huggingface repo
    repo_url = hf_api.create_repo(
        repo_id=name,
        token=token,
        private=False,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True
    )

    openai_api_key = os.getenv('OPENAI_API_KEY')
    hf_api.set_repo_secret(repo_id=name, token=token, secret_id="OPENAI_API_KEY", secret_value=openai_api_key)
    # Clone the repository
    os.system(f'git clone {repo_url}')

    # Copy the files into the repository
    shutil.copy('app.py', f'{name}/app.py')

    shutil.copy('requirements.txt', f'{name}/requirements.txt')

    shutil.copy('auto_test_config.yaml', f'{name}/auto_test_config.yaml')

    #need to add the secrets openai.api_key = os.getenv('OPENAI_API_KEY') and 

    # Add the files to the repository
    os.system(f'cd {name} && git add .')

    # Commit the changes
    os.system(f'cd {name} && git commit -m "Initial commit"')

    # Push the changes
    os.system(f'cd {name} && git push')

    #am ende müsste da ein laufender 






deploy_gradio("tiombo")