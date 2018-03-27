import os
import glob
import time
import lcddriver
import datetime
from vesync.api import VesyncApi
from time import strftime, localtime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

lcd = lcddriver.lcd()
lcd.lcd_clear()

api = VesyncApi("EMAIL", "PASSWORD")

fridge_id = "ID"
heater_id = "ID"

min_temp = 68
max_temp = 72
mid_temp = ((max_temp - min_temp) / 2) + min_temp

refresh_time = 30

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()

	equals_pos = lines[1].find('t=')

	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

def turn_on_fridge():
	api.turn_on(fridge_id)

def turn_on_heater():
	api.turn_on(heater_id)

def turn_off_fridge():
	api.turn_off(fridge_id)

def turn_off_heater():
	api.turn_off(heater_id)

turn_off_fridge()
turn_off_heater()

while True:
	#Get devices
	devices = api.get_devices()
	fridge_status = "off"
	heater_status = "off"

	#Get heater and fridge status
	for x in range(0, len(devices)):
		if devices[x]["cid"] == fridge_id:
			fridge_status = devices[x]["deviceStatus"]
		elif devices[x]["cid"] == heater_id:
			heater_status = devices[x]["deviceStatus"]

	#Get temperature
	temp = read_temp()[1]

	#Get current time
	current_time = strftime("%H:%M:%S", localtime())

	#Print status of system
	print '------------------------'
	print 'Time:\t', current_time
	print 'Temp:\t', temp
	print 'Fridge:\t', fridge_status
	print 'Heater:\t', heater_status

	#Show temp on screen
	lcd.lcd_clear()
	lcd.lcd_display_string("{0} (F)".format(temp), 1)

	#Show status and time on screen
	if(fridge_status == "on" and heater_status == "on"):
		lcd.lcd_display_string("ERROR", 2)
		turn_off_fridge()
		turn_off_heater()
	elif(heater_status == "on"):
		lcd.lcd_display_string("HEATING {0}".format(current_time), 2)
	elif(heater_status == "on"):
		lcd.lcd_display_string("COOLING {0}".format(current_time), 2)
	else:
		lcd.lcd_display_string("STANDBY {0}".format(current_time), 2)

	#Turn fridge on if higher than max temp
	if temp > max_temp:
		turn_on_fridge()
		turn_off_heater()

	#Turn heater on if lower than min temp
	elif temp < min_temp:
		turn_on_heater()
		turn_off_fridge()

	#Turn off heater if higher than mid temp
	elif temp > mid_temp:
		turn_off_heater()

	#turn off fridge if lower than mid temp
	elif temp < mid_temp:
		turn_off_fridge()

	#Sleep
	time.sleep(refresh_time)
