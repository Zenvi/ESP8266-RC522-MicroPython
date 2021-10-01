import mfrc522
from os import uname

def do_write(block_index, data):

    if uname()[0] == 'WiPy':
        rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")

    print("")
    print("Place card before reader to write to block {}".format(block_index))
    print("")

    try:
        while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid  : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, block_index, key, raw_uid) == rdr.OK:
                            stat = rdr.write(block_index, data)
                            # stat = rdr.write(block_index, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print("Data written to card")
                            else:
                                print("Failed to write data to card. ERROR STATUS: ", stat)
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")
        
if __name__ == '__main__':
    block_index = eval(input('Which block you intend to WRITE? Please input a number ranged 1~63: '))
    data = eval(input('What data you intend to WRITE to block {}? Please input a list: '))
    do_write(block_index, data)