from processing.code_storage.Countries import get_country_from_iso


class Form:
    SUB_NAME = ['sid5', 'sub_id2', 'sub_id_2', 'sub3', 'sub4', 'sid1', 'sid2', 'sid3', 'country']

    def __init__(self, soup, forms, conf: dict, msg: list):
        self.msg = msg
        self.soup = soup
        self.forms = forms
        self.conf = conf

    def process(self):
        for form in self.forms:
            subs = self.create_subs()
            select = form.find('select')
            if select:
                options = select.find_all('option')
                for option in options:
                    option.extract()
                country = self.conf.get('country')
                if country:
                    new_option = self.soup.new_tag('option', attrs={'value': country})
                    new_option.string = get_country_from_iso(country)
                    select.append(new_option)
            form['action'] = 'order.php'
            form['method'] = 'POST'
            old_subs = form.find_all('input', attrs={'type': 'hidden'})
            for sub in old_subs:
                sub.extract()
            if len(subs) > 0:
                for form_sub in subs:
                    form.insert(0, form_sub)

    def create_subs(self) -> list:
        inputs = [
            self.soup.new_tag('input', attrs=({'name': 'ip', 'value': '{ip}', 'type': 'hidden'})),
            self.soup.new_tag('input', attrs=({'name': 'sub1', 'value': '{subid}', 'type': 'hidden'}))
        ]
        for sub in self.SUB_NAME:
            if not self.conf.get(sub):
                continue
            tag = self.soup.new_tag('input', attrs={'name': sub, 'value': self.conf.get(sub), 'type': 'hidden'})
            inputs.append(tag)
        self.msg.append('✅Настройка формы')
        return inputs
