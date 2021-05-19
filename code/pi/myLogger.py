from datetime import datetime

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def log(message, level='INFO'):
    time_string = f'({datetime.now().strftime("%H:%M:%S.%f")})'
    # time_string = f'({datetime.now().strftime("%H:%M:%S")})'
    log = ""
    if level == 'ERR':
        log += FAIL + "[ERR]"
    elif level == 'WARN':
        log += WARNING  + "[WARN]"
    elif level == 'OK':
        log += OKGREEN + "[INFO]"
    else:
        log += "[INFO]"
        # print("[INFO]", message)
        # return 0
    print(log, time_string, ':', message, ENDC)