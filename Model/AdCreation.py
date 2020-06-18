from selenium.webdriver.remote.webelement import WebElement
from .Render import BASE_URL
from .Render import SiteGenericModel
import re

class AdPageModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()
    self.EXPECTED_CONTENTS.extend([
            [
                'div.oby_details_body > h1',
                'text',
                None,
                model.AD_CONTENT['title']
            ],
            [
                'div.oby_details_body > p',
                'text',
                None,
                model.AD_CONTENT['detail']
            ],
            [
                'div.oby_details_body',
                'text',
                None,
                model.EMAIL,
                'NotIn'
            ],
            [
                'div.oby_details_body > div:nth-of-type(1)',
                'text',
                None,
                'Регион: ' + model.AREA_SELECTS[5][1],
            ],
            [
                'div.oby_details_body > div:nth-of-type(2)',
                'text',
                None,
                'Телефон: ' + model.AD_CONTENT['pub_phone1'] + ', ' + model.AD_CONTENT['pub_phone2'],
            ],
            [
                'div.oby_details_body > div:nth-of-type(3) > a',
                'text',
                None,
                model.AD_CONTENT['url'],
            ],
            [
                'div.oby_details_body > div:nth-of-type(3) > a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/go.php?n=' + model.ad_n,
            ],
            [
                'div.oby_details_body > div.send_message_oby > a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/send_message.php?ad=' + model.ad_n,
            ],
            [
                'div.oby_box_right > div.frame > div.cell_embosed2:nth-of-type(1)',
                'text',
                None,
                'Объявление но. ' + model.ad_n,
            ],
            [
                'div.oby_box_right > div.frame > div.cell_embosed2:nth-of-type(4) > a',
                'text',
                None,
                'Сообщить другу',
            ],
            [
                'div.oby_box_right > div.frame > div.cell_embosed2:nth-of-type(4) > a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/tell_friend.php?ad=' + model.ad_n,
            ],
            [
                'div.oby_box_right > div.frame > div.cell_embosed2:nth-of-type(6) > a',
                'text',
                None,
                'Сообщить о нарушении',
            ],
            [
                'div.oby_box_right > div.frame > div.cell_embosed2:nth-of-type(6) > a',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/report_abuse.php?ad=' + model.ad_n,
            ],
        ])

class AdPreviewModel(AdPageModel):
  def __init__(self, model):
    super().__init__(model)
    self.CHECK_LINKS = False

class AdPublishedModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()

    self.EXPECTED_CONTENTS = [
            [
                'div.info',
                'text',
                None,
                ''
            ],
        ]

    if model.m == '1':
        self.EXPECTED_CONTENTS[0][3] = \
                "Объявление будет опубликовано после проверки модератора.\nВНИМАНИЕ: Оплата любой услуги позволяет обойти модерацию."
    elif model.m == '2':
        self.EXPECTED_CONTENTS[0][3] = \
                "Мы выслали на вашу электронную почту (" + model.EMAIL + ") письмо-подтверждение. Вам необходимо открыть письмо и перейти по специальной ссылке, чтобы подтвердить получение письма. Если вы не получите письмо в течение 15 минут, проверьте что оно не попало в Спам.\nОплата любой платной услуги также может служить подтверждением вашего адреса эл. почты."
    elif model.m == '3':
        self.EXPECTED_CONTENTS[0][3] = \
                "Ваше объявление опубликовано. Смотрите его здесь:\n" + model.AD_CONTENT['title'] + "\nНиже вы можете заказать дополнительные услуги."

class AdFeaturesEditModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()
    self.EXPECTED_CONTENTS = [
            [
                'form#ad_features_edit_form > div.common_table_sides > div.common_table_top_cell',
                'text',
                None,
                'Дополнительные услуги'
            ],
            [
                'form#ad_features_edit_form tr:nth-of-type(1) > td:nth-of-type(2)',
                'text',
                None,
                model.ad_n + ' ' + model.AD_CONTENT['title']
            ],
            [
                'form#ad_features_edit_form tr:nth-of-type(7) > td:nth-of-type(2) > select > option:nth-of-type(3)',
                'text',
                None,
                '30'
            ],
            [
                'form#ad_features_edit_form tr:nth-of-type(7) > td:nth-of-type(2) > select > option:nth-of-type(3)',
                WebElement.get_attribute,
                'value',
                '30'
            ],
            [
                'form#ad_features_edit_form tr:nth-of-type(7) > td:nth-of-type(2) > select > option:nth-of-type(3)',
                WebElement.is_selected,
                None,
                True
            ]
        ]
    self.EXPECTED_COUNTS = {
            'form#ad_features_edit_form tr'              : 7,
            'form#ad_features_edit_form select > option' : 6
        }

class AdFeaturesEditedModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()
    self.EXPECTED_CONTENTS = [
            [
                'form#payment_method_form > div.common_table_sides > div.common_table_top_cell',
                'text',
                None,
                'Обзор заказа'
            ],
            [
                'form#payment_method_form tr:nth-of-type(1) > td:nth-of-type(2)',
                'text',
                None,
                model.ad_n + ' ' + model.AD_CONTENT['title']
            ],
            [
                'form#payment_method_form tr:nth-of-type(2) > td:nth-of-type(2)',
                'text',
                None,
                'Расположение вверху списка\nРасположение на домашней странице'
            ],
            [
                'form#payment_method_form tr:nth-of-type(3) > td:nth-of-type(2)',
                'text',
                None,
                '14 дней'
            ],
            [
                'div.payment_options > div:nth-of-type(3)',
                self._strip_parentheses,
                None,
                'Яндекс деньги '
            ],
            [
                'div.payment_options > input:nth-of-type(3)',
                WebElement.get_attribute,
                'value',
                'yandex'
            ],
            [
                'div.payment_options > input:nth-of-type(3)',
                WebElement.is_selected,
                None,
                True
            ],
            [
                'div.payment_options > div:nth-of-type(4)',
                self._strip_parentheses,
                None,
                'Мобильный счет '
            ],
            [
                'div.payment_options > input:nth-of-type(4)',
                WebElement.get_attribute,
                'value',
                'freekassa'
            ],
            [
                'div.payment_options > input:nth-of-type(4)',
                WebElement.is_selected,
                None,
                False
            ],
            [
                'div.payment_options > div:nth-of-type(5)',
                self._strip_parentheses,
                None,
                'QIWI '
            ],
            [
                'div.payment_options > input:nth-of-type(5)',
                WebElement.get_attribute,
                'value',
                'freekassa'
            ],
            [
                'div.payment_options > input:nth-of-type(5)',
                WebElement.is_selected,
                None,
                False
            ]
        ]
    self.EXPECTED_COUNTS = {
            'form#payment_method_form tr' : 5,
            'div.payment_options input'     : 9
        }

  def _strip_parentheses(self, elem):
      preg = re.compile('\(.+\)')
      str = re.sub(preg, '', elem.text)
      return str

class PaymentPageModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()
    self.CHECK_LINKS = True
    self.EXPECTED_CONTENTS = [
            [
                'div.common_table_sides > div.common_table_top_cell',
                'text',
                None,
                'Оплата'
            ],
            [
                'div.common_table_sides > a:nth-of-type(1)',
                'text',
                None,
                'выбрать другой метод оплаты'
            ],
            [
                'div.common_table_sides > a:nth-of-type(1)',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/user.php?action=ad_features_edited&n[]=' + model.ad_n + '&featured=1&home_page=1&period=14'
            ],
            [
                'div.common_table_sides > a:nth-of-type(2)',
                'text',
                None,
                'изменить заказ'
            ],
            [
                'div.common_table_sides > a:nth-of-type(2)',
                WebElement.get_attribute,
                'href',
                BASE_URL + '/user.php?action=ad_features_edit&n[]=' + model.ad_n + '&featured=1&home_page=1&period=14'
            ],
            [
                'div.order_form > div > b',
                'text',
                None,
                model.expected_price
            ],
            [
                'div.order_form form',
                WebElement.get_attribute,
                'action',
                'https://www.free-kassa.ru/merchant/cash.php'
            ],
            [
                'div.order_form form > button',
                'text',
                None,
                'Оплатить'
            ],
            [
                'div.order_form form > input:nth-of-type(3)',
                WebElement.get_attribute,
                'name',
                'oa'
            ],
            [
                'div.order_form form > input:nth-of-type(3)',
                WebElement.get_attribute,
                'value',
                model.expected_price
            ],
        ]
    self.EXPECTED_COUNTS = {
            'div.order_form form > input' : 6
        }
