import json
from django.forms import fields

from django.test import TestCase


class BaseChecker(TestCase):
    fields = []
    response = None
    check_against_data = []
    responseData = {}

    def checkDictEqual(self, data1, data2, fields_to_check=None):
        if fields_to_check is None:
            fields_to_check = self.fields

        for field in fields_to_check:
            if data1.get(field) != data2.get(field):
                return False
        return True

    def checkDictArrayEqualAnyOrder(self, data1, data2, fields_to_check=None):
        if fields_to_check is None:
            fields_to_check = self.fields

        self.assertEqual(len(data1), len(data2))

        for datum1 in data1:
            found = False
            for datum2 in data2:
                if self.checkDictEqual(datum1, datum2, fields_to_check):
                    found = True
                    break
            if not found:
                return False
        return True

    def assertDictListSame(self, data1, data2, fields_to_check=None):
        if fields_to_check is None:
            fields_to_check = self.fields

        self.assertTrue(self.checkDictArrayEqualAnyOrder(data1, data2, fields_to_check))

    def assertDictEqual(self, data1, data2, fields_to_check=None):
        if fields_to_check is None:
            fields_to_check = self.fields

        self.assertTrue(self.checkDictEqual(data1, data2, fields_to_check))
        
    # Ok
    def assertResponse200(self):
        self.assertEqual(self.response.status_code, 200)
        self.loadJSONSafely()

    # Created
    def assertResponse201(self):
        self.assertEqual(self.response.status_code, 201)
        self.loadJSONSafely()

    # Bad request
    def assertResponse400(self):
        self.assertEqual(self.response.status_code, 400)

    # Unauthorized
    def assertResponse401(self):
        self.assertEqual(self.response.status_code, 401)

    # Not found
    def assertResponse404(self):
        self.assertEqual(self.response.status_code, 404)

    def loadJSONSafely(self):
        try:
            self.responseData = json.loads(self.response.content)
        except ValueError:
            self.fail("Couldn't load the JSON data safely.")

    def assertFieldsMissing(self, fields_to_check):
        self.loadJSONSafely()

        # Make sure there are the same amount of fields missing
        self.assertEqual(len(self.responseData), len(fields_to_check))

        errorDict = {}
        for field in fields_to_check:
            errorDict[field] = ['This field is required.']

        self.assertDictEqual(self.responseData, errorDict, fields_to_check)

    # This compares the current check_against_data to the current response data
    # using whatever fields are currently set
    def assertResponseEqual(self):
        self.loadJSONSafely()

        # Gotta check to see if it's a list
        if isinstance(self.check_against_data, list):
            self.assertDictListSame(self.responseData, self.check_against_data)
        else:
            self.assertDictEqual(self.responseData, self.check_against_data)