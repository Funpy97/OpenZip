# OpenZip
![](https://raw.githubusercontent.com/Funpy97/OpenZip/11742e5176ab5836a2b5924c6c9c2c35e44ad5de/assets/images/logo/svg/logo-no-background.svg)

Crack a zip file with the brute force and the distributed computing.

![](https://github.com/Funpy97/OpenZip/blob/master/data/assets/images/gifs/app.gif?raw=true)

## Features
|**Feature**|**Description**|**Status**|
|--|--|--|
| Simple to use.| Thanks to its intuitive graphical interface this tool does not require any particular technical knowledge to be used. |✅ |
| AES zip file.| Support for 128, 192 or 256 bits encrypted zip files.| ✅ |
| Secure connections. | Connections between the server and the clients are kept safe by an hybrid cryptosystem (RSA-4096 + AES-256)| ✅ |
| Custom multiprocessing. | The client decides how much power to use for the cracking process by setting the number of cores involved. | ✅ |
| Automatic servers discovering. | In the client mode the software will discover automatically all the server sessions in the local network, you don't need to know the IP address to connect. | ✅ |

## Installation
- Clone the git repository  `git clone https://github.com/Funpy97/OpenZip.git`
- Move to the folder just created by git `cd OpenZip`
- Create a virtual environment `python -m venv venv`
- Activate the virtual environment `./venv/Scripts/activate`
- Install the requirements with pip `pip install -r requirements.txt`
- Run the app `python openzip.py`

This installation is tested only on Windows but it could work also on Linux and Mac OS just changing the commands according to the OS.

## TODO
|**TODO**|**Description**|**Status**|
|--|--|--|
| Android support. | Re-writing the GUI, using Kivy, to extend the application on the android devices. | ❎ |
| Password's recovery system when a client close the connection. | When a client close the connection with the server before the completion of the password's generator assigned to it the system should consider that generator not completed and send it to another client. | ❎ |
| Server can push out the clients. | The user that runs the software in server mode can push out the clients manually. | ❎ |
| Cross platform networking. | Implement a cross platform algorithm to determinate the subnet mask and calculate the hosts to scan in the local network (now only Windows is supported, the default subnet mask for all the others platform is 255.255.255.0). | ❎ |
| Create a logo. | Create a logo for the application and for the project. | ❎ |
