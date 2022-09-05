# New School Robotics Team - Engineering Materials
This repository contains all information and code necessary to be able to reproduce our FE vehicle's design and function. The files are contained in folders in the main branch, while all info regarding programming and the principles behind the code can be found in this document.

## Table of contents
1. [Introduction](#introduction)
2. [Hardware](#hardware)
    - [Power](#hardwarepower)
    - [Motors](#hardwaremotor)
    - [Control](#hardwarecontrol)
    - [Sensing](#hardwaresensing)
    - [Hardware List](#hardwarelist)
3. [Uploading Code](#upload)
    - [Initial Preparation](#initial)
    - [Client SMB Configuration](#smb)
    - [Connecting via SSH](#ssh)
    - [Useful Commands](#commands)
    - [Notes](#uploadnotes)
5. [Code](#code)
6. [Bug Fixing](#bugs)
7. [Useful References](#references)
8. [Glossary](#glossary)

## Introduction <a name="introduction"></a>
The Future Engineers challenge requires us to build a robot that can complete two tasks. The first task (called the qualifying task) requires the vehicle to make three laps of a square track autonomously, avoiding hitting any walls, as fast as possible and within a period of three minutes. The second task (called the final task) requires the vehicle to make another three laps in the same manner, while also avoiding green and red obstacles in its route and passing them from the correct side, depending on their color.

To accomplish these tasks we built a custom rear-axle driven robot, based on the Raspberry Pi SBC, which allows us to manipulate its motor functions freely, depending on input from numerous sensors located around the front of the vehicle. A wide range of sensors were used, so that the tasks could be completed as efficiently and as fast as possible. These sensors varied from ultrasonic distance sensors to cameras. All systems of the robot were powered by a custom power distribution system, stepping down voltages and supplying power to all components of the robot. Two seperate power systems were created to decrease load and improve performance and reliability, each with its own working voltage, to match the requirements of the devices it powers. In this guide we will go over all the systems in detail and explain the principles and functions behind the code used for the autonomous driving of the robot. Definitions for terms which may be unknown to some readers will be in the end of this guide.

## Hardware <a name="hardware"></a>
The hardware used in this project can be divided into four distinct categories. Power, motor, control and sensing hardware. All these systems work together to complete the required tasks. In this section we will look at how each separate category works to support the completed robot. A schematic is available in the `schemes` directory of this repository, to better understand the information in this section and to help you replicate the design on your own. There will also be references to this section in code, so it is possible to refer to this section to understand the working principles behind the code mentioned in [section 4](#code).

### Power Hardware <a name="hardwarepower"></a>
The robot is powered from two 18650 lithium ion cells connected in series, with a combined nominal voltage of 7.4V (3.7V each). The output of these cells is distributed to two buck converters, each powered on with a separate switch, which step down the voltage to a stable 5V for the Raspberry Pi and 5.5V for the other components. Each buck converter is rated for up to 3A of current, more than enough for the systems to run without any voltage drops. The 5V buck converter connects directly to the Raspberry Pi 3B+ with a USB cable, while the power from the 5.5V one is distributed using [WAGO terminal blocks](https://cpc.farnell.com/search?st=wago%20terminal&gs=true). The Raspberry Pi is equipped with a [polyfuse](https://elinux.org/Polyfuses_explained) and the 5V step-down converter has an input fuse to protect it from any electrical failures of components connected to GPIO. Both electrical subsystems share a common ground, to enable communication between the digital equipment which use both power sources.

### Motor Hardware <a name="hardwaremotor"></a>
There is a total of 2 motors on the robot. A NEMA 17 stepper motor is used to drive the back axle. This is connected to a TMC2209 stepper motor driver and allows us to precisely manipulate the speed of the robot and the distance which it travels, by setting the exact number of steps the motor will move at any given time. This drive motor is connected by pulley to a custom made gear on the back axle and features great quiet performance and reliability, making it the best option for its selected purpose. A 9g Metal Gear Servo is used to control the front axle steering of the robot. This motor provides a holding torque of around 2.8kg.cm and a speed of approximately 0.09s/60°, making it the perfect motor for use in a steering system. Its high torque and fast response time allow us to have precise and fast steering, a necessity in such a robot. It is controlled using a PWM signal from the GPIO of the Raspberry Pi and is powered from the 5.5V power source.

### Control Hardware <a name="hardwarecontrol"></a>
The Raspberry Pi 3B+ was our SBC of choice for this project. This stems from its great computing capabilities, which are necessary for use with OpenCV, the library used for accessing and processing the camera image data. The presence of great documentation for every part of its operation with our code was also a deciding factor in the decision over its use. It has 40 GPIO ports and a dedicated CSI camera connector, making it a great choice for use in such a project. All other components are connected to it via the GPIO, providing useful data and allowing manipulation of motors using code.

### Sensing Hardware <a name="hardwaresensing"></a>
In total 7 sensors of 4 different types are used to give the robot information about the track and its location. A camera is used to provide OpenCV with an image of the view from the front of the robot. The camera has an FOV of 160 degrees, giving us a view containing all areas necessary to compute the best path. It is connected to the Raspberry Pi by use of the dedicated CSI connection. Three HC-SR04 Ultrasonic Sensors are present on the robot, one for each side except the back of the robot. They are connected to the Raspberry Pi via the GPIO and a code function is used to calculate the distance from the walls on each side. More information on their working principle can be found [here](https://www.allaboutcircuits.com/industry-articles/understanding-the-basics-of-ultrasonic-proximity-sensors/). Two infrared obstacle sensors, for the left and right sides of the robot, are also present on the robot and could be used for wall detection, even though they are not in the current version of the code due to interference problems. A TCS3200 Color Sensor mounted facing the track under the robot is also present, although this as well is not used for any function as of the latest code version. It could however be used as an alternative way to count the number of laps travelled, by counting the colored lines present on the track surface.

### List of Hardware Used: <a name="hardwarelist"></a>
- 1x Raspberry Pi 3B+
- 2x 3400mAh Li-Ion 18650 Battery Cells
- 1x DFRobot DC-DC Fast Charge Module (5V)
- 1x DC-DC Adjustable Buck Converter
- 5x 3-terminal WAGO Terminal Blocks
- 1x 2-terminal WAGO Terminal Block
- 1x TMC2209 Stepper Motor Driver
- 1x NEMA 17 Stepper Motor
- 1x Active Buzzer
- 2x Infrared Obstacle Sensors
- 3x HC-SR04 Ultrasonic Distance Sensors
- 1x 9g Metal Gear Sensor
- 1x TCS3200 Color Sensor
- 1x Raspberry Pi Camera Module 5MP 160°

## Uploading Code <a name="upload"></a>
### Initial Preparation: <a name="initial"></a>
1. Start with the Raspberry Pi turned off.
2. Open a hotspot on your mobile phone or other device with the following characteristics:
- SSID: xxxx
- Password: xxxx
- Security: WPA2-Personal(AES)
- Client Isolation: Off (usually off by default).
3. Initially (optional) power on the motors by turning on the right switch. Then close the left switch, turning on the Raspberry Pi. Automatically the Raspberry Pi will try to connect to the network we created and will start the necessary services for ssh and smb.
4. Using an IP Scanner application ([iPhone](https://apps.apple.com/us/app/ubiquiti-wifiman/id1385561119), [Android](https://play.google.com/store/apps/details?id=com.myprog.netscan&gl=US)) find and note the IP address of the Raspberry Pi. *(In this guide we will denote it as x.x.x.x)*

### Preparing Linux / MacOS systems:
#### - Initial [smb](https://en.wikipedia.org/wiki/Server_Message_Block) configuration for file transfer *(Only once on each network)*: <a name="smb"></a>
1. Open a file browser of your choice. *(In this case Dolphin will be used, but the instructions are the same for all graphical programs.)*

![1](https://i.ibb.co/5RXzKZB/a1.png "1")

2. Right click on the left bar on the *Remote* or *Network* header of your program. Then select *Add Entry* or an equivalent option. ***(Attention! Click on the header and not on the Network item)***.

![2](https://i.ibb.co/cT8hRwv/a2.png "2")

3. In the dialog that will appear add a name of your choice, the IP address and the connection protocol in the format `smb://x.x.x.x` and if you want and have the option to do so, select an image for easier identification. In case there is a field for username and passwork enter the following details: `Username: xxx, Password: xxx`.

![3](https://i.ibb.co/Xs0kQBV/a3.png "3")

4. Now there will be an icon in the left bar of our program which will have the name and the image you have chosen. <a name="step4"></a>

![4](https://i.ibb.co/HDbdMXf/a4.png "4")

5. Clicking on it will bring up a folder. Open it. *(The name will be different)*

![5](https://i.ibb.co/V3MK98D/a5.png "5")

6. In the identification dialog that will appear enter the following details: `Username: xxx, Password: xxx` and press *OK* or *Connect*. *(If you have entered them before they may not be requested)*

![6](https://i.ibb.co/18p9CLp/a6.png "6")

7. From there go to *Desktop* and from there to the *xxx* folder, where our libraries are downloaded. There you can upload your code to run it in the next part of the guide. *(If you can't see Desktop in this folder, it will be in the home folder.)

#### - Connect via [ssh](https://en.wikipedia.org/wiki/Secure_Shell) to run code: <a name="ssh"></a>
1. Open your Terminal program, it will be different depending on the distribution, but the steps remain the same.

![1](https://i.ibb.co/n1yXcFh/b1.png "1")

2. There execute the command `ssh xxx@x.x.x.x`, where x.x.x.x is the IP address you found in [step 4](#step4) of the initial setup.
3. Immediately afterwards you will be prompted for the password, where you will enter `xxx`.

![3](https://i.ibb.co/Q8HXjTf/b3.png "3")

4. Once you press *Return/Enter* you will be logged in to the Raspberry Pi. Here you can run anything you want on the Raspberry Pi.

![4](https://i.ibb.co/0p55CYd/b4.png "4")

5. To find the code you uploaded you need to go to the *xxx* folder in *Desktop*. Do this by using the cd command and more specifically the `cd Desktop/xxx` command.
6. Here you will notice that the working directory has been changed to `~/Desktop/xxx`.

![6](https://i.ibb.co/Jm4G7mz/b6.png "6")

7. From there you can now run the code with the command `sudo python3 xxxx.py`, where `xxxx.py` is the name of the code file. Here you can also run any other command you need to fix your code and the Raspberry Pi.

#### Useful Commands <a name="commands"></a>
- To close the connection run the `exit` command,
- If you want to shut down the Raspberry Pi use the command `sudo shutdown 0`.
- To reboot immediately another useful command is `sudo reboot now`.
- To stop the execution of the code it is sufficient to use the keybind `Ctrl+C`

#### Notes <a name="uploadnotes"></a>
- Details denoted with `xxx` need to be filled in by the user.

## Code <a name="code"></a>


## Bug Fixing <a name="bugs"></a>
- **The motor doesn't operate normally, it runs in a random direction every time:** Make sure that the login shell over serial is disabled, then reboot.

## Useful References <a name="references"></a>
1. [TMC_2209 Raspberry Pi Library GitHub](https://github.com/Chr157i4n/TMC2209_Raspberry_Pi)
2. [Wiring Schematic](https://github.com/EliaKr/new-school-robotics-fe/blob/main/schemes/schematic.pdf)

## Glossary <a name="glossary"></a>
- FE: The Future Engineers category of the World Robotics Olympiad
- Main Branch: The main branch of this github repository
- SBC: Single Board Computer
- Buck Converter: A device which takes in a higher voltage and converts it to a lower one by use of efficient rapid switching.
- WAGO Terminal Blocks: A type of cage clamp connector which allows for easy reversible connection splicing.
- Polyfuse: A type of self-resettable fuse made out of polymer.
- GPIO: The General Purpose Input and Output pins of the Raspberry Pi. They allow for control of other hardware via a variety of modes, such as PWM and I2C, but also typical analog and digital operation.
- Stepper Motor: A type of brushless motor allowing the user to precisely define its angle and speed of rotation.
- Servo Motor: A type of motor which allows the user to define the angle at which it is positioned by use of a PWM signal.
- FOV: Field of View, a measure of the area covered by the camera.
