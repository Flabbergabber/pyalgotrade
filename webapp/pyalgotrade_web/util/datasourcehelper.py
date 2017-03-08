import os
from django.conf import settings

PYALGOTRADE_BASE = os.path.abspath(os.path.join(settings.BASE_DIR, ".."))
PYALGOTRADE_DATA_FOLDER = os.path.join(PYALGOTRADE_BASE, "data/")
PYALGOTRADE_SAMPLES_FOLDER = os.path.join(PYALGOTRADE_BASE, "samples/")
