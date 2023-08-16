
class ATag:

    def __init__(self, soup, a_tags, conf: dict, msg: list):
        self.msg = msg
        self.soup = soup
        self.atags = a_tags
        self.conf = conf

    def process(self):
        new_href = self.conf.get('a') if self.conf.get('a') else ''
        for a_tag in self.atags:
            a_tag['href'] = new_href
            a_tag['target'] = ''
