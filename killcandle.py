###
 # filename: readtemp.py
 # author: norris, joel r.
 # description:
 # 	taking temperature using RPi and DS18B20 probe
 ##

import os
import glob
import time
from threading import Timer
import RPi.GPIO as GPIO

base_temp = 0		# hold onto the relatice base temperature
temp_diff = 100		# a temp differential to check against
i = 0			# yay! an incrementor!
timer_off = True	# flag for the timer
timer_time = 17		# how long the timer should go for

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)                                                                                                         
GPIO.setwarnings(False)                                                                                                         
GPIO.setup(21,GPIO.OUT)                                                                                                                 

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
		return int(temp_string)
		#return temp_c 

# function to turn on the fan
def fan_on():
	print("fan on");
	GPIO.output(21,GPIO.HIGH)       
	time.sleep(10)
	print "fan off"  
	GPIO.output(21,GPIO.LOW) 
	

timer = Timer(timer_time, fan_on) 	# set up timer for fan

# main execution loop (infinite)
while True:
	
	if i==10: 
		base_temp = read_temp()
		print("base_temp= " + str(base_temp))
		print("trigger_temp= " + str(base_temp+temp_diff))

	print(read_temp())

	i += 1

	# compare base temp and temp diff, if base temp is greater than 
	# base temp + diff, start the timer.
	if i > 10:
		if (timer_off):
			if (read_temp() > (base_temp + temp_diff) ):

				print("timer started")
				timer.start()
				timer_off = False
 
	time.sleep(0.1)
 
