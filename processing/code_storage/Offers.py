
def check_offer_name(text: str):
    offers = [
        'Eremax', 'Eronex', 'Erogan', 'Erasmin', 'Reduslim', 'W-Loss', 'Love-X', 'Vipromac', 'Cannabis Oil',
        'CannabisOil', 'Hondrofrost'
    ]
    clear_text = text.lower().split()
    for word in offers:
        if len(word.split()) > 1:
            first = word.split()[0] in clear_text
            continue
        if word.lower() in clear_text:
            return word
    return None
