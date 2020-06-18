import unittest
from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import time
from Model.Render import ErrorModel

ERROR_URL = ErrorModel().META_TITLE

class SiteTestGeneric(unittest.TestCase):
    def setUp(self):

        self.headless = True

        options = Options()

        if self.headless:
            options.add_argument("--headless") # Runs Chrome in headless mode.
            options.add_argument('--disable-gpu')  # applicable to windows os only
        options.add_argument('--no-sandbox') # Bypass OS security model
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        # Prevent any output to STDOUT
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=OFF")
        self.driver = webdriver.Chrome(options=options)

        # self.driver = webdriver.Chrome()
        self.maxDiff = None
        self.driver.implicitly_wait(5)
        # self.driver.maximize_window()

    def tearDown(self):
        # check for javascript errors
        self._check_javascript_errors()

        # wait if we're not running in headless mode
        if not self.headless:
            time.sleep(30)

        # close the browser window
        self.driver.quit()

    def _fetch_check_against_model(self, model):
        self.driver.get(model.URL)
        self._check_against_model(model)

    def _check_against_model(self, model):
        if model.STRICT: func = self.assertEqual
        else           : func = self.assertIn

        if hasattr(model, 'META_TITLE'):
            func(model.META_TITLE, self.driver.title)

        if hasattr(model, 'META_DESC'):
            elem = self.driver.find_element_by_xpath('//html/head/meta[@name="description"]')
            func(model.META_DESC, elem.get_attribute('content'))

        if hasattr(model, 'META_KW'):
            elem = self.driver.find_element_by_xpath('//html/head/meta[@name="keywords"]')
            func(model.META_KW, elem.get_attribute('content'))

        self._check_expected_content(model)
        self._check_expected_counts(model)
        if model.CHECK_LINKS:
            self._check_links_work(model)

    def _check_expected_content(self, model):
        for expectation in model.EXPECTED_CONTENTS:
            elem = self.driver.find_element_by_css_selector(expectation[0])

            if hasattr(expectation[1], '__call__'):
                if expectation[2]:
                    value = expectation[1](elem, expectation[2])
                else:
                    value = expectation[1](elem)
            else:
                value = getattr(elem, expectation[1])

            if len(expectation) == 5:
                if   expectation[4] == 'NotNone':
                    self.assertIsNotNone(value)
                elif expectation[4] == 'NotIn':
                    self.assertNotIn(expectation[3], value)
            elif model.STRICT:
                self.assertEqual(value, expectation[3])
            else:
                self.assertIn(value, expectation[3])

    def _check_expected_counts(self, model):
        for selector, expectation in model.EXPECTED_COUNTS.items():
            arr = self.driver.find_elements_by_css_selector(selector)
            self.assertEqual(expectation, len(arr))

    def _check_links_work(self, model):
        arr = []
        for expectation in model.EXPECTED_CONTENTS:
            elem = self.driver.find_element_by_css_selector(expectation[0])
            if elem.tag_name == 'a':
                arr.append(elem.get_attribute('href'))

        for url in list(set(arr)):
            self._check_link_works(url)

    def _check_link_works(self, url):
        self.driver.get(url)
        self.assertFalse(self._is_error_page())

    def _is_error_page(self):
        if self.driver.title == ERROR_URL:
            return True

    def _check_javascript_errors(self):
        # Check for javascript errors
        browserLog = self.driver.get_log("browser")
        errors = [logEntry['message']
            for logEntry in browserLog
            if (logEntry['level'] == 'SEVERE' and
                logEntry['source'] == 'javascript')]
        if errors:
            self.fail("The following Javascript errors occurred:\n\t" + "\n\t".join(errors) + "\n")

class SiteInteractionGeneric(SiteTestGeneric):

    def _fill_form(self, model_values, form_id):
        for name, value in model_values.items():
            elem = self.driver.find_element_by_xpath("//form[@id='" + form_id + "']//*[@name='"+name+"']")
            type = elem.get_attribute('type')
            if elem.tag_name == 'textarea' or \
               type == 'text' or type == 'password':
                elem.send_keys(value)
            elif type == 'checkbox':
                if (value == True and not elem.is_selected()) or \
                    (value == False and elem.is_selected()):
                        elem.click()

        self.driver.find_element_by_xpath("//form[@id='" + form_id + "']//input[@type='submit']").click()

    def _interact_with_dropdown(self, input_name, select_name, dropdown_n, option_name, expected, has_subcats):
        dropdown_name = select_name + str(dropdown_n)
        xpath = "//select[@name='" + dropdown_name + "']/option[text()='" + option_name + "']"
        self.driver.find_element_by_xpath(xpath).click()
        vis_arr = [True] * (dropdown_n)
        vis_arr.append( has_subcats )
        vis_arr.extend( [False] * ( 4 - dropdown_n ) )
        self._check_selects_visibility(select_name, vis_arr)
        self._check_value(input_name, expected)

    def _check_selects_visibility(self, select_name, vis):
        names = ['1','2','3']
        for name, visibility in zip(names, vis):
            # print (name + ' : ' + str(visibility))
            elem = self.driver.find_element_by_name(select_name + name)
            self.assertEqual(visibility, elem.is_displayed())

    def _is_submission_error(self):
        try:
            elem = self.driver.find_element_by_css_selector('div.info > h3.red')
        except common.exceptions.NoSuchElementException:
            return False

        # return True
        elem = self.driver.find_element_by_css_selector('div.info')
        return elem.text

    def _check_value(self, elem_name, expected):
        elem = self.driver.find_element_by_name(elem_name)
        self.assertEqual(expected, elem.get_attribute('value'))

if __name__ == '__main__':
    unittest.main()