from selenium.webdriver.remote.webelement import WebElement
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get('BASE_URL')
USER_EMAIL = os.environ.get('USER_EMAIL')
USER_PASSW = os.environ.get('USER_PASSW')
IMAGE_CONTROL = os.environ.get('IMAGE_CONTROL')

class GenericInput(object):
  def _get_title(self):
    title_words = 'лорем ипсум долор сит амет'.split(' ')
    random.shuffle(title_words)
    title = ' '.join(title_words)
    return title.capitalize()

  def _get_detail(self):
    detail_paragraphs = [
        'Лорем ипсум долор сит амет, но ипсум яуаеяуе про. Еа вим аудиам молестиае перципитур, ад елит ассуеверит еум. Убияуе рецусабо патриояуе вис ех, еа дебет патриояуе сед, ин мел омнис доценди. Ан хис веро миним молестиае, ан мел еирмод аццусам. Еум дебет ерудити ид, апериам лабитур петентиум еу иус.',
        'Унум инани номинави ут мел, ут утамур нецесситатибус еам, тота лаборе витуператорибус сеа ет. Хис солута омиттам витуператорибус ид, еа легимус вертерем глориатур нец. Амет сцрипта импедит усу цу, либрис делецтус меа но. Ет дицант сцрипсерит вел, ест легимус яуалисяуе еа. Симул цонсул не усу, цу при меис фиерент луптатум.',
        'Ид хис одио еффициантур, утамур сусципит опортеат ин еос. Ид еум иисяуе алияуам, дуо цетерос деленити но, ностро аппареат хис ид. Утрояуе цонцлудатуряуе еу нец, ат вел нулла аудиам нусяуам. Диам фиерент цонсулату ат мел, мел импедит платонем тхеопхрастус ад, амет путант сед ат. Дицам пондерум патриояуе ест не.',
        'Сит цу цасе зрил. Либрис еирмод апериам те вис, еум стет опортере цонсеяуат не. Еу ессе видерер нец, сеа те натум солеат аудире. Малис елеифенд но хис, ид еиус рецтеяуе неглегентур сеа. Суас дицерет еурипидис вис ан, не меа еяуидем менандри патриояуе. Вих поссит цаусае неглегентур те.',
        'Персецути тхеопхрастус но нец, ассум регионе диспутатиони еа дуо, сит ин суас пробо улламцорпер. Еи нам вери цонгуе алияуид, нец мунере семпер садипсцинг ут, плацерат инвенире цонституто хас ат. Вис еним темпор оффициис еу, еу малорум тинцидунт ехпетендис усу, убияуе персеяуерис ех при. Алияуам омнесяуе ратионибус ад вел, ут дуо адмодум цорпора аццоммодаре. Мелиус цомпрехенсам иус ид. Ут цонгуе пхилосопхиа меа, вим витуперата цомпрехенсам не, еиус апеириан ехпетенда цу вел. Еос долор суавитате ат, ут мовет аудиам пондерум хас, меи видит пхаедрум цонсеяуунтур не.'
    ]
    random.shuffle(detail_paragraphs)
    return '\n\n'.join(detail_paragraphs)

class AdCreationInput(GenericInput):
  def __init__(self):
    self.URL = [
            BASE_URL + '/user.php?action=ad_create',
            BASE_URL + '/user.php?action=ad_create&c%5B%5D=37&c1=10&c2=35&c3=37&B1=%D0%9F%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B8%D1%82%D1%8C',
            BASE_URL + '/user.php?action=ad_edit&previewed=yes&n=',
            BASE_URL + '/user.php',
            BASE_URL + '/user.php?action=ad_features_edit&n=',
            BASE_URL + '/user.php?action=ad_features_edited&n%5B%5D=',
            BASE_URL + '/obyavlenia/',
        ]
    self.CAT_SELECTS = [
            [1, 'Автомобили, транспорт', '10', True],
            [2, 'Автомобили', '35', True],
            [3, 'Легковые автомобили', '37', False]
        ]
    self.AREA_SELECTS = [
            [1, 'Россия', '595', True],
            [2, 'Санкт-Петербург', '598', False],
            [1, 'Все регионы', '0', False],
            [1, 'Россия', '595', True],
            [2, 'Москва', '596', True],
            [3, 'Центр', '1316', False]
        ]
    self.EMAIL = USER_EMAIL
    self.AD_CONTENT = {
            'title'         : self._get_title(),
            'detail'        : self._get_detail(),
            'email'         : self.EMAIL,
            'email_confirm' : self.EMAIL,
            'pub_phone1'    : '+8-903-123-45-67',
            'pub_phone2'    : '+8(903) 456-12-37',
            'url'           : 'https://www.somewebsite.com',
            'google_map'    : '',
            'youtube_video' : '',
            'image_upload[0][1]' : '',
            'image_upload[0][2]' : '',
            'image_upload[0][3]' : '',
            'image_upload[0][4]' : '',
            'image_control' : IMAGE_CONTROL,
            'user_agreement': True
        }

class AdCreationRegisteredInput(AdCreationInput):
  def __init__(self):
    super().__init__()

    self.URL.append(BASE_URL + '/user.php?action=user_login')

    del self.AD_CONTENT['email']
    del self.AD_CONTENT['email_confirm']

class LoginInput(object):
  def __init__(self):
    self.URL = [
        BASE_URL + '/user.php?action=user_login',
        BASE_URL + '/user.php?action=user_log_off',
    ]
    self.LOGIN_CREDENTIALS = {
        'email'    : USER_EMAIL,
        'password' : USER_PASSW
    }

class SendMessageUserInput(GenericInput):
  def __init__(self):
    self.EMAIL = USER_EMAIL
    self.NAME  = 'Yuri'
    self.MESSAGE_CONTENT = {
            'message'       : self._get_detail(),
            'email'         : self.EMAIL,
            'name'          : self.NAME,
            'image_control' : IMAGE_CONTROL
        }

class SendMessageUserRegisteredInput(SendMessageUserInput):
  def __init__(self):
    super().__init__()
    del self.MESSAGE_CONTENT['email']
    del self.MESSAGE_CONTENT['name']