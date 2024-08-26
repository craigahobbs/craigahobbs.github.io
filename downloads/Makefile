# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


# Python package download rule
define PYTHON_DATA_RULE
.PHONY: python-$(strip $1)
python-$(strip $1):
	python3 -c "$$$$DATA_UPDATE_PY" $(strip $1)

.PHONY: data
data: python-$(strip $1)
endef


# Python package download rules
$(eval $(call PYTHON_DATA_RULE, bare-script))
$(eval $(call PYTHON_DATA_RULE, chisel))
$(eval $(call PYTHON_DATA_RULE, markdown-up))
$(eval $(call PYTHON_DATA_RULE, ollama-chat))
$(eval $(call PYTHON_DATA_RULE, schema-markdown))
$(eval $(call PYTHON_DATA_RULE, simple-git-changelog))
$(eval $(call PYTHON_DATA_RULE, template-specialize))
$(eval $(call PYTHON_DATA_RULE, unittest-parallel))


# Python script to download and combine pypistats data
define DATA_UPDATE_PY
import datetime
import json
import os
import sys
import urllib.request

# Maximum days of download data to keep
max_days = 365

# Report the data file name
package_name = sys.argv[1]
package_file = os.path.join('data', f'python-{package_name}.json')
print(f'Downloading data/{package_file}.json')

# Read the data file
if os.path.isfile(package_file):
	with open(package_file, 'r', encoding='utf-8') as fh:
		package_data = json.load(fh)
else:
	package_data = {'data': []}

# Get the pypistats data
package_url = f'https://pypistats.org/api/packages/{package_name}/overall'
with urllib.request.urlopen(package_url) as response:
	package_updated = json.load(response)

# Update the package data
package_rows = []
row_keys = set()
date_min = (datetime.date.today() - datetime.timedelta(days=max_days + 1)).isoformat()
for data in (package_updated, package_data):
	for row in data['data']:
		row_key = (row['date'], row['category'])
		if row_key not in row_keys and row['date'] >= date_min:
			package_rows.append(row)
			row_keys.add(row_key)
package_rows.sort(key=lambda row: (row['date'], row['category']))
package_data['data'] = package_rows

# Update the data file
with open(package_file, 'w', encoding='utf-8') as fh:
	json.dump(package_data, fh)
endef
export DATA_UPDATE_PY
