# CANbus data collection using Raspberry Pi and OSIsoft PI System

A vehicle’s CAN (Controller Area Network) is its way of communicating between each of its electronic components through a central bus. They send strings of bits that identify which component is "talking," followed by its current status or state. Some examples of the time series data that gets communicated:

- Temperature & kWh remaining on battery pack
- Speed of the vehicle, RPM of each wheel
- Flag warnings including: battery malfunction; high temperatures; and high current & voltage differentials  

By using a Raspberry Pi and a PiCAN2, it's possible to log the CAN messages directly from the vehicle onto the RPi. From there, this collection of Python scripts used in conjunction with a dictionary of data translations can be used to turn the raw CANbus output into meaningful, interpretable data.

## Setting up the Raspberry Pi 3

To enable the use of the PiCAN2 board, you need to first configure your RPi. Make sure that you have the newest version of the OS installed, and that everything is up to date. Open up a new terminal window, and enter:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
sudo reboot
```

Next, install the `can-utils` package, which includes all of the executable for viewing, sniffing, and logging the CAN messages. In the terminal, enter:
```
sudo apt-get install can-utils
```

Next, we have to edit the boot configuration file to recognize the PiCAN2 board on start-up. In the terminal, enter:
```
sudo nano /boot/config.txt
```
This brings up the text file, and allows you to make changes. Add the following text, then exit out of the file with CTRL-X, making sure to save your changes:
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=spi-bcm2835-overlay
dtoverlay=spi-dma-overlay
```

## Configuring a *virtual* CAN device
This procedure will configure a **VIRTUAL** can device, which is perfect for testing out your procedures. You can simulate the same type of data stream that you would be getting when plugged into the OBDII port of a car and receieving CAN messages.

In your terminal, first enter:
```
sudo modprobe vcan
```
This allows the module vcan to be loaded to the Linux kernal. Next, we will add a new vcan device. I'm going to call it `vcan0`. In the terminal, enter:
```
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```
Check to make sure the device was added by looking for it when you enter this in the terminal:
```
ifconfig
```
You should see it along with any other devices you have loaded.


## Configuring a *real* CAN device
This procedure is specific to the Nissan LEAF, but it very similar for other vehicles' CANbuses. The LEAF specifiic step is setting the `bitrate` to `500000`. Every vehicles CAN sends messages at a specefied bitrate, and the LEAF's happens to be 500,000. The most common ones are 33,333 bps, 50 Kbps, 83,333 bps, 100 Kbps, 125 Kbps, 250 Kbps, 500 Kbps, 800 Kpbs, and 1,000 Kbps. If you configure your device with the wrong bitrate, you will probably not recieve any data. 

Similarly to the virtual CAN setup, we start with the modprobe:
```
sudo modprobe vcan
```
The next step is the same except for the set up. *USE YOUR VEHICLE-SPECIFIC BITRATE*
```
sudo ip link add dev can0 type can
sudo ip link set can0 type can bitrate 500000 listen-only on
```
Check to make sure the device was added by looking for it when you enter this in the terminal:
```
ifconfig
```
You should see it along with any other devices you have loaded.





 

