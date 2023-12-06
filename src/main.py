import sys

import selenium
from selenium.common import ElementNotInteractableException

from html_parser import HTMLParser
from datatype import SelectedTag
from model_adpter import fill_in_the_box

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

INPUT_TAG_INFO = None
LOCAL_CONTEXT_INFO = None
GLOBAL_CONTEXT_INFO = None

load_wait_short = 2
load_wait_middle = 4
load_wait_long = 6

# TODO: 将input tag不是规则的情况也考虑进来


def main(file_name,tag_str):
    global INPUT_TAG_INFO, LOCAL_CONTEXT_INFO, GLOBAL_CONTEXT_INFO

    # file_name = sys.argv[1]

    parser = HTMLParser(file_name)

    soup = parser.soup
    # tag_str = ' '.join(sys.argv[2:])

    # need to bridge with selenium here
    selected_tag = SelectedTag(tag_str, soup)

    if soup:
        print("selected_tag: \n", selected_tag)

        # Get Global Information
        GLOBAL_CONTEXT_INFO = parser.get_global_context_info()

        # Get Local Information
        INPUT_TAG_INFO = parser.get_input_tag_info(selected_tag)

        # Get Local Information
        LOCAL_CONTEXT_INFO = parser.get_local_context_info(selected_tag)

        text_return=fill_in_the_box(input_tag_info=INPUT_TAG_INFO,
                        global_context_info=GLOBAL_CONTEXT_INFO,
                        local_context_info=LOCAL_CONTEXT_INFO)

        generated_input=get_input_text(text_return)
        return generated_input

    else:
        print("Parsing failed")


def get_input_text(text_return):
    generated_text = text_return
    last_colon_index_CN = text_return.rfind('：')
    last_colon_index_EN=text_return.rfind(':')
    last_colon_index=max(last_colon_index_CN,last_colon_index_EN)

    # last_colon_index = text_return.rfind(':')

    # 找到冒号后的第一个换行符的索引
    first_newline_index_after_colon = text_return.find('\n', last_colon_index)
    # 找到冒号后的第二个换行符的索引
    second_newline_index_after_colon = text_return.find('\n', first_newline_index_after_colon + 1)

    # 检查是否找到了冒号和两个换行符
    if last_colon_index != -1 and first_newline_index_after_colon != -1 and second_newline_index_after_colon != -1:
        # 获取冒号后到第二个换行符之间的内容
        generated_text = text_return[first_newline_index_after_colon + 1:second_newline_index_after_colon]
    elif last_colon_index != -1 and first_newline_index_after_colon != -1:
        # 获取冒号后到第一个换行符之间的内容
        generated_text = text_return[last_colon_index + 1:]
    elif last_colon_index != -1:
        generated_text = text_return[last_colon_index + 1:]

    # 使用正则表达式去掉双引号和方括号
    generated_text = re.sub(r'["\[\]]', '', generated_text)

    # 分割字符串，并只保留第一部分
    if '、' in generated_text:
        generated_text = generated_text.split('、')[0]

    if ',' in generated_text:
        generated_text = generated_text.split(',')[0]

    # 去掉句号
    generated_text = generated_text.replace('。', '')

    # 去掉尾部的句号（如果存在）
    if generated_text.endswith('.'):
        generated_text = generated_text[:-1]

    return generated_text.strip()


def getChromeBrowser():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    browser = webdriver.Chrome(options=chrome_options)
    return browser


def openBrowserWebsite():
    browser = getChromeBrowser()
    browser.implicitly_wait(load_wait_short)
    print('web title:', end='')
    print(browser.title)
    html = browser.execute_script("return document.documentElement.outerHTML")
    filename = 'example.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    # 查找页面上的所有输入框
    input_boxes = browser.find_elements(By.TAG_NAME, "input")
    # 遍历输入框
    for input_box in input_boxes:
        # 检查输入框是否可用
        if input_box.is_enabled():
            print("***********************************************")
            input_box_html = input_box.get_attribute('outerHTML')
            # print(f"HTML: {input_box_html}\n")

            # 生成输入内容
            generated_input = main('example.html',input_box_html)
            print(generated_input)
            # 填入生成的内容
            try:
                input_box.send_keys(generated_input)
            except ElementNotInteractableException:
                print()



if __name__ == "__main__":
    openBrowserWebsite()

