import os

from bs4 import BeautifulSoup
from selenium import webdriver

from config import CONFIG
from datatype import InputTagInfo, GlobalContextInfo, LocalContextInfo

DISTANCE_BOUND = CONFIG['distance']


class HTMLParser:
    url: str
    file_path: str
    soup: BeautifulSoup
    html: str

    def __init__(self, filename):
        self.file_path = filename
        self.soup = None
        self.html = None
        self.text_tree = None

        if os.path.isfile(self.file_path):

            # 文件存在，读取文件内容
            with open(filename, 'r', encoding='utf-8') as file:
                self.html = file.read()

            self.soup = BeautifulSoup(self.html, 'html.parser')


        else:
            raise Exception("The file doesn't exist.")

        self.remove_css()

        self.remove_js()

        self.soup.prettify()

    def remove_css(self):
        # 移除 <style> 标签及其内容
        for style_tag in self.soup.find_all('style'):
            style_tag.decompose()

    def remove_js(self):
        # 移除 <script> 标签及其内容
        for script_tag in self.soup.find_all('script'):
            script_tag.decompose()

    @staticmethod
    def get_input_tag_info(selected_tag):
        return InputTagInfo(tag=selected_tag.soup_obj)

    @staticmethod
    def get_local_context_info(selected_tag):

        text_database = {}  # key = text , value = distance

        # start from the selected tag and explore the subtree (top-down from the root)

        def search_context(element, distance):
            if distance > DISTANCE_BOUND:
                return

            if element.parent and distance <= DISTANCE_BOUND:
                parent_text = element.parent.get_text(separator=",", strip=True)
                current_text_database = parent_text.split(",")

                if len(parent_text) > 0:
                    has_new_text = False
                    for text in current_text_database:
                        if text not in text_database.keys():
                            text_database[text] = distance
                            has_new_text = True
                    if has_new_text:
                        search_context(element.parent, distance + 1)
                    else:
                        search_context(element.parent, distance)

                else:
                    search_context(element.parent, distance)

        selected_node = selected_tag.soup_obj

        search_context(selected_node, 0)

        return LocalContextInfo(text_database)

    # 从整个html文件的头部、标题获取全局信息
    def get_global_context_info(self):
        # global_inform = {}
        soup = self.soup
        html_head = soup.head.get_text(strip=True)
        html_title = soup.title.get_text(strip=True)
        # global_inform['head'] = html_head
        # global_inform['title'] = html_title
        print("Global Information:")
        print("HTML头部:", html_head)
        print("HTML标题:", html_title)
        return GlobalContextInfo(html_head, html_title)
