from datetime import datetime

import pandas as pd

from Log import get_logger

logger = get_logger('Toexcel')


def ExcelOut(raw_data):
    try:
        raw_data = pd.DataFrame(raw_data)
        now = datetime.now()
        filename = "test"

        path = 'download'
        OUTPUT = path + '/%s_%s.xlsx' % (filename, now.strftime('%Y%m%d%H%M%S'))
        raw_data.to_excel(excel_writer=OUTPUT)
    except Exception as msg:
        logger.error(msg)
        logger.error('Toexcel')
