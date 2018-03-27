# FridgeTemperatureController

The goal of this project is to manage the temperature of a fridge to ferment beer. This was accomplished using a Raspberry Pi, temperature probe (DS18B20), i2c screen, fish tank heater, Vsync smart outlets, and a mini fridge. 

The fridge and heater are plugged into the smart outlets and using a wrapper created by tylergets (https://github.com/tylergets/python-vesync) I am able to turn the fridge/heater on or off based on the temperature. A threshold is set so when the temperature dips below the set minimum the heater is turned on and vice versa.

I followed this tutorial for setting up the temperature probe: https://www.hackster.io/timfernando/a-raspberry-pi-thermometer-you-can-access-anywhere-33061c

I followed this tutorial for setting up the i2c screen here: https://tutorials-raspberrypi.com/control-a-raspberry-pi-hd44780-lcd-display-via-i2c/
