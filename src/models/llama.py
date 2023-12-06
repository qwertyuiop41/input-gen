from config import CONFIG

from gradio_client import Client

LLM_url = CONFIG["llm_url"]["llama"]


def request_Llama(prompt):
    client = Client(LLM_url)
    result = client.predict(
        prompt,
        api_name="/predict"
    )
    return result
