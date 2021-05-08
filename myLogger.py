
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def log(message, level='INFO'):
    log = ""
    if level == 'ERR':
        log += FAIL + "[ERR] "
    elif level == 'WARN':
        log += WARNING  + "[WARN] "
    elif level == 'OK':
        log += OKGREEN + "[INFO] "
    else:
        print("[INFO]", message)
        return 0
    print(log + message + ENDC)