# There are two possible choices for LLM right now  "llm": ["llama", "chatglm-6b"]

CONFIG = {
    "llm_list": ["llama"],
    "llm_url": {
        "llama": "http://10.16.69.141:9001/",
        "chatglm-6b": "http://10.16.69.201:8000/"
    },
    "input_tag_types": ["input", "textarea", "contenteditable"],
    "print_styles": {
        "global_info_prompt": "rgb(127,255,0)",
        "global_info_content": "rgb(0,128,0)",
        "local_info_prompt": "rgb(135,206,250)",
        "local_info_content": "rgb(0,255,255)",
        "tag_info_prompt": "rgb(205,92,92)",
        "tag_info_content": "rgb(220,20,60)",
        "role_play": "rgb(218,165,32)",
        "chain_of_thought": "rgb(147,112,219)"
    },
    "distance": 0
}
