import os
import unittest
from reversedns import Client, Fields
from reversedns import ParameterError, ApiAuthError


class TestClient(unittest.TestCase):
    """
    Final integration tests without mocks.

    Active API_KEY is required.
    """

    def setUp(self) -> None:
        self.client = Client(os.getenv('API_KEY'))

        self.correct_terms = [
            {
                'field': Fields.domain,
                'term': 'facebook.*'
            }
        ]

        self.correct_terms_exclude = [
            {
                'field': Fields.domain,
                'term': 'facebook.*',
                'exclude': True
            }
        ]

        self.incorrect_terms = [
            {
                'term': 'facebook.*',
            }
        ]

        self.incorrect_terms_exclude = [
            {
                'field': Fields.domain,
                'term': 'facebook.*',
                'exclude': 'foo'
            }
        ]

        self.incorrect_terms_field = [
            {
                'field': 'foo is not bar',
            }
        ]

        self.incorrect_terms_many = [
            {
                'field': Fields.domain,
                'term': 'foo.*'
            },
            {
                'field': Fields.domain,
                'term': 'bar.*'
            },
            {
                'field': Fields.domain,
                'term': 'baz.*'
            },
            {
                'field': Fields.domain,
                'term': 'spam.*'
            },
            {
                'field': Fields.domain,
                'term': 'ham.*'
            }
        ]

        self.incorrect_terms_short = [
            {
                'field': Fields.domain,
                'term': 'ab'
            }
        ]

        self.incorrect_terms_str = [
            {
                'foo',
                'bar'
            }
        ]

    def test_get_correct_data(self):
        response = self.client.get(
            terms=self.correct_terms,
            record_type=Client.TXT
        )
        self.assertIsNotNone(response.size)

    def test_extra_parameters(self):
        response = self.client.get(
            terms=self.correct_terms,
            record_type=Client.TXT,
            limit=2
        )
        self.assertEqual(response.size, 2)

    def test_empty_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(record_type=Client.TXT)

    def test_empty_record_type(self):
        with self.assertRaises(ParameterError):
            self.client.get(terms=self.correct_terms)

    def test_empty_api_key(self):
        with self.assertRaises(ParameterError):
            client = Client('')
            client.get(terms=self.correct_terms, record_type=Client.TXT)

    def test_incorrect_api_key(self):
        client = Client('at_00000000000000000000000000000')
        with self.assertRaises(ApiAuthError):
            client.get(terms=self.correct_terms, record_type=Client.TXT)

    def test_raw_data(self):
        response = self.client.get_raw(
            terms=self.correct_terms,
            record_type=Client.TXT,
            output_format=Client.XML_FORMAT
        )
        self.assertTrue(response.startswith('<?xml'))

    def test_exclude(self):
        response = self.client.get(
            terms=self.correct_terms_exclude,
            record_type=Client.TXT
        )
        self.assertIsNotNone(response.size)

    def test_incorrect_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.incorrect_terms,
                record_type=Client.TXT
            )

    def test_incorrect_str_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.incorrect_terms_str,
                record_type=Client.TXT
            )

    def test_incorrect_exclude_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.incorrect_terms_exclude,
                record_type=Client.TXT
            )

    def test_incorrect_field_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.incorrect_terms_field,
                record_type=Client.TXT
            )

    def test_incorrect_many_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.incorrect_terms_many,
                record_type=Client.TXT
            )

    def test_incorrect_short_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.incorrect_terms_short,
                record_type=Client.TXT
            )

    def test_incorrect_record_type(self):
        with self.assertRaises(ParameterError):
            self.client.get(terms=self.correct_terms, record_type='foo')

    def test_incorrect_limit(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.correct_terms,
                record_type=Client.TXT,
                limit=1001
            )

    def test_output(self):
        with self.assertRaises(ParameterError):
            self.client.get(
                terms=self.correct_terms,
                record_type=Client.TXT,
                response_format='yaml'
            )


if __name__ == '__main__':
    unittest.main()
