import os

import pandas as pd

from Log import get_logger

logger = get_logger('Convert')


def ExcelToCSV():
    try:
        FILE = 'file/test.xlsx'
        dataset = pd.read_excel(FILE, usecols=[1, 2, 3, 4, 5])
        path = 'download'
        CSVFILE = path + '/SNMP_test.csv'
        dataset.to_csv(CSVFILE,
                       index=None, header=True, encoding='cp949')
        data = pd.read_csv(CSVFILE, encoding='cp949')
        os.remove(CSVFILE)
        return data
    except Exception as msg:
        logger.error(msg)
        logger.error('Convert.py')
