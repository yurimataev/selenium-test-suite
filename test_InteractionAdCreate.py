import unittest
from selenium import webdriver
from selenium import common
from SiteTestGeneric import SiteInteractionGeneric
import Model.AdCreation as AdCreation
import Model.Other as Other
import Model.Inputs as Inputs
from pprint import pprint
import re

class AdCreateTest(SiteInteractionGeneric):
    # Also test failure mode
        # - captcha fail
        # - mandatory fields?
        # - filters?
        # - spam protection?

    def test_ad_creation_unregistered(self):
        input = Inputs.AdCreationInput()

        self._test_ad_creation(input)

        # ensure ad is not automatically created
        self.driver.get(input.URL[6] + input.ad_n)
        self.assertTrue(self._is_error_page())

    def test_ad_creation_registered(self):
        input = Inputs.AdCreationRegisteredInput()

        self._login()
        self.driver.get(input.URL[0])
        self._test_ad_creation(input)

        # check ad is created correctly
        self.driver.get(input.ad_url)
        self._check_against_model(AdCreation.AdPageModel(input))

        # test send message
        self._test_send_messages_user(input)

    def _login(self):
        input = Inputs.LoginInput()
        self.driver.get(input.URL[0])
        self._fill_form(input.LOGIN_CREDENTIALS, 'user_login')

    def _logout(self):
        input = Inputs.LoginInput()
        self.driver.get(input.URL[1])

    def _test_send_messages_user(self, input):
        msg = Inputs.SendMessageUserRegisteredInput()
        self._test_send_message_user(
                input,
                msg,
                Other.SendMessageUserRegisteredModel(input, msg)
            )
        self._logout()
        self._test_send_message_user(
                input,
                Inputs.SendMessageUserInput(),
                Other.SendMessageUserModel(input)
            )

    def _test_send_message_user(self, input, msg, model):
        self.driver.get(input.ad_url)

        # retrieve link to contact page
        elem = self.driver.find_element_by_css_selector('div.send_message_oby > a')
        url = elem.get_attribute('href')

        # navigate to contact page
        self.driver.get(url)
        self._check_against_model(model)

        # input data
        self._fill_form(msg.MESSAGE_CONTENT, 'message_form')

        # check output page
        self._check_against_model(Other.SentMessageUserModel(input))

    def _test_ad_creation(self, input):
        self._test_category_selection_page(input)
        self._test_ad_creation_page(input)
        self._test_ad_preview_page(input)
        self._test_ad_published_page(input)
        self._test_ad_features_edited_page(input)
        self._test_payment_page(input)

    def _test_category_selection_page(self, input):
        self.driver.get(input.URL[0])

        self._check_value('c[]', '')
        self._check_selects_visibility('c', [True, False, False])
        for selection in input.CAT_SELECTS:
            self._interact_with_dropdown('c[]', 'c', selection[0], selection[1], selection[2], selection[3])

        self.driver.find_element_by_xpath("//form[@name='catform']//input[@type='submit']").click()

    def _test_ad_creation_page(self, input):
        self.assertEqual(input.URL[1], self.driver.current_url)
        self._check_value('a[]', '')
        self._check_selects_visibility('a1', [True, False, False])
        for selection in input.AREA_SELECTS:
            self._interact_with_dropdown('a[]', 'a1', selection[0], selection[1], selection[2], selection[3])

        self._fill_form(input.AD_CONTENT, 'the_form')

    def _test_ad_preview_page(self, input):
        for i in [True, False]:
            if i:
                curr_url = input.URL[2]
                input.ad_n = self.driver.current_url.replace(curr_url, '')
            else:
                curr_url = input.URL[3]

            self.assertFalse(self._is_submission_error())
            self.assertIn(curr_url, self.driver.current_url)
            ad_input = AdCreation.AdPreviewModel(input)
            self._check_against_model(ad_input)

            if i:
                edit_form = self.driver.find_element_by_css_selector('div#the_edit_form')
                preview_div = self.driver.find_element_by_css_selector('div#the_preview')
                self.assertFalse(edit_form.is_displayed())
                self.assertTrue(preview_div.is_displayed())
                self.driver.find_element_by_css_selector('div#the_preview > div.info input#edit_button').click()
                self.assertTrue(edit_form.is_displayed())
                self.assertFalse(preview_div.is_displayed())
                self.driver.find_element_by_xpath("//form[@id='the_form']//input[@type='submit' and @name='preview']").click()
            else:
                self.driver.find_element_by_css_selector('div#the_preview > div.info input#publish_button').click()

    def _test_ad_published_page(self, input):
        for i in [True, False]:
            if i:
                curr_url = input.URL[4] + input.ad_n + '&m='
                input.m = self.driver.current_url.replace(curr_url, '')

                if input.m == '3':
                    elem = self.driver.find_element_by_css_selector("div.info a")
                    input.ad_url = elem.get_attribute('href')
            else:
                curr_url = input.URL[5] + input.ad_n

            self.assertIn(curr_url, self.driver.current_url)

            if i:
                self._check_against_model(AdCreation.AdPublishedModel(input))
            self._check_against_model(AdCreation.AdFeaturesEditModel(input))

            if not i:
                xpath = "//input[@type='checkbox' and @name='featured']"
                self.driver.find_element_by_xpath(xpath).click()
                xpath = "//input[@type='checkbox' and @name='home_page']"
                self.driver.find_element_by_xpath(xpath).click()

                xpath = "//select[@name='period']/option[@value='90']"
                self.driver.find_element_by_xpath(xpath).click()
                xpath = "//select[@name='period']/option[@value='14']"
                self.driver.find_element_by_xpath(xpath).click()

            self.driver.find_element_by_xpath("//form[@id='ad_features_edit_form']//input[@type='submit']").click()

    def _test_ad_features_edited_page(self, input):
        self.assertIn(input.URL[5], self.driver.current_url)

        self._check_against_model(AdCreation.AdFeaturesEditedModel(input))

        xpath = "//input[@name='p_method'][1]"
        self.driver.find_element_by_xpath(xpath).click()
        xpath = "//input[@name='p_method'][4]"
        self.driver.find_element_by_xpath(xpath).click()

        elem = self.driver.find_element_by_css_selector('div.payment_options > div:nth-of-type(4)')
        input.expected_price = self._get_price_in_parentheses(elem)

        self.driver.find_element_by_xpath("//form[@id='payment_method_form']//input[@type='submit']").click()

    def _test_payment_page(self, input):
        self.assertEqual(input.URL[3], self.driver.current_url)

        self._check_against_model(AdCreation.PaymentPageModel(input))

        # Click each link? Re-test that page

    def _test_ad_page_in_depth(self):
        return True
        # Test contact link; test report abuse link
        # Test ad images -> LIGHTBOX
        # Test similar ads

    def _get_price_in_parentheses(self, elem):
        str = re.sub(r'^.+\((.+) (руб\.|USD|WMZ|WMR)\)$', r'\1', elem.text)
        return str

if __name__ == '__main__':
    unittest.main()