#!/usr/local/bin/python
import subprocess
import logging
from time import sleep

host = '8.8.8.8'

logger = logging.getLogger('wifi_check')
log_handeler = logging.FileHandler('/var/log/wifi_check.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_handeler.setFormatter(formatter)
logger.addHandler(log_handeler) 
logger.setLevel(logging.DEBUG)

def reboot_host():
	subprocess.call(['shutdown', '-r', 'now'])
	
def ping():
	ping_response = subprocess.call(['ping', '-c', '5', host])
	print ping_response
	if ping_response == 0:
		logger.info('Ping check passed to ' + host)
	elif ping_response == 2 or ping_response == 1:
		logger.error('Initial Ping check failed to ' + host)
		ping_response_recheck = subprocess.call(['ping', '-c', '5', host])
		if ping_response_recheck == 2 or ping_response_recheck == 1:
			logger.error('Secondary Ping check failed to ' + host + ' REBOOTING')
			reboot_host()
		else:
			logger.info('Secondary check passed to ' + host)
	else:
		logger.warning('Ping not complete, may be packet lost to ' + host)
			
if __name__ == "__main__":		
	ping()
