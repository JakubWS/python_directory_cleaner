import datetime, requests,os,yaml
from os.path import exists as file_exists


def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S:%f")
    print(timestamp+" :: [info] "+message)

def log_error(message):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S:%f")
    print(timestamp+" :: [error]"+message)

def log_fatal(message):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S:%f")
    print(timestamp+" :: [fatal]"+message)
    quit()
  
def connection_test(url, timeout):
    try:
        request = requests.get(url, timeout=timeout, verify=False)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def test_path(path):
    if file_exists(path) == True:
        log("path " + path + " exist")
        return True
    else:
        log("path " + path + " not found")
        return False
        
def create_folder(path):
    if test_path(path) == False:
        log("creating directory "+path)
        os.mkdir(path)

def load_configuration(path):
    test_path(path)
    with open(path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def getfiles(path):
    list = [item for item in os.listdir(path)
        if os.path.isfile(os.path.join(path, item))]
    list.sort(key=lambda item: os.path.getmtime(os.path.join(path, item)))
    return list
    