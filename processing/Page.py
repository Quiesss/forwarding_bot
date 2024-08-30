from bs4 import BeautifulSoup


class Page:

    def __init__(self, soup: BeautifulSoup, conf: dict):
        self.soup = soup
        self.conf = conf

    def process(self):
        self.remove_iframe()
        # self.add_meta()

    def remove_iframe(self):
        for iframe in self.soup.find_all('iframe'):
            iframe.extract()

    # def add_meta(self):
    #     if self.conf.get('cobeklo'):
    #         meta = self.soup.find('meta', attrs={'name': 'msapplication'})
    #         if meta:
    #             meta.extract()
    #         meta_tag = self.soup.new_tag(
    #             'meta',
    #             attrs={
    #                 'content': '0x' + self.conf.get('cobeklo'),
    #                 'name': 'msapplication'
    #             })
    #         self.soup.html.head.append(meta_tag)
