import os

import pandas as pd

from Log import get_logger

logger = get_logger('Convert')


def excel_to_csv():
    try:
        file_name = 'file/test.xlsx'
        dataset = pd.read_excel(file_name, usecols=[1, 2, 3, 4, 5])
        path = 'download'
        csv_file = path + '/SNMP_test.csv'
        dataset.to_csv(csv_file,
                       index=None, header=True, encoding='cp949')
        data = pd.read_csv(csv_file, encoding='cp949')
        os.remove(csv_file)
        return data
    except Exception as msg:
        logger.error(msg)
        logger.error('Convert.py')
