from processing.Partners import get_partner_params
from processing.code_storage.Countries import country_to_lang


class Order:

    def __init__(self, conf: dict, msg):
        self.msg = msg
        self.partner = conf.get('partner')
        self.params = get_partner_params(self.partner)
        self.conf = conf

    def replace_order(self):
        with open('processing/partner/orders/' + self.partner + '.php', 'r') as f:
            order_text = f.read()
            self.params.append('sub2')
        for param in self.params:
            if self.conf.get(param):
                order_text = order_text.replace('{' + param + '}', self.conf.get(param))
        order_text = order_text.replace('{success}', self.get_success_path())
        return order_text

    def get_success_path(self):
        success = self.conf.get('success')
        product = self.conf.get('product') or 'Product'
        lang = self.conf.get('lang') or country_to_lang(self.conf.get('country'))
        if success:
            self.msg.append('✅Страница спасибо')
            return f'../tp/{success}/?l={lang}&p={product}&name=" . $_POST[\'name\'] . "&phone=" . $_POST[\'phone\']'
        else:

            return f'../thankyou/index.php?lang={lang}"'
