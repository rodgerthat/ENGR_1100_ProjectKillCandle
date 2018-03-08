###
 # filename: monitortemp.py
 # author: norris, joel r.
 # description:
 # 	monitoring temperature using RPi and DS18B20 probe
 ##

import os
import glob
import time
from threading import Timer

from datetime import datetime
from time import gmtime, strftime

base_temp = 0		# hold onto the relatice base temperature
temp_diff = 100		# a temp differential to check against
i = 0			# yay! an incrementor!
timer_off = True	# flag for the timer

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


# open the device and read the temp from the file (everything in linux is a file)
# read it, then close the file, 
# returns the file data
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# reads the lines and splits after the key values before the data
# converts to normal celcius value and returns that and converts to degrees F
def read_temp():

	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.05)
		lines = read_temp_raw()

	equals_pos = lines[1].find('t=')

	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		#return int(temp_string)
		#return temp_c 
		temp_string = str(temp_f)
		return temp_string 


# main execution loop (infinite)
while True:

	#f = open('2017_11_25_log.txt', 'a')	# open logfile for writing
	#right_now = datetime.time(datetime.now())
	right_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	logmsg =  right_now + " " + read_temp() 
	print(logmsg)
	#print(read_temp())
	#f.write(logmsg)
	#f.close()

	#time.sleep(300)		# 5 mins ( 60 * 5 = 300s )
	time.sleep(1)
 
