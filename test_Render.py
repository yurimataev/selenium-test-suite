import unittest
from selenium import webdriver
from selenium import common
from SiteTestGeneric import SiteTestGeneric
import Model.Render as Render
from pprint import pprint
#from webdriverdownloader import ChromeDriverDownloader

class NavigationTest(SiteTestGeneric):

    def test_home_page(self):
        self._fetch_check_against_model(Render.HomeModel())

    def test_russia_home_page(self):
        self._fetch_check_against_model(Render.RussiaHomeModel())

    def test_moscow_home_page(self):
        self._fetch_check_against_model(Render.MoscowHomeModel())

    def test_category_page(self):
        model = Render.CategoryModel()
        self._fetch_check_against_model(model)
        self._test_breadcrumbs(model.URL)

    def test_russia_category_page(self):
        model = Render.RussiaCategoryModel()
        self._fetch_check_against_model(model)
        self._test_breadcrumbs(model.URL)

    def test_moscow_category_page(self):
        model = Render.MoscowCategoryModel()
        self._fetch_check_against_model(model)
        self._test_breadcrumbs(model.URL)

    def test_ad_page_basic(self):
        model = Render.SiteGenericModel()
        self.driver.get(model.URL)
        elem = self.driver.find_element_by_css_selector('div.home_featured_oby > a')
        url = elem.get_attribute('href')
        model.URL = url

        self._check_link_works(model.URL)
        self._fetch_check_against_model(model)
        self._test_breadcrumbs(model.URL)

    def test_interaction_pages_basic(self):
        for url in Render.InteractionPageModel().URLS:
            self._check_link_works(url)

    def test_file_not_found(self):
        self._fetch_check_against_model(Render.ErrorModel())

    def _test_breadcrumbs(self, url):
        self.driver.get(url)
        elems = self.driver.find_elements_by_css_selector('.category_info a')

        links = []
        for a in elems:
            links.append(a.get_attribute('href'))

        for url in links:
            self._check_link_works(url)

if __name__ == '__main__':
    unittest.main()