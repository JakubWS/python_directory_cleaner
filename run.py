import os, datetime, sys, time, pprint
import lib
from lib import log as log
from lib import log_error as log_error
logFile_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
logfile_name = str("cleanup-"+logFile_timestamp+".log")
config = lib.load_configuration('configuration.yml')
logfile_path = config['common']['logsFolderFullPath']
lib.create_folder(logfile_path)
logfile_full_path = os.path.join(logfile_path,logfile_name)

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(logfile_full_path, "a")
   
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        self.log.close()
    
sys.stdout = Logger()
now = time.time()
log('Starting cleaning - ' + str(now))
dir_list = config['Jobs']
log('folders to clean: ')
pprint.pprint(dir_list)
for dir in dir_list:
    
    item_path = dir['path']
    
    if dir['method'] == 'lastfiles':  
        how_many = int(dir['how_many_to_keep'])*-1
        items = lib.getfiles(item_path)
        items = items[:how_many]
        
        for item in items:
            full_path_to_delete = os.path.join(item_path, item)
            log('deleting: '+full_path_to_delete)
            if os.path.exists(full_path_to_delete):
                os.remove(full_path_to_delete)
                if lib.file_exists(full_path_to_delete) == False:
                    log("file "+ item + " deleted successfully")
                else:
                    log_error("cannot delete "+full_path_to_delete)
    
    elif dir['method'] == 'lastdays':
        for filename in os.listdir(item_path):
            filestamp = os.stat(os.path.join(item_path, filename)).st_mtime
            how_many = int(dir['how_many_to_keep'])
            filecompare = now - how_many * 86400
            if  filestamp < filecompare:
                full_path_to_delete = os.path.join(item_path, filename)
                if os.path.exists(full_path_to_delete):
                    os.remove(full_path_to_delete)
                if lib.file_exists(full_path_to_delete) == False:
                    log("file "+ filename + " deleted successfully")
                else:
                    log_error("cannot delete "+full_path_to_delete)

log("end of cleaning... CU")
