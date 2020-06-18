import unittest
from selenium import webdriver
from selenium import common
from SiteTestGeneric import SiteInteractionGeneric
import Model.Render as Render
import Model.Other as Other
from pprint import pprint
import re

class InteractionTest(SiteInteractionGeneric):

    def _test_send_message_admin(self):
        return True

    def _test_report_abuse(self):
        return True
    def _test_report_abuse_no_ad(self):
        return True

    def _test_user_create(self):
        return True
    def _test_user_edit(self):
        return True

if __name__ == '__main__':
    unittest.main()