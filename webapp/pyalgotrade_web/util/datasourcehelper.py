import os
from django.conf import settings

PYALGOTRADE_BASE = os.path.abspath(os.path.join(settings.BASE_DIR, ".."))
PYALGOTRADE_DATA_FOLDER = os.path.join(PYALGOTRADE_BASE, "data/")
PYALGOTRADE_SAMPLES_FOLDER = os.path.join(PYALGOTRADE_BASE, "samples/")
PYALGOTRADE_TEMP_DUMP_JSON_FILE = os.path.join(PYALGOTRADE_DATA_FOLDER, "temp/jsondump.json")


class DataSourceHelper:
    csvExtension = '.csv'

    def __init__(self):
        pass

    @staticmethod
    def getDataFilePath(csvFileName):
        """
        Builds a fully qualified path to a csv file in the dedicated data folder from a simple file name.
        :param csvFileName: str
        :return: Full path to file if it exists, empty path otherwise.
        """
        if csvFileName[-4:] != DataSourceHelper.csvExtension:
            csvFileName += DataSourceHelper.csvExtension
        fullPath = os.path.join(PYALGOTRADE_DATA_FOLDER, csvFileName)
        if os.path.isfile(fullPath):
            return fullPath
        else:
            # Try in samples?
            fullPath = os.path.join(PYALGOTRADE_SAMPLES_FOLDER, csvFileName)
            if os.path.isfile(fullPath):
                return fullPath
            else:
                return ''

    @staticmethod
    def getTempDumpJsonFilePath():
        return PYALGOTRADE_TEMP_DUMP_JSON_FILE
