# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

import datetime
import io
import json
import os
import tempfile
import unittest
import unittest.mock
import urllib.error

import downloads


# The fixed "today" for tests
class MockDate(datetime.date):

    @classmethod
    def today(cls):
        return cls(2024, 2, 4)


# Helper to mock urllib.request.urlopen with a map of URL to JSON response (or exception)
def mock_urlopen(responses):
    def urlopen(url):
        response = responses[url]
        if isinstance(response, Exception):
            raise response
        return io.BytesIO(json.dumps(response).encode('utf-8'))
    return urlopen


PYPI_URL = 'https://pypistats.org/api/packages/alpha/overall'
NPM_URL = 'https://api.npmjs.org/downloads/range/2023-02-04:2024-02-04/alpha'


class TestDownloads(unittest.TestCase):

    def run_main(self, argv, package_data, responses):
        with tempfile.TemporaryDirectory() as temp_dir, \
             unittest.mock.patch('sys.argv', ['downloads.py', *argv]), \
             unittest.mock.patch('datetime.date', MockDate), \
             unittest.mock.patch('downloads.PACKAGES', [
                 {'Package': 'alpha', 'Language': 'JavaScript'},
                 {'Package': 'alpha', 'Language': 'Python'}
             ]), \
             unittest.mock.patch('urllib.request.urlopen', side_effect=mock_urlopen(responses)) as urlopen, \
             unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as stdout:
            cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                with open('downloads.json', 'w', encoding='utf-8') as fh:
                    json.dump(package_data, fh)
                downloads.main()
                with open('downloads.json', 'r', encoding='utf-8') as fh:
                    return json.load(fh), stdout.getvalue(), [call.args[0] for call in urlopen.call_args_list]
            finally:
                os.chdir(cwd)


    def test_main(self):
        package_data = [
            # Older than the minimum date - pruned
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2022-12-31', 'Downloads': 1},
            # Not in the update - kept
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2023-01-01', 'Downloads': 2},
            # In the update - replaced
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2024-02-02', 'Downloads': 3},
            {'Package': 'alpha', 'Language': 'JavaScript', 'Date': '2024-02-02', 'Downloads': 4},
            # Untracked package - kept
            {'Package': 'beta', 'Language': 'Python', 'Date': '2024-02-01', 'Downloads': 5}
        ]
        responses = {
            PYPI_URL: {
                'data': [
                    # Older than the minimum date - ignored
                    {'category': 'without_mirrors', 'date': '2022-12-30', 'downloads': 6},
                    {'category': 'with_mirrors', 'date': '2024-02-02', 'downloads': 70},
                    {'category': 'without_mirrors', 'date': '2024-02-02', 'downloads': 7},
                    {'category': 'without_mirrors', 'date': '2024-02-03', 'downloads': 8},
                    # Today's partial data - ignored
                    {'category': 'without_mirrors', 'date': '2024-02-04', 'downloads': 9}
                ]
            },
            NPM_URL: {
                'downloads': [
                    {'day': '2024-02-02', 'downloads': 10},
                    {'day': '2024-02-03', 'downloads': 11},
                    {'day': '2024-02-04', 'downloads': 12}
                ]
            }
        }
        package_data, stdout, urls = self.run_main(['--years', '1'], package_data, responses)
        self.assertListEqual(package_data, [
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2023-01-01', 'Downloads': 2},
            {'Package': 'beta', 'Language': 'Python', 'Date': '2024-02-01', 'Downloads': 5},
            {'Package': 'alpha', 'Language': 'JavaScript', 'Date': '2024-02-02', 'Downloads': 10},
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2024-02-02', 'Downloads': 7},
            {'Package': 'alpha', 'Language': 'JavaScript', 'Date': '2024-02-03', 'Downloads': 11},
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2024-02-03', 'Downloads': 8}
        ])
        self.assertEqual(stdout, 'Updating alpha (JavaScript)\nUpdating alpha (Python)\n')
        self.assertListEqual(urls, [NPM_URL, PYPI_URL])


    def test_main_default_years(self):
        package_data = [
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2018-12-31', 'Downloads': 1},
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2019-01-01', 'Downloads': 2}
        ]
        responses = {
            PYPI_URL: {'data': []},
            NPM_URL: {'downloads': []}
        }
        package_data, _, _ = self.run_main([], package_data, responses)
        self.assertListEqual(package_data, [
            {'Package': 'alpha', 'Language': 'Python', 'Date': '2019-01-01', 'Downloads': 2}
        ])


    def test_urlopen_json(self):
        with unittest.mock.patch('urllib.request.urlopen', side_effect=mock_urlopen({'url': {'a': 1}})), \
             unittest.mock.patch('time.sleep') as sleep:
            self.assertDictEqual(downloads.urlopen_json('url'), {'a': 1})
        sleep.assert_not_called()


    def test_urlopen_json_retry(self):
        responses = [urllib.error.URLError('error'), TimeoutError('timeout'), io.BytesIO(b'{"a": 1}')]
        with unittest.mock.patch('urllib.request.urlopen', side_effect=responses), \
             unittest.mock.patch('time.sleep') as sleep, \
             unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as stdout:
            self.assertDictEqual(downloads.urlopen_json('url'), {'a': 1})
        self.assertEqual(sleep.call_args_list, [unittest.mock.call(10), unittest.mock.call(10)])
        self.assertEqual(stdout.getvalue(), (
            '  Request failed (<urlopen error error>), retrying in 10s\n'
            '  Request failed (timeout), retrying in 10s\n'
        ))


    def test_urlopen_json_final_attempt(self):
        responses = [urllib.error.URLError('error')] * 4 + [io.BytesIO(b'{"a": 1}')]
        with unittest.mock.patch('urllib.request.urlopen', side_effect=responses) as urlopen, \
             unittest.mock.patch('time.sleep') as sleep, \
             unittest.mock.patch('sys.stdout', new_callable=io.StringIO):
            self.assertDictEqual(downloads.urlopen_json('url'), {'a': 1})
        self.assertEqual(urlopen.call_count, 5)
        self.assertEqual(sleep.call_count, 4)


    def test_urlopen_json_failure(self):
        with unittest.mock.patch('urllib.request.urlopen', side_effect=urllib.error.URLError('error')) as urlopen, \
             unittest.mock.patch('time.sleep') as sleep, \
             unittest.mock.patch('sys.stdout', new_callable=io.StringIO):
            with self.assertRaises(urllib.error.URLError):
                downloads.urlopen_json('url')
        self.assertEqual(urlopen.call_count, 5)
        self.assertEqual(sleep.call_count, 4)
