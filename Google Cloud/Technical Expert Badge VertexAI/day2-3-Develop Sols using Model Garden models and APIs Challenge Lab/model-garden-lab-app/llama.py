import streamlit as st
import os
from logs import write_log_entry

import openai
from google.auth import default, transport

project_id = os.environ['GOOGLE_CLOUD_PROJECT']
region = os.environ['GOOGLE_CLOUD_REGION']

def get_llama_response(models, prompt, output_area):
    """Streams response from Llama model using OpenAI-compatible SDK."""
    credentials, _ = default()

    auth_request = transport.requests.Request()

# TODO Note how the credentials are set

    credentials.refresh(auth_request)


# TODO Note the structure of the base URL 

    client = openai.OpenAI(
        base_url=f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/endpoints/openapi/chat/completions?",
        api_key=credentials.token,
    )

    system_msg = {
        "role": "system",
        "content": (
            "You are the Cymbal Generative AI Chatbot. You provide clear, accurate, "
            "and professional responses. Use step-by-step reasoning if prompted."
        )
    }
    welcome_msg = {"role": "assistant", "content": "Hi! I'm the Cymbal Chatbot. How can I help you?"}
    user_msg = {"role": "user", "content": prompt}
    messages = [system_msg, welcome_msg, user_msg]

    stream = client.chat.completions.create(
# TODO: Pass parameters for model, messages, stream, temperature and max_tokens here
       model = models["Llama"], # TODO your_value here,
       messages = messages, # TODO your_value here,
       stream = True, # TODO your_value here,
       temperature = 0.5, # TODO your_value here,
       max_tokens = 2048 # TODO your_value here,
    )

    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            write_log_entry(models['Llama'], prompt, content)
            response += content
            output_area.markdown(response, unsafe_allow_html=True)
