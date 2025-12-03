from bs4 import BeautifulSoup
from processing.code_storage import UtmStorage


class Scripts:
    BAD_SRC_SCRIPT = [
        'leadprofit.js', 'test.js', 'minfobiz', 'shakesland', 'back.js', 'validator.js', 'imask.js', 'ld.js',
        '_.js', 'tag.js', 'fp.js', 'tr.js', 'ua-parser.min.js', 'shakes.js', 'back.js',
        'leadprofit2.js', 'jquery.min.js'
    ]
    BAD_INNER_SCRIPT_WORDS = [
        'history.pushState', 'vitBack', 'minfobiz', 'domonet', 'domonetka', 'IMask',
        'x_order_form', "on('submit', 'form'", 'order-in-progress__popup', 'leadprofit', 'initBacklink', 'land-form'
    ]

    def __init__(self, soup: BeautifulSoup, scripts, conf: dict, msg: list):
        self.msg = msg
        self.soup = soup
        self.scripts = scripts
        self.conf = conf

    def process(self):
        # Removing bad scripts and scripts with bad words
        for script in self.scripts:
            if script.has_attr('src'):
                for bad_src in self.BAD_SRC_SCRIPT:
                    if script['src'].find(bad_src) != -1:
                        script.decompose()
                        break
            if script.string:
                for bad_word in self.BAD_INNER_SCRIPT_WORDS:
                    if bad_word in script.text:
                        script.decompose()
                        break
        self.scroll()
        new_tag = self.soup.new_tag('script', attrs={'src': '../jquery-migration-3.7.1.min.js'})
        self.soup.html.head.append(new_tag)
        self.msg.append('✅ Скролл')

    # Скрипт домонетизации
    def add_domonet(self):
        if self.conf.get('op'):
            utm = UtmStorage.get_op_utm(self.conf.get('op'))
            if not utm:
                self.msg.append('❌Домонетизация')
                return
            self.add_new_tag(attrs={'src': 'https://mixer-track.com/back.js'})
            self.add_new_tag(tag_text=f'''
    document.addEventListener("DOMContentLoaded", function() {{
        window.vitBack("https://mixer-track.com/new?utm_campaign={utm}&utm_source=[SID]&utm_medium=4840", true);
    }});
            ''')
            self.msg.append('✅Домонетка OneProfit')
        if self.conf.get('minfobiz'):
            utm = UtmStorage.get_minfobiz_utm(self.conf.get('minfobiz').upper())
            if not utm:
                self.msg.append('❌Домонетизация')
                return
            new_tag = self.soup.new_tag('script', attrs={'src': f'https://minfobiz.online/js/250/{utm}_0v7.js'})
            self.soup.html.head.append(new_tag)
            self.msg.append('✅Домонетка minfobiz (newsTrends)')

    def add_new_tag(self, attrs=None, tag_text=''):
        if attrs is None:
            attrs = {}
        new_tag = self.soup.new_tag('script', attrs=attrs)
        new_tag.string = tag_text
        self.soup.html.body.append(new_tag)

    def mask(self, pattern: str):

        self.add_new_tag(attrs={'src': 'https://unpkg.com/imask@6.2.2/dist/imask.js'})
        self.add_new_tag(tag_text=f'''
                var elements = document.querySelector('input["name=phone"]');
                for (var i = 0; i < elements.length; i++) {{
                  new IMask(elements[i], {{
                    mask: '{pattern if pattern != True else '000000000000'}',
                  }});
                }}
            ''')
        self.msg.append('✅Маска на номер телефона')

    def anti_double(self):
        self.add_new_tag(tag_text='''
    $( "body" ).on( "submit", 'form', function() {
      const phone = ($('input[name="phone"]', this).val() || '').replace(/[^0-9๐๑๒๓๔๕๖๗๘๙]+/g, '');
      if(getCookie('user_phone_recent') === phone) {
        $('body').append(getTemplate(window.lang || 'en', 'recently_confirmed'));
        return false;
      }
      if(getCookie('user_phone_in_progress') === phone) {
        $('body').append(getTemplate(window.lang || 'en', 'in_progress'));
        return false;
      }
      setCookie('user_phone_recent', phone, 60 * 60);//60 minutes
      setCookie('user_phone_in_progress', phone, 21 * 24 * 60 * 60);//21 day
    });
      function getCookie(name) {
            name = name.replace(/([.*+?^=!:${}()|[\\]\\/\\\\])/g, '\\\\$1');
            const regex = new RegExp('(?:^|;)\\\\s?' + name + '=(.*?)(?:;|$)','i'),
                match = document.cookie.match(regex);
            return match && unescape(match[1]);
      }
      function setCookie(cname, cvalue, expireSeconds) {
            var d = new Date();
            d.setTime(d.getTime() + (expireSeconds * 1000));
            var expires = "expires=" + d.toUTCString();
            document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
      }
    function getTemplate(lang, msg) {
     const phone_support = msg === 'in_progress' ? window.duplicate_order_phone : '';
        const main_msg = msg === 'in_progress' ? window.order_in_progress : window.order_recently_confirmed;
     const styles = '<style scoped> #order-in-progress__popup {\
      position: fixed;\
      left: 50%;\
      top: 50%;\
      z-index: 200;\
      transform: translateX(-50%) translateY(-50%);\
       background: white;\
       box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);\
       font-family: inherit;\
       font-size: 18px;\
       text-align: center;\
       display: flex;\
       justify-content: center;\
       align-items: center;\
       flex-direction: column;\
       max-width: 400px;\
       width: 100%;\
       height: auto;\
       border-radius: 5px;\
       padding: 30px;\
      }\
      #order-in-progress__popup button {\
       background: #f57d02;\
       border-radius: 3px;\
       border: none;\
       text-transform: uppercase;\
       padding: 10px 20px;\
       margin-top: 20px;\
       font-weight: 700;\
       color: white;\
       font-size: 19px;\
       font-family: inherit;\
      }\
      #order-in-progress__popup span {\
       width: 100%;\
      }\
      @media screen and (max-width: 479px) {\
       #order-in-progress__popup {\
        max-width: calc(90vw - 40px);\
        padding: 15px 20px;\
       }\
      }</style>';
     return styles + '<div id="order-in-progress__popup" ' +
      'style="position: fixed; z-index: 2147483647;" >' +
      '<span>Order is not accepted!</span>' +
      '<button' +
      'style="background: #f57d02; border: 0px;margin-top: 30px; width: auto;"' +
      'onclick="document.body.removeChild(document.querySelector(\\'#order-in-progress__popup\\'))">You was ordering!</button>' +
     '</div>';
    }
        ''')
        # self.msg.append('✅Антидубль')

    def validator(self):
        self.add_new_tag(tag_text='''
  $(function () {
        $(document).on('submit', 'form', function() {
            $(this).find("button").prop('disabled',true);
            $(this).find("input[type=submit]").remove();
        });
        $('[name="name"]').on('input change', function(){
            var val = $(this).val();
            $(this).val(val.replace(/[0-9+]/g, ''));
        });
        $('[name="phone"]').on('input change', function(e){
            var val = $(this).val();
            $(this).val(val.replace(/[A-zА-яіїЁё ]/g, ''));
            $(e.currentTarget).attr('pattern', '[0-9+]{6,}')
        });
  });
        ''')
        # self.msg.append('✅Валидатор формы')

    def anchor(self):
        self.add_new_tag(tag_text=f'''
        $("a").click(function(e) {{
        e.preventDefault();
        var destination = $('#form').offset().top - 200;
        jQuery("html:not(:animated),body:not(:animated)").animate({{scrollTop: destination}}, 800);
        return false;
        }})
        ''')
        # self.msg.append('✅Якорь')

    def scroll(self):
        self.add_new_tag(tag_text=f'''
            window.addEventListener('DOMContentLoaded', () => {{
                const links = document.querySelectorAll('a');
                const domain = window.location.hostname;  // Получаем текущий домен

                links.forEach(link => {{
                    link.href = link.href.replace('https:///', `https://` + domain + `/`);
                }});
            }});
            window.addEventListener("DOMContentLoaded", function() {{
                let maxScroll = 0;
                window.addEventListener("scroll", function() {{
                    let scrollTop = window.scrollY;
                    let windowHeight = window.innerHeight;
                    let documentHeight = document.documentElement.scrollHeight;
                    let scrollPercent = (scrollTop / (documentHeight - windowHeight)) * 100;
                    if (scrollPercent > maxScroll) {{
                        maxScroll = scrollPercent;
                    }}
                }});

            let links = document.querySelectorAll("a");
            let url = links[0].href;
            links.forEach(function(link) {{
                link.addEventListener("click", function(event) {{
                    event.preventDefault();
                    url += (url.includes("?") ? "&" : "?") + "scroll=" + Math.round(maxScroll);
                    window.location.href = url;
                }});
            }});
            }});
        ''')
    
