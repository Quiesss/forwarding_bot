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

    PRICE_ENUM = 'USD|usd|\\$|EUR|eur|\\€|doll|DOLL|EURO|euro|pld|PLD|pln|PLN|zł|sol'
    CROSS_EMOJI = '❌'
    OK_EMOJI = '✅'

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
        # product = self.conf.get('product')
        # price = self.conf.get('price')
        page = str(self.page.prettify())
        # if product:
        #     old_product = self.conf.get('old_p') or check_offer_name(self.page.text)
        #     if old_product is not None:
        #         page, count_offer_name = re.subn(old_product, product, page)
        #         if count_offer_name > 0:
        #             self.msg.append(self.OK_EMOJI + f'Поменял название оффера в {count_offer_name} местах')
        #         else:
        #             self.msg.append(self.CROSS_EMOJI + 'Не смог найти оффер в тексте')
        # if price:
        #     page, replace_count = re.subn(f'\\b\\d+(?:\\.\\d+)?\\s?({self.PRICE_ENUM})', price, page)
        #     if replace_count > 0:
        #         self.msg.append(self.OK_EMOJI + f'Поменял цену в {replace_count} местах')
        #     else:
        #         self.msg.append(self.CROSS_EMOJI + 'Не смог найти цены в тексте')

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
