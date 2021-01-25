HOW TO RUN THE CODE

Available features:

- /          gives a list of paths
- /pins      for a list of pins and their names
- /sensors   for a list of sensors  and their names
- /pins/
    - /pins/led      get value of led
    - /pins/led/on   turns on led
    - /pins/led/off  turns off led

    - /pins/np   get value of neopixels
    - /pins/np/1/red or /pins/np/1/green or /pins/np/1/blue    turns neopixel 1 red, green or blue
    - /pins/np/2/red or /pins/np/2/green or /pins/np/2/blue    turns neopixel 2 red, green or blue 
    - /pins/np/off   turns the neopixels off 

- /sensor/
    - /sensor/temp     get value of temperature sensor
    - /sensor/potent   get value of potentiometer  (also controls internal red led)