from dataclasses import dataclass
import bs4
from bs4 import BeautifulSoup
from config import CONFIG

input_tag_types = CONFIG["input_tag_types"]
distance = CONFIG["distance"]


class SelectedTag:
    type: str
    tag_str: str
    attr: {}
    soup_obj: bs4.element.Tag

    def __init__(self, tag_str: str, soup):
        for keyword in input_tag_types:
            if f"<{keyword}" in tag_str:
                self.type = keyword
                break

        if self.type is None:
            raise ValueError("Selected tag is not a valid input tag.")

        self.tag_str = tag_str
        self.attr = self.html_to_dict()
        self.soup_obj = soup.find(name=self.type, attrs=self.attr)

    def __repr__(self):
        return f"<{self.type} {self.attr}>"

    def html_to_dict(self):

        # 创建BeautifulSoup对象并解析HTML
        soup_temp = BeautifulSoup(self.tag_str, 'html.parser')

        # 提取属性名和属性值，分组为字典
        attrs = soup_temp.input.attrs
        grouped_dict = {}
        for attr, value in attrs.items():
            if attr:
                grouped_dict[attr] = value

        # print(grouped_dict)

        return grouped_dict


# three kinds of information mentioned in the ICSE 24 paper


class InputTagInfo:
    ## Parser relevant attributes
    tag: bs4.element.Tag
    attr: {}
    tag_type: str  # the sort of input tag: input/textarea/select/contenteditable

    ## HTML element attributes
    ## TODO: add more attributes
    id: str
    name: str = None
    clazz: str = None
    type: str = None
    placeholder: str = None
    aria_label: str = None
    max_length: int = None
    min_length: int = None
    size: int = None

    def __init__(self, tag):
        self.tag = tag  # beautifulsoup tag object
        self.attr = self.tag.attrs  # attribute dict
        self.input_tag_type = self.tag.name  # input / textarea / select / contenteditable

        self.id = self.attr['id'] if 'id' in self.attr and self.attr['id'] != "" else None

        self.name = self.attr['name'] if 'name' in self.attr and self.attr['name'] != "" else None

        self.clazz = self.attr['class'] if 'class' in self.attr and self.attr['class'] != "" else None

        self.type = self.attr['type'] if 'type' in self.attr and self.attr['type'] != "" else None

        if 'placeholder' in self.attr:
            self.placeholder = self.attr['placeholder']
        elif 'data-active-placeholder' in self.attr:
            self.placeholder = self.attr['data-active-placeholder']
        else:
            self.placeholder = None

        self.aria_label = self.attr['aria-label'] if 'aria-label' in self.attr and self.attr[
            'aria-label'] != "" else None

        self.max_length = int(self.attr['maxlength']) if 'maxlength' in self.attr and self.attr[
            'maxlength'] != "" else None

        self.min_length = int(self.attr['minlength']) if 'minlength' in self.attr and self.attr[
            'minlength'] != "" else None

        self.size = int(self.attr['size']) if 'size' in self.attr and self.attr['size'] != "" else None

    def get_tag_info_prompt(self):
        prompt = f"This input is used to "
        if self.id is not None and len(self.id) > 0:
            prompt += f"{self.id}"
        if self.placeholder is not None and len(self.placeholder) > 0:
            prompt += f", which indicates {self.placeholder}"
        return prompt

    def get_constraint(self):
        prompt = "The input have some constraints: "
        constraint = ""
        if self.max_length is not None:
            constraint += f"Has a max length of {self.max_length} characters"
        if self.min_length is not None:
            constraint += f", Has a min length of {self.min_length} characters"
        if self.size is not None:
            constraint += f", Has a size of={self.size}"

        if constraint != "":
            prompt += constraint
            return prompt
        else:
            return constraint

    def get_category(self):
        # TODO: 需要给文本生成任务做分类
        prompt = "The input box on the web page is used to "
        return prompt + "query"

    def __repr__(self):
        pass


@dataclass
class GlobalContextInfo:
    head: str = None
    title: str = None


class LocalContextInfo:
    text_database: {}

    def __init__(self, text_database):
        self.text_database = text_database

    def __repr__(self):
        return str(self.text_database)

    # TODO: 需要根据文本任务设置不同的context,目前按全局设置返回
    def get_context(self):
        content = ""

        for i in self.text_database.keys():
            if self.text_database[i] <= distance:
                # 删除i中的标点符号
                content += i.replace(",.", "") + ","

        return content
