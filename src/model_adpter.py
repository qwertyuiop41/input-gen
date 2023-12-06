from rich.console import Console
from rich.theme import Theme

from config import CONFIG

theme = CONFIG["print_styles"]
custom_theme = Theme(theme)
console = Console(theme=custom_theme)

LLM_LIST = CONFIG["llm_list"]


def fill_in_the_box(input_tag_info, global_context_info, local_context_info):
    prompt = generate_prompt(input_tag_info, global_context_info, local_context_info)
    print(prompt)

    if "chatglm-6b" in LLM_LIST:
        from models.chatglm import request_GLM as query
        result_glm = query(prompt)

        # print("***********************************************")
        print("chatglm-6b REPLY: \n", result_glm)
        return result_glm

    if "llama" in LLM_LIST:
        from models.llama import request_Llama as query
        result_llama = query(prompt)

        # print("***********************************************")
        print("llama REPLY: \n", result_llama)
        return result_llama


def generate_prompt(input_tag_info, global_context_info, local_context_info):
    # TODO：这里的 category 会被用于生成上下文信息，但是目前还没有实现

    category = input_tag_info.placeholder

    role_play_prompt = \
        ("You are an end-to-end web tester."
         "Input text for the box on the web page you are viewing.")

    # print("***********************************************")
    # print("role_play_prompt: \n", role_play_prompt)
    #
    # print("***********************************************")
    structured_output_prompt = "Just give me the input without explanation."
    # print("structured_output_prompt: \n", structured_output_prompt)

    # print("***********************************************")
    global_header_prompt = f"You are browsing the 华为云 web application and the page you are viewing has the web page title: {global_context_info.title}."
    # print("global_header_prompt: \n", global_header_prompt)

    # print("***********************************************")
    task_category_prompt = f"{input_tag_info.get_category()}."
    # print("task_category_prompt: \n", task_category_prompt)

    # print("***********************************************")
    tag_info_prompt = f"{input_tag_info.get_tag_info_prompt()}."
    # print("tag_info_prompt: \n", tag_info_prompt)

    # print("***********************************************")
    tag_info_constraint_prompt = f"{input_tag_info.get_constraint()}"
    # print("tag_info_constraint_prompt: \n", tag_info_constraint_prompt)

    # print("***********************************************")
    local_context_prompt = f"These text is placed next to the input box: {local_context_info.get_context()}"
    # print("local_context_prompt: \n", local_context_prompt)

    pattern = role_play_prompt + \
              structured_output_prompt + \
              global_header_prompt + \
              task_category_prompt + \
              tag_info_prompt + \
              tag_info_constraint_prompt + \
              local_context_prompt

    return pattern

# def generate_prompt_debugging(input_tag_info, global_context_info, local_context_info):
#     category = "query"
#     role_play_prompt = \
#         ("You are an end-to-end web tester."
#          "You can generate input text for the text box on the web you are viewing based on the information on the web.")
#
#     pattern_global = f"This is [{theme['global_info_content']}]{global_context_info.head}[/] web application and the page you are viewing with web title [{theme['global_info_content']}]{global_context_info.title}[/]."
#
#     pattern_cat = f"The input box on the web page is used to [{theme['global_info_content']}]{category}[/]."
#
#     pattern_input_tag_info = "This input is about "
#
#     pattern_input_tag_info += f"[{theme['tag_info_content']}] "
#
#     pattern_input_tag_info += f"{input_tag_info.placeholder} "
#     # for value in input_tag_info.attr.values():
#     #     pattern_input_tag_info = pattern_input_tag_info + str(value) + ","
#     # # pattern_input_tag_info = f""
#     # # for key, value in local_inform.items():
#     # #     pattern_input_tag_info = pattern_input_tag_info + f"The {key} of the input box is {value}. "
#     # pattern_input_tag_info = pattern_input_tag_info[:len(pattern_input_tag_info) - 1]
#     # if len(input_tag_info.attr) >= 2:
#     #     # 将句子以最后一个 "and" 为分隔符，进行分割
#     #     parts = pattern_input_tag_info.rsplit(",", 1)
#     #
#     #     # 将除了最后一个部分以外的所有 "and" 替换为逗号 ","
#     #     pattern_input_tag_info = parts[0] + " and " + parts[1]
#     pattern_input_tag_info += f"[/]. "
#
#     pattern_local_context_info = "Please generate the input with the context"
#
#     pattern_local_context_info += f"[{theme['local_info_content']}]"
#
#     pattern_local_context_info += str(local_context_info)
#
#     pattern_local_context_info += f"[/]. "
#
#     pattern_input = "No explanation! Just give me the text input!"
#     # pattern = role_play_prompt + example + pattern_global + pattern_cat + pattern_input_tag_info + pattern_input
#     pattern = role_play_prompt + pattern_global + pattern_cat + pattern_input_tag_info + pattern_local_context_info + pattern_input
#
#     #
#     console.print(role_play_prompt, style="role_play", end=" ")
#     console.print(pattern_global, style="global_info_prompt", end=" ")
#     console.print(pattern_cat, style="global_info_prompt", end=" ")
#     console.print(pattern_input_tag_info, style="tag_info_prompt", end=" ")
#     console.print(pattern_local_context_info, style="tag_info_prompt", end=" ")
#     console.print(pattern_input, style="chain_of_thought")
#
#     def remove_contents_in_brackets(text):
#         result = ""
#         inside_brackets = False
#
#         for char in text:
#             if char == '[':
#                 inside_brackets = True
#             elif char == ']':
#                 inside_brackets = False
#             elif not inside_brackets:
#                 result += char
#
#         return result
#
#     pattern = remove_contents_in_brackets(pattern)
#
#     return pattern
