# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


# Package download data rule
define DATA_RULE
.PHONY: data-$(strip $2)-$(strip $1)
data-$(strip $2)-$(strip $1):
	python3 -c "$$$$DATA_UPDATE_PY" $(strip $1) $(strip $2)

.PHONY: data
data: data-$(strip $2)-$(strip $1)
endef


# JavaScript packages
$(eval $(call DATA_RULE, bare-script, javascript))
$(eval $(call DATA_RULE, element-model, javascript))
$(eval $(call DATA_RULE, markdown-model, javascript))
$(eval $(call DATA_RULE, markdown-up, javascript))
$(eval $(call DATA_RULE, schema-markdown-doc, javascript))
$(eval $(call DATA_RULE, schema-markdown, javascript))


# Python packages
$(eval $(call DATA_RULE, bare-script, python))
$(eval $(call DATA_RULE, chisel, python))
$(eval $(call DATA_RULE, markdown-up, python))
$(eval $(call DATA_RULE, ollama-chat, python))
$(eval $(call DATA_RULE, schema-markdown, python))
$(eval $(call DATA_RULE, simple-git-changelog, python))
$(eval $(call DATA_RULE, template-specialize, python))
$(eval $(call DATA_RULE, unittest-parallel, python))


# Python script to download and combine pypistats data
define DATA_UPDATE_PY
import datetime
import json
import os
import sys
import urllib.request

# Command-line arguments
package_name, package_language = sys.argv[1:]

# Minimum date for which to keep data
today = datetime.date.today()
date_min = today - (today - today.replace(year=today.year - 5))
date_min_iso = date_min.isoformat()

# Read the data file
package_file = os.path.join('data', f'{package_language}-{package_name}.json')
if os.path.isfile(package_file):
	with open(package_file, 'r', encoding='utf-8') as fh:
		package_data = json.load(fh)
else:
	package_data = []

# Get the package download data
if package_language == 'python':
	package_url = f'https://pypistats.org/api/packages/{package_name}/overall'
	with urllib.request.urlopen(package_url) as response:
		package_updated_raw = json.load(response)
	package_updated = [
		{'Package': package_name, 'Language': package_language, 'Date': row['date'], 'Downloads': row['downloads']}
		for row in package_updated_raw['data'] if row['category'] == 'without_mirrors'
	]
else: # package_language == 'javascript'
	year_ago = today - datetime.timedelta(days=365)
	package_url = f'https://api.npmjs.org/downloads/range/{year_ago.isoformat()}:{today.isoformat()}/{package_name}'
	with urllib.request.urlopen(package_url) as response:
		package_updated_raw = json.load(response)
	package_updated = [
		{'Package': package_name, 'Language': package_language, 'Date': row['day'], 'Downloads': row['downloads']}
		for row in package_updated_raw['downloads']
	]

# Update the package data
package_rows = []
row_dates = set()
for data in (package_updated, package_data):
	for row in data:
		if row['Date'] not in row_dates and row['Date'] >= date_min_iso:
			package_rows.append(row)
			row_dates.add(row['Date'])
package_rows.sort(key=lambda row: row['Date'])

# Update the data file
with open(package_file, 'w', encoding='utf-8') as fh:
	json.dump(package_rows, fh)
endef
export DATA_UPDATE_PY
