# ESP8266  + RC522 + MicroPython

Note: This is a modified version originated from: https://github.com/wendlers/micropython-mfrc522

## 1. Preparation

+ Get an ESP8266 (Mine is a 4MB flash one, and sometimes there is not enough memory to allocate)

+ Get a RC522 high frequency RFID reader

+ Connect ESP8266 and RC522 according to :

  | Signal | GPIO ESP8266 |
  | :----: | :----------: |
  |  sck   |      0       |
  |  mosi  |      2       |
  |  miso  |      4       |
  |  rst   |      5       |
  |  sda   |      14      |

+ Install a Python IDE which is capable of calling interpreters from coms: https://thonny.org/

## 2. MicroPythonize ESP8266

+ `pip install esptool`

+ `esptool --port COM4 erase_flash`

+ `esptool --port COM4 --baud 460800 write_flash --flash_size=detect -fm dout 0 esp8266-20210902-v1.17.bin`

  Note: `COM4` is the com connected to ESP8266 in MY COMPUTER; `esp8266-20210902-v1.17.bin` is just the MicroPython image to be flashed; Modify these two parameters according to your own situation.

+ Open up a Serial Port Assist software to test whether your ESP8266 can run python codes. If yes, proceed to the next step (Below is a positive instance)

  <img src=".\Readme-pics\image-20210921160127679.png" alt="image-20210921160127679" style="zoom:50%;" />

## 3. Put Python Scripts into ESP8266

+ Go to folder `./Python-Scripts`, put `rc522.py`, `test.py`, `utils.py` to ESP8266 through Thonny
+ Run `test.py`

