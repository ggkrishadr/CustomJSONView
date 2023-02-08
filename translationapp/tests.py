from django.test import TestCase

from core import settings


# Create your tests here.
class LanguageTestCase(TestCase):
    codes = [lang[0] for lang in settings.LANGUAGES]
    label = [lang[1] for lang in settings.LANGUAGES]

    def test_language_option_empty(self):
        self.assertGreaterEqual(len(settings.LANGUAGES), 1)

    def test_default_language_code(self):
        self.assertIn(settings.DEFAULT_LANGUAGE_CODE, self.codes)

    def test_empty_or_none_code(self):
        self.assertNotIn('', self.codes) or self.assertNotIn(None, self.codes)

    def test_empty_or_none_labels(self):
        self.assertNotIn('', self.label) or self.assertNotIn(None, self.label)
