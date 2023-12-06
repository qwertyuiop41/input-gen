import json

import requests

from config import CONFIG

LLM_url = CONFIG["llm_url"]["chatglm-6b"]


def request_GLM(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": f'{prompt}',
        "history": []
    }

    response = requests.post(LLM_url, headers=headers, data=json.dumps(data))
    return response.json()['response']

