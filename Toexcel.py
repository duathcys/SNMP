from datetime import datetime

import pandas as pd

from Log import get_logger

logger = get_logger('Toexcel')


def excel_export(raw_data):
    try:
        raw_data = pd.DataFrame(raw_data)
        now = datetime.now()
        file_name = "test"

        path = 'download'
        output = path + '/%s_%s.xlsx' % (file_name, now.strftime('%Y%m%d%H%M%S'))
        raw_data.to_excel(excel_writer=output)
    except Exception as msg:
        logger.error(msg)
        logger.error('Toexcel')
