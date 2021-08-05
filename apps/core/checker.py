import json

from django.test import TestCase


class BaseChecker(TestCase):
    def assertDictEqual(self, data1, data2, fields):
        for field in fields:
            self.assertEqual(data1.get(field), data2.get(field))

    def assertResponse201(self, response):
        self.assertEqual(response.status_code, 201)

    def assertResponse400(self, response):
        self.assertEqual(response.status_code, 400)

    def assertResponse401(self, response):
        self.assertEqual(response.status_code, 401)

    def loadJSONSafely(self, response):
        try:
            responseData = json.loads(response.content)
        except ValueError:
            self.fail("Coudln't load the JSON data safely.")
        return responseData

    def assertFieldsMissing(self, response, fields):
        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)

        # Make sure there are the same amount of fields missing
        self.assertEqual(len(responseData), len(fields))

        errorDict = {}
        for field in fields:
            errorDict[field] = ['This field is required.']
        
        self.assertDictEqual(responseData, errorDict, fields)
