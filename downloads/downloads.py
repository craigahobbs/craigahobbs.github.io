# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

# pylint: disable=missing-function-docstring, missing-module-docstring

import argparse
import datetime
import json
import os
import urllib.request


# Packages to track
PACKAGES = [
    # JavaScript packages
    {'Package': 'bare-script', 'Language': 'JavaScript'},
    {'Package': 'element-model', 'Language': 'JavaScript'},
    {'Package': 'markdown-model', 'Language': 'JavaScript'},
    {'Package': 'markdown-up', 'Language': 'JavaScript'},
    {'Package': 'schema-markdown-doc', 'Language': 'JavaScript'},
    {'Package': 'schema-markdown', 'Language': 'JavaScript'},

    # Python packages
    {'Package': 'bare-script', 'Language': 'Python'},
    {'Package': 'chisel', 'Language': 'Python'},
    {'Package': 'markdown-up', 'Language': 'Python'},
    {'Package': 'ollama-chat', 'Language': 'Python'},
    {'Package': 'schema-markdown', 'Language': 'Python'},
    {'Package': 'simple-git-changelog', 'Language': 'Python'},
    {'Package': 'template-specialize', 'Language': 'Python'},
    {'Package': 'unittest-parallel', 'Language': 'Python'}
]


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser()
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
            pepy_url = f'https://api.pepy.tech/api/v2/projects/{package_name}'
            pepy_headers = {
                'X-API-Key': os.environ.get('PEPY_API_KEY'),
                'User-Agent': 'Mozilla/5.0 (compatible; MyScript/1.0)'
            }
            req = urllib.request.Request(pepy_url, headers=pepy_headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
            downloads_by_date = data.get('downloads') or {}
            package_updated = [
                {'Package': package_name, 'Language': package_language, 'Date': date_str, 'Downloads': sum(version_downloads.values())}
                for date_str, version_downloads in sorted(downloads_by_date.items())
            ]
        else: # package_language == 'JavaScript'
            year_ago = today - datetime.timedelta(days=365)
            package_url = f'https://api.npmjs.org/downloads/range/{year_ago.isoformat()}:{today.isoformat()}/{package_name}'
            with urllib.request.urlopen(package_url) as response:
                package_updated_raw = json.load(response)
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


if __name__ == '__main__':
    main()
