# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

# pylint: disable=missing-function-docstring, missing-module-docstring

import argparse
import datetime
import json
import sys
import time
import urllib.error
import urllib.request


# Packages to track
PACKAGES = [
    # JavaScript packages
    {'Package': 'bare-script', 'Language': 'JavaScript'},
    {'Package': 'element-model', 'Language': 'JavaScript'},
    {'Package': 'markdown-model', 'Language': 'JavaScript'},
    {'Package': 'markdown-up', 'Language': 'JavaScript'},
    {'Package': 'schema-markdown', 'Language': 'JavaScript'},

    # Python packages
    {'Package': 'bare-script', 'Language': 'Python'},
    {'Package': 'chisel', 'Language': 'Python'},
    {'Package': 'ctxkit', 'Language': 'Python'},
    {'Package': 'markdown-up', 'Language': 'Python'},
    {'Package': 'ollama-chat', 'Language': 'Python'},
    {'Package': 'schema-markdown', 'Language': 'Python'},
    {'Package': 'simple-git-changelog', 'Language': 'Python'},
    {'Package': 'template-specialize', 'Language': 'Python'},
    {'Package': 'unittest-parallel', 'Language': 'Python'}
]


def main():
    # Command-line arguments
    argument_parser_args = {}
    if sys.version_info >= (3, 14): # pragma: no cover
        argument_parser_args['color'] = False
    parser = argparse.ArgumentParser(**argument_parser_args)
    parser.add_argument('--years', type=int, default=5, help='Number of years of data to keep')
    args = parser.parse_args()

    # Minimum date for which to keep data
    today = datetime.date.today()
    date_min = today - (today - today.replace(year=today.year - args.years, month=1, day=1))
    date_min_iso = date_min.isoformat()
    date_max_iso = today.isoformat()

    # Read the data file
    package_file = 'downloads.json'
    with open(package_file, 'r', encoding='utf-8') as fh:
        package_data = json.load(fh)

    # Iterate the packages
    for package in PACKAGES:
        package_name = package['Package']
        package_language = package['Language']
        print(f'Updating {package_name} ({package_language})')

        # Get the package download data
        if package_language == 'Python':
            package_url = f'https://pypistats.org/api/packages/{package_name}/overall'
            package_updated_raw = urlopen_json(package_url)
            package_updated = [
                {'Package': package_name, 'Language': package_language, 'Date': row['date'], 'Downloads': row['downloads']}
                for row in package_updated_raw['data'] if row['category'] == 'without_mirrors'
            ]
        else: # package_language == 'JavaScript'
            year_ago = today - datetime.timedelta(days=365)
            package_url = f'https://api.npmjs.org/downloads/range/{year_ago.isoformat()}:{today.isoformat()}/{package_name}'
            package_updated_raw = urlopen_json(package_url)
            package_updated = [
                {'Package': package_name, 'Language': package_language, 'Date': row['day'], 'Downloads': row['downloads']}
                for row in package_updated_raw['downloads']
            ]

        # Update the package data
        package_existing = [row for row in package_data if row['Package'] == package_name and row['Language'] == package_language]
        package_data = [row for row in package_data if not (row['Package'] == package_name and row['Language'] == package_language)]
        package_dates = set(row['Date'] for row in package_updated)
        package_data.extend(row for row in package_updated if row['Date'] < date_max_iso)
        for row in package_existing:
            if row['Date'] not in package_dates and row['Date'] >= date_min_iso:
                package_data.append(row)

    # Update the data file
    with open(package_file, 'w', encoding='utf-8') as fh:
        json.dump(sorted(package_data, key=lambda row: (row['Date'], row['Language'], row['Package'])), fh, indent=4)


# Helper to download a text resource URL with retries
def urlopen_json(url):
    retries = 5
    retry_delay_s = 10
    for _ in range(retries -1):
        try:
            with urllib.request.urlopen(url) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f'  Request failed ({exc}), retrying in {retry_delay_s}s')
            time.sleep(retry_delay_s)

    # Final attempt - let exceptions propagate
    with urllib.request.urlopen(url) as response:
        return json.load(response)


if __name__ == '__main__':
    main()
