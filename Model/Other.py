from selenium.webdriver.remote.webelement import WebElement
from .Render import BASE_URL
from .Render import SiteGenericModel

class SendMessageUserModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()
    self.CHECK_LINKS = False
    self.EXPECTED_CONTENTS.extend([
            [
                'div.info > a',
                'text',
                None,
                'Вернуться к объявлению'
            ],
            [
                'div.info > a',
                WebElement.get_attribute,
                'href',
                model.ad_url
            ],
            [
                'div.common_table_sides > div.common_table_top_cell',
                'text',
                None,
                'Связаться с разместителем объявления но. ' + model.ad_n
            ],
            [
                'div.common_table_sides > div:nth-of-type(2)',
                'text',
                None,
                'Это сообщение пойдет разместителю объявления но. ' + model.ad_n + ' ' + model.AD_CONTENT['title'] + '.'
            ],
        ])
    self.EXPECTED_COUNTS = {
            'div.common_table_sides input'    : 4,
            'div.common_table_sides textarea' : 1
        }

class SendMessageUserRegisteredModel(SendMessageUserModel):
  def __init__(self, model, msg_input):
    super().__init__(model)
    self.EXPECTED_CONTENTS.extend([
            [
                'div.common_table_sides > div:nth-of-type(4) > input',
                WebElement.get_attribute,
                'value',
                msg_input.EMAIL
            ],
            [
                'div.common_table_sides > div:nth-of-type(5) > input',
                WebElement.get_attribute,
                'value',
                msg_input.NAME
            ],
        ])

class SentMessageUserModel(SiteGenericModel):
  def __init__(self, model):
    super().__init__()
    self.EXPECTED_CONTENTS.extend([
            [
                'div.common_table_sides > div.common_table_top_cell',
                'text',
                None,
                'Сообщение отправлено'
            ],
            [
                'div.common_table_sides > h3:nth-of-type(1)',
                'text',
                None,
                'Сообщение отправлено разместителю объявления. Спасибо.'
            ],
            [
                'div.common_table_sides > h3:nth-of-type(2) > a',
                'text',
                None,
                'Вернуться к объявлению ' + model.ad_n + ' (' + model.AD_CONTENT['title'] + ')'
            ],
            [
                'div.common_table_sides > h3:nth-of-type(2) > a',
                WebElement.get_attribute,
                'href',
                model.ad_url
            ],
        ])

