from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image, ImageDraw
import time

# 启动WebDriver
driver = webdriver.Chrome()
driver.get("http://example.com")  # 替换为目标网址

# 找到所有输入框
input_boxes = driver.find_elements(By.TAG_NAME, "input")

# 选择并点击第一个输入框
if input_boxes:
    selected_input_box = input_boxes[0]
    selected_input_box.click()

    # 获取输入框的位置和尺寸
    location = selected_input_box.location
    size = selected_input_box.size

    # 等待页面加载和交互
    time.sleep(2)

    # 截屏
    screenshot_file = "/path/to/screenshot.png"  # 替换为你想保存截图的路径
    driver.save_screenshot(screenshot_file)

    # 使用Pillow框出输入框
    image = Image.open(screenshot_file)
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        [(location['x'], location['y']),
         (location['x'] + size['width'], location['y'] + size['height'])],
        outline="red",
        width=2
    )

    # 保存修改后的截图
    image.save("/path/to/modified_screenshot.png")  # 替换为你想保存修改后的截图的路径

# 关闭WebDriver
driver.quit()
