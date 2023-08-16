
def get_partner_params(partner=None):
    partners = {
        'shakes': ['url', 'country', 'offerId', 'streamCode'],
        'lemonad': ['offerId'],
        'leadbit': ['streamCode', 'country'],
        'm1': ['offerId', 'country'],
        'leadreaktor': ['offerId', 'country'],
        'clickhouse': ['price', 'currency', 'locale', 'sub2', 'offerId'],
        'terraleads': ['stream', 'offerId', 'country'],
        'affstar': ['stream', 'country'],
        'skylead': ['flow', 'offerId', 'country'],
        'lucky': ['apikey', 'stream', 'country'],
        'rocketprofit': ['stream'],
        'aray': ['stream', 'country', 'price', 'offerId'],
        'metacpa': [],
        'kmabiz': ['stream', 'country'],
        'aff1': ['target', 'flow', 'country'],
        'LeadTrade': [],
        'offerstore': ['offerId', 'flow'],
        'leadrock': ['stream'],
        'leadbusters': [],
        'adcombo': ['stream', 'offerId', 'price', 'country'],
        'drcash': ['flow'],
        'whocpa': [],
        'affscale': [],
        'xleads': [],
        'webvork': [],
        'everad': ['stream'],
        'cashfactories': ['flow', 'offerId'],
        'trafficlight': []
    }
    if not partner:
        return partners.keys()
    return partners.get(partner)
