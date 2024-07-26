from openai import OpenAI
import os

def gpt_model_list():
    client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
    model_list = [model.id for model in client.models.list().data]
    filtered_model_list = [model for model in model_list if model.startswith('gpt')]
    return filtered_model_list