import requests
import os

__all__ = ['download_captcha', 'check_captcha']


def download_captcha(save_path):
    """
    下载验证码并保存。
    :param save_path: string;保存的位置.
    :return: string;图像的cookies
    """
    try:
        doc = requests.get(CAPTCHA_URL)
        image_raw = doc.content
        with open(os.path.join(save_path, "captcha.jpeg"), "wb") as fin:
            fin.write(image_raw)
        return doc.headers['Set-Cookie']
    except requests.ConnectionError:
        return None


LOGIN_PAGE_URL = "http://jwk.lzu.edu.cn/academic/common/security/login.jsp"
CAPTCHA_URL = "http://jwk.lzu.edu.cn/academic/getCaptcha.do"
CAPTCHA_CHECK_URL = "http://jwk.lzu.edu.cn/academic/checkCaptcha.do?captchaCode="
SECURE_CHECK_URL = "http://jwk.lzu.edu.cn/academic/j_acegi_security_check"


def check_login(cookies, code, user, passwd):
    """
    目前被弃用，用于检测是否登陆成功。
    :param cookies: string;从check_captcha中获得
    :param code: string or int;验证码
    :param user: string;用户名
    :param passwd: string;密码
    :return: bool;是否登录成功
    """
    secure_check_header = {
        "Host": "jwk.lzu.edu.cn",
        "Connection": "keep-alive",
        "Content-Length": "64",
        "Cache-Control": "max-age=0",
        "Origin": "http://jwk.lzu.edu.cn",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://jwk.lzu.edu.cn/academic/common/security/login.jsp",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7",
    }
    sect = secure_check_header.copy()
    sect['Cookie'] = cookies.split(';')[0]
    data = "j_username={}&j_password={}&j_captcha={}".format(user, passwd, code)
    doc = requests.post(SECURE_CHECK_URL, headers=sect, data=data, allow_redirects=False)
    if (len(doc.cookies) > 0):
        return True
    else:
        return False


def check_captcha(cookies, code):
    """
    用于检测输入的验证码是否正确。
    :param cookies: string;cookies
    :param code: int or string;验证码
    :return: bool;是否正确
    """
    check_captcha_header = {
        "Host": "jwk.lzu.edu.cn",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Accept": "text/plain, */*; q=0.01",
        "Origin": "http://jwk.lzu.edu.cn",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "DNT": "1",
        "Referer": "http://jwk.lzu.edu.cn/academic/common/security/login.jsp",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7",
    }
    ct = check_captcha_header.copy()
    ct['Cookie'] = cookies
    tmp_doc = requests.post(CAPTCHA_CHECK_URL + "{}".format(code), headers=ct)
    if tmp_doc.text == 'true':
        return True
    else:
        return False
