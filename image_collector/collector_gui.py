import os
import shutil

import PySimpleGUI as sg
from PIL import Image
import logging
import time

from util.web_util.contrib import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("./{}.log".format(time.strftime("%Y%m%d%H%M%S")), encoding="utf-8")
file_handler.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)

captcha_image = "./../tmp/captcha.jpeg"
captcha_png = "./../tmp/captcha.png"
captcha_path = "./../tmp"
save_path = "./../resources/data"


def img_process(size=(320, 100)):
    """
    处理验证码图像。
    :param size: tuple;存储大小
    :return: None
    """
    global cookies
    cookies = download_captcha(captcha_path)

    data = Image.open(captcha_image).resize(size, Image.ANTIALIAS)
    data.save(captcha_png)


image = sg.Image(captcha_png)
code = sg.InputText()
layout = [
    [image],
    [code],
    [sg.OK('确定'), sg.Exit('退出')]
]


def record_data(codes):
    """
    将图像移入resources/data,并且写入resource/csv中的csv文件
    :param codes: string or int;验证码
    :return: None
    """
    name = time.strftime("%Y%m%d%H%M%S") + ".jpeg"
    shutil.move(captcha_image, os.path.join(save_path, name))
    with open("./../resources/csv/data.csv", "a", encoding="utf-8") as fout:
        data = "{},{},{}\n".format(name, len(codes), code)
        fout.write(data)


img_process()
with sg.Window('验证码输入窗口', ).Layout(layout) as window:
    while True:
        event, values = window.Read()
        if event == "确定":
            code = values[0]
            if check_captcha(cookies, code):
                record_data(code)
                logger.info("验证码录入,{}.".format(code))
            else:
                logger.info("验证码输入错误.")
            img_process()
            image.Update(captcha_png)
        elif event == "退出":
            break
