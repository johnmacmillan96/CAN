# CANbus data collection using Raspberry Pi and OSIsoft PI System

A vehicle’s CAN (Controller Area Network) is its way of communicating between each of its electronic components through a central bus. They send strings of bits that identify which component is "talking," followed by its current status or state. Some examples of the time series data that gets communicated:

•	Temperature & kWh remaining on battery pack
•	Speed & RPM of each wheel
•	Flag warnings including: battery malfunction; high temperatures; and high current & voltage differentials  

By using a Raspberry Pi and a PiCAN2, it's possible to log the CAN messages directly from the vehicle onto the RPi. From there, this collection of Python scripts used in conjunction with a dictionary of data translations can be used to turn the raw CANbus output into meaningful, interpretable data.


 

