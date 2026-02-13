***************************************************************************************

# Requirements for running this project:

- Install System-Level Dependencies

sudo apt install python3-lgpio

- Create and Activate a Python Virtual Environment (with system packages enabled for lgpio)

`python3 -m venv --system-site-packages venv'
`source venv/scripts/activate`

- Install Python Dependencies (Inside the Virtual Environment)

`pip install rpi_ws281x`
`pip install adafruit-circuitpython-neopixel`

# Configuring a Light Strip:

- cd into ./led
- Open config.py with an editor of your choice
- Set the default PIN that corresponds to the board's GPIO pin connected to the data wire
- Set the default amount of lights to be the amount of lights on the LED strip.

***************************************************************************************
