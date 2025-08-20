from jedi.plugins import pytest

import config

[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = test_*.py
python_files = tests.py test_*.py *_tests.py
