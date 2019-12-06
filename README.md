# rcv-app

## Overview
This application was developed for EGEN310R at Montana State University. The purpose of this application is to allow a user to control the GPIO pins on a Raspberry PI from an Android Phone using Bluetooth.

## Setup
Several steps should be taken in order to run this application.
1) Pull this code onto your laptop and your Raspberry PI
2) On your Raspberry PI:
  i) Create a virtual environment and activate it
  ii) Run `pip install PyBluez`
  ii) Run `pip install pigpio`
  iii) Start pigpiod by running `systemctl start pigpiod`
  iv) Run `python main.py` to run the application
3) On your computer:
  i) Connect your phone to your laptop and enable Android studio to run on it
  ii) Ensure that you are able to find the Raspberry PI's Bluetooth from your phone. If not, see this article: https://electronicshobbyists.com/controlling-gpio-through-android-app-over-bluetooth-raspberry-pi-bluetooth-tutorial/
  iii) Find the MAC Address of your vehicle and enter it on line 37 of the BluetoothController.java file.
  iv) This should be about all that there is to get this thing running. Now run build in Android Studio.
