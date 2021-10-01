import mfrc522
from os import uname


def do_read(block_index=0):

    if uname()[0] == 'WiPy':
        rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")

    print("")
    print("Place card before reader to read from block {}".format(block_index))
    print("")

    try:
        while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, block_index, key, raw_uid) == rdr.OK:
                            print("Block {} data: {}".format(block_index, rdr.read(block_index)))
                            rdr.stop_crypto1()
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")
        
        
if __name__ == '__main__':
    block_index = eval(input('Which block you intend to READ? Please input a number ranged 0~63: '))
    do_read(block_index)