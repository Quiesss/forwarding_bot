

def get_minfobiz_utm(label):
    if not label:
        return 'undefined'
    utm = {
        'DE': '5183DE01',
        'IQ': '5175IQ01',
        'ID': '5177ID01',
        'BE': '5198BE01',
        'FR': '5188FR01',
        'CO': '5181CO01',
        'CH': '5178CH01',
        'GH': '5190GH01',
        'DZ': '5184DZ01',
        'CZ': '5182CZ01',
        'GR': '5191GR01',
        'BG': '5166BG01',
        'CI': '5179CI01',
        'ES': '5130ES01',
        'AR': '5141AR01',
        'CL': '5180CL01',
        'AT': '5145AT01',
        'GT': '5128GT01',
        'AL': '5138AL01',
        'EC': '5185EC01',
        'HU': '5129HU01',
        'HR': '5193HR01',
        'AE': '5137AE01',
        'BD': '5159BD01',
        'BA': '5147BA01',
        'IN': '5176IN01',
        'EG': '5187EG01',
        'CR': '5127CR01',
        'IT': '5173IT01',
        'KE': '5171KE01',
        'LT': '5200LT01',
        'LV': '5168LV01',
        'MA': '5194MA01',
        'MK': '5165MK01',
        'MX': '5163MX01',
        'NG': '5161NG01',
        'PE': '5160PE01',
        'PL': '5157PL01',
        'PT': '5156PT01',
        'RO': '5154RO01',
        'RS': '5153RS01',
        'SA': '5133SA01',
        'SG': '5150SG01',
        'SI': '5149SI01',
        'SK': '5148SK01',
        'SN': '5146SN01',
        'TH': '5143TH01',
        'TN': '5142TN01',
        'TR': '5140TR01',
        'ZA': '5139ZA01',
        'BO': '5367BO01',
    }
    return utm.get(label)


def get_op_utm(label):
    if not label:
        return None
    utm = {
        '100V': 54763,
        '101G': 53813,
        '103P': 54866,
        '106Y': 54810,
        '10M': 53478,
        '12S': 54489,
        '13B': 53705,
        '14V': 53686,
        '16D': 54650,
        '17O': 54650,
        '23E': 53738,
        '24A': 54704,
        '31N': 53622,
        '37K': 53689,
        '39V': 53685,
        '45D': 54352,
        '48S': 53420,
        '50K': 53700,
        '51E': 53458,
        '54I': 53977,
        '56A': 54705,
        '59D': 53429,
        '5S': 53895,
        '60M': 54789,
        '78I': 53427,
        '79R': 53463,
        '83A': 53461,
        '85Y': 54817,
        '86D': 53978,
        '98D': 53710,
        '99R': 54620,
        '52V': 55036,
        '3D': 55083,
        '80A': 55290,
        '40K': 56264,
        '116R': 56737,
        '84T': 56855,
        '42K': 56861,
        '123N': 57419,
        '9M': 57494,
        '62V': 53389,
        '122A': 57693,
        '118S': 57714,
        '113V': 58187,
        '108D': 58539,
        '136V': 59207,
        '135U': 59738,
        '124V': 59761,
        '126I': 62071
    }
    return utm.get(label)
