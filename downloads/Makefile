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


define DATA_UPDATE_PY
import datetime
import json
import os
import sys
import urllib.request

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
package_dates = set(row['date'] for row in package_data['data'])
for row in package_updated['data']:
	if row['date'] not in package_dates:
		package_data['data'].append(row)

# Filter rows by date
date_min = (datetime.date.today() - datetime.timedelta(days=366)).isoformat()
package_data['data'] = [row for row in package_data['data'] if row['date'] >= date_min]

# Update the data file
package_data['data'].sort(key=lambda row: row['date'])
with open(package_file, 'w', encoding='utf-8') as fh:
	json.dump(package_data, fh)
endef
export DATA_UPDATE_PY
