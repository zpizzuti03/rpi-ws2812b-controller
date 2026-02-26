# Requirements for running this project:

## Install System-Level Dependencies

```sudo apt install python3-lgpio```

## Create and Activate a Python Virtual Environment with system packages enabled for lgpio

```python3 -m venv --system-site-packages venv```

```source venv/scripts/activate```

## Install Python Dependencies inside of the Virtual Environment

```pip install rpi_ws281x```

```pip install adafruit-circuitpython-neopixel```

# Configuring a Light Strip:

## From the root directory:

```cd ./led```

### Open config.py with an editor of your choice

### Set the default PIN that corresponds to the board's GPIO pin connected to the data wire.
- This project's default is the rpi5 GPIO 18 pin.
```PIN = board.D18```

### Set the default amount of lights to be the amount of lights on your physical LED strip.
- This project's default is a strip of length 60.
```LED_COUNT = 60```

## Running the Application
- From the project root directory, execute the CLI module:

```python3 -m cli.__main__ -h```

### To run the testing code, you will also need to install pytest in your Virtual Environment:
```pip install -U pytest```
