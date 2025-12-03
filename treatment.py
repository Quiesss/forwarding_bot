from bs4 import BeautifulSoup
from processing.Atags import ATag
from processing.Forms import Form
from processing.Page import Page
from processing.Scripts import Scripts
from processing.code_storage.Offers import check_offer_name
import re

from processing.partner.Order import Order


def remove_old_php_code(text: bytes):
    return str(re.sub('<\\?php([\\s\\S]+?)\\?>', '', text.decode('utf-8')))


def parse_conf(msg_capture) -> dict:
    if msg_capture is None:
        return {}
    conf = {}
    msg_split = msg_capture.split('\n')
    for line in msg_split:
        param = line.split(':')
        if len(param) > 1:
            conf[param[0].strip()] = ''.join(param[1:]).strip()
        else:
            conf[param[0].strip()] = True
    return conf


class IndexParse:

    def __init__(self, index_text, conf: dict, msg: list):
        self.msg = msg
        try:
            self.conf = conf
            self.page = BeautifulSoup(remove_old_php_code(index_text), "lxml")
            self.forms = self.page.find_all('form')
            self.scripts = self.page.find_all('script')
            self.a_tags = self.page.find_all('a')
        except Exception as e:
            raise Exception('Что-то с версткой, ' + str(e))

    def tuning(self):
        if self.page.html is None:
            raise Exception('Поломан &lt;html&gt; тег')
        if self.page.html.head is None:
            raise Exception('Поломан &lt;head&gt; тег')
        if self.page.html.body is None:
            raise Exception('Поломан &lt;body&gt; тег')

        # Form(self.page, self.forms, self.conf, self.msg).process()
        ATag(self.page, self.a_tags, self.conf, self.msg).process()
        Scripts(self.page, self.scripts, self.conf, self.msg).process()
        Page(self.page, self.conf).process()
        return self.get_php_code(self.conf[0], self.conf[1]) + self.text_tuning()

    def text_tuning(self):
        page = str(self.page.prettify())
        return page

    def get_php_code(self, cobeklo: str, value: str):
        if cobeklo is None or value is None:
            self.msg.append('❌cobeklo, ')
            return ''
        self.msg.append('✅ ' + cobeklo + ' = ' + value)
        return f'''<?php if ($_GET["{cobeklo}"] != '{value}') {{ echo '<script>window.location.replace("https://www.google.com/"); document.location.href="https://www.google.com/" </script>'; exit; }} ?>'''


def make_order_file(conf, msg):
    order = Order(conf, msg)
    return order.replace_order()
