"""These file creates the connector to the openai api"""

import base64
import json
import os
import requests

from dotenv import load_dotenv

from config import settings
from utils.exceptions import OpenAIException

load_dotenv()

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}


def send_online_image_to_openai(query: str, image_url, **kwargs):
    """
    Sends an online image to the openai api with the query.
    If 'system_message' is in kwargs, it will be sent as a system message.
    """

    params = {
        "model": "gpt-4-vision-preview",
        'max_tokens': 300,
        'temperature': 0,
        **kwargs
    }
    params.update(kwargs)

    messages = []  
    if 'system_message' in kwargs:
        system_message = kwargs['system_message']
        messages.append({
            "role": "system",
            "content": [
                {"type": "text",
                 "text": system_message,
                }]
        })
        params.pop('system_message')

    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        ]
    })
    params.update({"messages": messages})

    if 'json_mode' in params:
        params.update({"reponse_format": {"type": "json-object"}})
        if messages[0]["role"] != 'system':
            raise OpenAIException("The first message must be a system message with JSON instructions")
        params.pop('json_mode')
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=params)
        
        if response.json().get('error'):
            print(params)
            raise OpenAIException(response.json()['error'])

    except Exception as e:
        raise OpenAIException(response.json())

    obj = {
        "prompt_tokens": response.json()["usage"]["prompt_tokens"],
        "completion_tokens": response.json()["usage"]["completion_tokens"],
        "total_tokens": response.json()["usage"]["total_tokens"],
        "content": response.json()["choices"][0]["message"]["content"],
    }    

    return obj

def send_local_image_to_openai(query: str, encoded_image, **kwargs):
    """
    Sends an encoded image to the openai api with the query.
    If 'system_message' is in kwargs, it will be sent as a system message.
    """

    params = {
        "model": "gpt-4-vision-preview",
        'max_tokens': 300,
        'temperature': 0,
        **kwargs
    }

    messages = []    
    if 'system_message' in kwargs:
        system_message = kwargs['system_message']
        messages.append({
            "role": "system",
            "content": system_message
        })

    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{encoded_image}"
                }
            }
        ]
    })
    params.update({"messages": messages})

    if 'json_mode' in params:
        params.update({"reponse_format": {"type": "json-object"}})
        if messages[0]["role"] != 'system':
            raise OpenAIException("The first message must be a system message with JSON instructions")
        params.pop('json_mode')

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=params)

    except Exception as e:
        raise OpenAIException(response.json())

    obj = {
        "prompt_tokens": response.json()["usage"]["prompt_tokens"],
        "completion_tokens": response.json()["usage"]["completion_tokens"],
        "total_tokens": response.json()["usage"]["total_tokens"],
        "content": response.json()["choices"][0]["message"]["content"],
    }    

    return obj

def send_query_to_openai(query: str, **kwargs):
    """
    Send a query to openai's chat completion api endpoint
    ----
    Parameters
    model - if not given, it's set to gpt-3.5-turbo
    temperature - if not given, it's set to 0
    max_tokens - if not given, it's set to 300 tokens
    json_mode - if True, it will return the json response. false by default
    
    ----
    
    The parameters like models, temperature, top_p, etc
    can be passed in kwargs
    """
    params = {
        "max_tokens": 300,
        "temperature": 0,
        "json_mode": False,
        "model": "gpt-3.5-turbo-1106"
    }
    params.update(kwargs)

    messages = []
    if 'system_message' in kwargs:
        system_message = kwargs['system_message']
        messages.append({
            "role": "system",
            "content": system_message
        })
        params.pop('system_message')

    messages.append({
        "role": "user",
        "content": query
    })

    params.update({"messages": messages})
    
    if params['json_mode']:
        params.update({"reponse_format": {"type": "json-object"}})
        if messages[0]["role"] != 'system':
            raise OpenAIException("The first message must be a system message with JSON instructions")
    params.pop('json_mode')

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=params
        )

    except Exception as e:
        raise OpenAIException(e)
    
    obj = {
        'completion_tokens': response.json()['usage']['completion_tokens'],
        'prompt_tokens': response.json()['usage']['prompt_tokens'],
        'total_tokens': response.json()['usage']['total_tokens'],
        'content': response.json()['choices'][0]['message']['content'],
        'finish_reason': response.json()['choices'][0]['finish_reason']
    }

    return obj