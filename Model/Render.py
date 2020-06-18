from selenium.webdriver.remote.webelement import WebElement
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get('BASE_URL')

class SiteGenericModel(object):
  def __init__(self):
    self.STRICT = True
    self.CHECK_LINKS = True
    self.URL = BASE_URL
    self.EXPECTED_CONTENTS = [
            [
                'div.site_title a',
                'text',
                None,
                'Название сайта'
            ],
            [
                'div#footer',
                'text',
                None,
                '(c) Название сайта (domain.com)'
            ],
        ]
    self.EXPECTED_COUNTS = {}

class ErrorModel(SiteGenericModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL + '/obyavlenia/999-doesnt-exist.html'
    self.META_TITLE = 'Ошибка'
    self.EXPECTED_CONTENTS.append([
            '#wrapper > div.common_table_sides > div.common_table_top_cell',
            'text',
            None,
            'Ошибка'
        ])

class HomeModel(SiteGenericModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL
    self.META_TITLE = 'Доска объявлений - Все регионы'
    self.META_DESC = 'Бесплатная доска объявлений. Бесплатное и удобное размещение объявлений без регистрации. Русские объявления в России, Украине, Белорусии, прочих странах СНГ, США, Канаде, Европе.'
    self.META_KW = 'объявления, доска объявлений, бесплатная доска объявлений, россия, украина, снг, сша, канада, авто, автозапчасти, работа, вакансии, знакомства, недвижимость, аренда, коммерческая недвижимость'
    self.EXPECTED_CONTENTS.extend([
            [
                '#selected_area',
                'text',
                None,
                'Все регионы [Поменять]'
            ],
            [
                'div.index_category > div > a',
                'text',
                None,
                'Автомобили, транспорт'
            ],
            [
                'div.index_category > div > a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/cat/10-0/avtomobili-transport.html'
            ],
            [
                '#areas_table ul a',
                'text',
                None,
                'Австралия'
            ],
            [
                '#areas_table ul a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/cat/0-1279/avstraliya-vse-razdely.html'
            ]
        ])
    self.EXPECTED_COUNTS = {
            'div.home_featured_oby' : 8,
            'div.index_column'      : 4
        }

class RussiaHomeModel(HomeModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL + '/cat/0-595/rossiya-vse-razdely.html'
    self.META_TITLE = 'Доска объявлений - Россия'
    self.EXPECTED_CONTENTS.append([
                '.site_title',
                'text',
                None,
                'Название сайта - Россия'
            ])
    self.EXPECTED_CONTENTS[2][3] = 'Россия [Поменять]'
    self.EXPECTED_CONTENTS[4][3] = BASE_URL + '/cat/10-595/rossiya-avtomobili-transport.html'
    self.EXPECTED_CONTENTS[5][3] = 'Алтайский край'
    self.EXPECTED_CONTENTS[6][3] = BASE_URL + '/cat/0-600/altajskij-kraj-vse-razdely.html'

class MoscowHomeModel(HomeModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL + '/cat/0-596/moskva-vse-razdely.html'
    self.META_TITLE = 'Доска объявлений - Россия >> Москва'
    self.EXPECTED_CONTENTS.append([
                '.site_title',
                'text',
                None,
                'Название сайта - Москва'
            ])
    self.EXPECTED_CONTENTS[2][3] = 'Россия >> Москва [Поменять]'
    self.EXPECTED_CONTENTS[4][3] = BASE_URL + '/cat/10-596/moskva-avtomobili-transport.html'
    self.EXPECTED_CONTENTS[5][3] = 'Запад'
    self.EXPECTED_CONTENTS[6][3] = BASE_URL + '/cat/0-1322/zapad-vse-razdely.html'

class CategoryModel(SiteGenericModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL + '/cat/10-0/avtomobili-transport.html'
    self.META_TITLE = 'Название сайта - Автомобили, транспорт.'
    self.META_DESC = 'Раздел Автомобили, транспорт - автомобили, гаражи, парковка, мотоциклы, мопеды, водный транспорт, ищу попутчика, разное. Доска объявлений.'
    self.META_KW = 'автомобили, автомобили объявления, транспорт, транспорт объявления, объявления, доска объявлений, бесплатная доска объявлений, Название сайта, объявление, разместить объявление'
    self.EXPECTED_CONTENTS.extend([
            [
                '#selected_area',
                'text',
                None,
                'Все регионы [Поменять]'
            ],
            [
                'h1',
                'text',
                None,
                'Автомобили, транспорт'
            ],
            [
                'ul.subcat_columns > li > a',
                'text',
                None,
                None,
                'NotNone'
            ],
            [
                'ul.subcat_columns > li > a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/cat/35-0/avtomobili-transport/avtomobili.html'
            ],
            [
                'td.main_cell > a',
                'text',
                None,
                None,
                'NotNone'
            ],
            [
                'div.page_index a',
                'text',
                None,
                '2'
            ],
            [
                'div.page_index a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/cat/10-0/avtomobili-transport/page-2.html'
            ],
            [
                '#areas_table ul a',
                'text',
                None,
                'Австралия'
            ],
            [
                '#areas_table ul a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/cat/10-1279/avstraliya-avtomobili-transport.html'
            ]
        ])
    self.EXPECTED_COUNTS = {
            'ul.subcat_columns > li > a' : 6,
            'tbody > tr'                 : 75
        }

class RussiaCategoryModel(CategoryModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL + '/cat/10-595/rossiya-avtomobili-transport.html'
    self.META_TITLE = 'Название сайта - Россия. Автомобили, транспорт.'
    self.META_DESC = 'Россия. Раздел Автомобили, транспорт - автомобили, гаражи, парковка, мотоциклы, мопеды, водный транспорт, ищу попутчика, разное. Доска объявлений.'
    self.META_KW = 'автомобили, автомобили объявления, транспорт, транспорт объявления, россия, россия объявления, объявления, доска объявлений, бесплатная доска объявлений, Название сайта, объявление, разместить объявление'
    self.EXPECTED_CONTENTS[2][3] = 'Россия [Поменять]'
    self.EXPECTED_CONTENTS[3][3] = 'Россия - Автомобили, транспорт'
    self.EXPECTED_CONTENTS[5][3] = BASE_URL + '/cat/35-595/rossiya-avtomobili-transport/avtomobili.html'
    self.EXPECTED_CONTENTS[8][3] = BASE_URL + '/cat/10-595/rossiya-avtomobili-transport/page-2.html'
    self.EXPECTED_CONTENTS[9][3] = 'Алтайский край'
    self.EXPECTED_CONTENTS[10][3] = BASE_URL + '/cat/10-600/altajskij-kraj-avtomobili-transport.html'

class MoscowCategoryModel(CategoryModel):
  def __init__(self):
    super().__init__()
    self.URL = BASE_URL + '/cat/10-596/moskva-avtomobili-transport.html'
    self.META_TITLE = 'Название сайта - Москва. Автомобили, транспорт.'
    self.META_DESC = 'Москва. Раздел Автомобили, транспорт - автомобили, гаражи, парковка, мотоциклы, мопеды, водный транспорт, ищу попутчика, разное. Доска объявлений.'
    self.META_KW = 'автомобили, автомобили объявления, транспорт, транспорт объявления, москва, москва объявления, объявления, доска объявлений, бесплатная доска объявлений, Название сайта, объявление, разместить объявление'
    self.EXPECTED_CONTENTS[2][3] = 'Россия >> Москва [Поменять]'
    self.EXPECTED_CONTENTS[3][3] = 'Москва - Автомобили, транспорт'
    self.EXPECTED_CONTENTS[5][3] = BASE_URL + '/cat/35-596/moskva-avtomobili-transport/avtomobili.html'
    self.EXPECTED_CONTENTS[8][3] = BASE_URL + '/cat/10-596/moskva-avtomobili-transport/page-2.html'
    self.EXPECTED_CONTENTS[9][3] = 'Запад'
    self.EXPECTED_CONTENTS[10][3] = BASE_URL + '/cat/10-1322/zapad-avtomobili-transport.html'

class InteractionPageModel(object):
  def __init__(self):
    self.URLS = [
                  BASE_URL + '/send_message.php',
                  BASE_URL + '/send_message.php?ad=1786618',
                  BASE_URL + '/user.php?action=ad_create',
                  BASE_URL + '/user.php?action=ad_create&c[]=37&c1=10&c2=35&c3=37',
                  BASE_URL + '/user.php?action=user_login',
                  BASE_URL + '/user.php',
                  BASE_URL + '/report_abuse.php',
                  BASE_URL + '/report_abuse.php?ad=1786618',
              ]