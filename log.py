### log를 세팅 해주는 단계입니다.
# logging 모듈 import
import logging
import logging.handlers
import os
from datetime import datetime
import time
import sys
import traceback as tr



def get_logger(name=None):
    # 1 logger instance를 만듭니다.
    logger = logging.getLogger(name)

    # log 저장 폴더 생성
    # TODO log 폴더 별도 관리 > 절대 경로
    today_month = datetime.today().strftime("%Y_%m")

    dir_path = 'log' + '/' + today_month + '/'

    # 월별 log 폴더 생성
    os.makedirs(dir_path, exist_ok=True)

    # 2 logger의 level을 가장 낮은 수준인 DEBUG로 설정합니다.
    logger.setLevel(logging.DEBUG)

    # 3 formatter 지정하여 log head를 구성해줍니다.
    ## asctime - 시간정보
    ## levelname - logging level
    ## funcName - log가 기록된 함수
    ## lineno - log가 기록된 line
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s")

    # 4 handler instance 생성하여 console 및 파일로 저장할 수 있도록 합니다. 파일명은 txt도 됩니다.
    console = logging.StreamHandler()
    file_handler_debug = logging.FileHandler(filename=dir_path + "log_debug.log")
    file_handler_info = logging.FileHandler(filename=dir_path + "log_info.log")
    file_handler_error = logging.FileHandler(filename=dir_path + "log_error.log")

    # 5 handler 별로 다른 level 설정합니다. 설정한 level 이하 모두 출력,저장됩니다.
    console.setLevel(logging.DEBUG)
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_info.setLevel(logging.INFO)
    file_handler_error.setLevel(logging.ERROR)

    # 6 handler 출력을 format 지정방식으로 합니다.
    console.setFormatter(formatter)
    file_handler_debug.setFormatter(formatter)
    file_handler_info.setFormatter(formatter)
    file_handler_error.setFormatter(formatter)

    # 7 logger에 handler 추가합니다.
    logger.addHandler(console)
    logger.addHandler(file_handler_debug)
    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_error)

    # 8 설정된 log setting을 반환합니다.
    return logger

def catchException(logger, script_name, max_seq, startTime, typ, value, traceback):
    logger.error(f"Script: {script_name}")
    logger.error("Type: %s" % typ)
    logger.error("Value: %s" % value)
    logger.error("Traceback: %s" % traceback)
    logger.error("Unexpected exception", exc_info=(typ, value, traceback))

    # 강제 종료 로깅 추가
    if issubclass(typ, KeyboardInterrupt):
        msg = 'Shutdown by User Request(KeyboardInterrupt)'
    else:
        msg = "".join(tr.format_exception(typ, value, traceback))

    argument = sys.argv
