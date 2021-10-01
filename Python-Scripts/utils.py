import rc522
from os import uname

def do_read(block_index=0,
            keyA=(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
            keyB=(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
            MODE='A'):

    # Check inputs:
    if (type(block_index) is not int) or (block_index > 63) or (block_index < 0):
        print('Please input a block numbered 0~63')
        return
    if len(keyA) != 6 or len(keyB) != 6:
        print('Please input keyA or keyB in the correct format')
        return
    if MODE not in ['A', 'B']:
        print('Please select the correct authentication mode: A or B')
        return

    # Check Platform
    if uname()[0] == 'WiPy':
        rdr = rc522.RC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = rc522.RC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")

    # Prepare to read
    print("")
    print("Place card before reader to read from block {}".format(block_index))
    print("")

    try:
        while True:

            # Request cards
            (stat, tag_type) = rdr.request(rdr.PICC_REQIDL)

            if stat == rdr.OK:

                # Anti-collision
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:

                    # Print the uid of the detected card
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    # Select card
                    if rdr.select_tag(raw_uid) == rdr.OK:

                        # Authentication
                        mode = rdr.PICC_AUTHENT1A if MODE == 'A' else rdr.PICC_AUTHENT1B
                        if rdr.auth(mode, block_index, keyA, keyB, raw_uid) == rdr.OK:

                            # Read data
                            print("Block {} data: {}".format(block_index, rdr.read(block_index)))

                            rdr.stop_crypto1()

                            msg = input('try again? (Y/N)')
                            if msg in ['Y', 'y']:
                                pass
                            else:
                                break

                        else:
                            print("Authentication error")

                            msg = input('try again? (Y/N)')
                            if msg in ['Y', 'y']:
                                pass
                            else:
                                break
                    else:
                        print("Failed to select tag")

                        msg = input('try again? (Y/N)')
                        if msg in ['Y', 'y']:
                            pass
                        else:
                            break

    except KeyboardInterrupt:
        print("Bye")


def do_write(block_index,
             data,
             keyA=(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
             keyB=(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
             MODE='A'):
    
    # Check inputs
    if (type(block_index) is not int) or (block_index > 63) or (block_index < 1):
        print('Please input a block numbered 1~63')
        return
    if len(keyA) != 6 or len(keyB) != 6:
        print('Please input keyA or keyB in the correct format')
        return
    if MODE not in ['A', 'B']:
        print('Please select the correct authentication mode: A or B')
        return
    if len(data) != 16:
        print('Please input the data with the correct format!')
        return
    
    # Check platform
    if uname()[0] == 'WiPy':
        rdr = rc522.RC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = rc522.RC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")
    
    # Prepare to write
    print("")
    print("Place card before reader to write to block {}".format(block_index))
    print("")

    try:
        while True:
            
            # Request card
            (stat, tag_type) = rdr.request(rdr.PICC_REQIDL)

            if stat == rdr.OK:
                
                # Anti-collision
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    
                    # Print out the uid of the gotten card
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid  : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")
                    
                    # Select card
                    if rdr.select_tag(raw_uid) == rdr.OK:
                        
                        # Authentication
                        mode = rdr.PICC_AUTHENT1A if MODE == 'A' else rdr.PICC_AUTHENT1B
                        if rdr.auth(mode, block_index, keyA, keyB, raw_uid) == rdr.OK:
                            
                            # Write block
                            stat = rdr.write(block_index, data)
                            
                            rdr.stop_crypto1()
                            
                            if stat == rdr.OK:
                                print("Data written to card")

                                msg = input('try again? (Y/N)')
                                if msg in ['Y', 'y']:
                                    pass
                                else:
                                    break

                            else:
                                print("Failed to write data to card.")

                                msg = input('try again? (Y/N)')
                                if msg in ['Y', 'y']:
                                    pass
                                else:
                                    break

                        else:
                            print("Authentication error")

                            msg = input('try again? (Y/N)')
                            if msg in ['Y', 'y']:
                                pass
                            else:
                                break

                    else:
                        print("Failed to select tag")

                        msg = input('try again? (Y/N)')
                        if msg in ['Y', 'y']:
                            pass
                        else:
                            break

    except KeyboardInterrupt:
        print("Bye")


def do_value(block_index,
             data,
             cmd = 'increment',
             keyA=(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
             keyB=(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
             MODE='A'):
    '''
    E-Wallet operations: increment/decrement a block
    NOTE: a block is only able to be incremented/decremented after it has been initialized by the E-Wallet format:
    value(4B), value_b(4B), value(4B), block_index(1B), block_index_b(1B), block_index(1B), block_index_b(1B)
    BEWARE: LSB of value goes to the LHS of the 4B cache

    PARAMETERS:
        block_index: which block you want to operate, ranged from 1~63, except blocks indexed 3,7,11,...,63
        data: how much you wish to increment/decrement; 4B length, LSB comes first
    '''
    # Check inputs
    if (type(block_index) is not int) or (block_index > 63) or (block_index < 1) or ((block_index+1)%4==0):
        print('Please input a block numbered 1~63')
        return
    if len(keyA) != 6 or len(keyB) != 6:
        print('Please input keyA or keyB in the correct format')
        return
    if MODE not in ['A', 'B']:
        print('Please select the correct authentication mode: A or B')
        return
    if len(data) != 4:
        print('Please input the data with the correct format!')
        return
    if cmd not in ['increment', 'decrement']:
        print('Please input the correct commad! (increment/decrement)')
        return

    # Check platform
    if uname()[0] == 'WiPy':
        rdr = rc522.RC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = rc522.RC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")

    # Prepare to do value operations
    print("")
    print("Place card before reader to {} block {}".format(cmd, block_index))
    print("")

    try:
        while True:

            # Request card
            (stat, tag_type) = rdr.request(rdr.PICC_REQIDL)

            if stat == rdr.OK:

                # Anti-collision
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:

                    # Print out the uid of the gotten card
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid  : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    # Select card
                    if rdr.select_tag(raw_uid) == rdr.OK:

                        # Authentication
                        mode = rdr.PICC_AUTHENT1A if MODE == 'A' else rdr.PICC_AUTHENT1B
                        if rdr.auth(mode, block_index, keyA, keyB, raw_uid) == rdr.OK:

                            # Operate block
                            stat = rdr.value(mode=cmd, addr=block_index, data=data)

                            rdr.stop_crypto1()

                            if stat == rdr.OK:
                                print("Block {} {}ed!".format(block_index, cmd))

                                msg = input('try again? (Y/N)')
                                if msg in ['Y', 'y']:
                                    pass
                                else:
                                    break
                            else:
                                print("Failed to increment block {}.".format(block_index))

                                msg = input('try again? (Y/N)')
                                if msg in ['Y', 'y']:
                                    pass
                                else:
                                    break
                        else:
                            print("Authentication error")

                            msg = input('try again? (Y/N)')
                            if msg in ['Y', 'y']:
                                pass
                            else:
                                break
                    else:
                        print("Failed to select tag")

                        msg = input('try again? (Y/N)')
                        if msg in ['Y', 'y']:
                            pass
                        else:
                            break

    except KeyboardInterrupt:
        print("Bye")


def CtlBlock_2_CtlBits(block_data):

    assert len(block_data) == 16, 'Wrong format of input data'

    CtlBytes = block_data[6:9]

    lines = []
    for line in CtlBytes:
        lines.append('{:08b}'.format(line))

    X3 = int(lines[1][0]), int(not int(lines[0][0])), int(lines[2][0])
    X2 = int(lines[1][1]), int(not int(lines[0][1])), int(lines[2][1])
    X1 = int(lines[1][2]), int(not int(lines[0][2])), int(lines[2][2])
    X0 = int(lines[1][3]), int(not int(lines[0][3])), int(lines[2][3])

    return X0, X1, X2, X3


def CtlBits_2_CtlBlock(X):

    X3 = X[3]
    X2 = X[2]
    X1 = X[1]
    X0 = X[0]

    L1 = str(int(not X3[1])) + str(int(not X2[1])) + str(int(not X1[1])) + str(int(not X0[1])) + \
         str(int(not X3[0])) + str(int(not X2[0])) + str(int(not X1[0])) + str(int(not X0[0]))
    L2 = str(X3[0]) + str(X2[0]) + str(X1[0]) + str(X0[0]) + \
         str(int(not X3[2])) + str(int(not X2[2])) + str(int(not X1[2])) + str(int(not X0[2]))
    L3 = str(X3[2]) + str(X2[2]) + str(X1[2]) + str(X0[2]) + str(X3[1]) + str(X2[1]) + str(X1[1]) + str(X0[1])

    L1 = '0b' + L1
    L2 = '0b' + L2
    L3 = '0b' + L3

    return eval(L1), eval(L2), eval(L3)


def E_Wallet_init(block_index, initial_value):

    inv_dict = {'0': 'f',
                '1': 'e',
                '2': 'd',
                '3': 'c',
                '4': 'b',
                '5': 'a',
                '6': '9',
                '7': '8',
                '8': '7',
                '9': '6',
                'a': '5',
                'b': '4',
                'c': '3',
                'd': '2',
                'e': '1',
                'f': '0'}

    value = '{:08x}'.format(initial_value)
    value = value[-2] + value[-1] + value[-4] + value[-3] + value[-6] + value[-5] + value[-8] + value[-7]

    value_b = ''
    for x in value:
        value_b += inv_dict[x]

    addr = '{:02x}'.format(block_index)

    addr_b = ''
    for x in addr:
        addr_b += inv_dict[x]

    data = [eval('0x'+value[0:2]), eval('0x'+value[2:4]), eval('0x'+value[4:6]), eval('0x'+value[6]+value[7]),
            eval('0x'+value_b[0:2]), eval('0x'+value_b[2:4]), eval('0x'+value_b[4:6]), eval('0x'+value_b[6]+value_b[7]),
            eval('0x' + value[0:2]), eval('0x' + value[2:4]), eval('0x' + value[4:6]), eval('0x' + value[6] + value[7]),
            eval('0x'+addr), eval('0x'+addr_b), eval('0x'+addr), eval('0x'+addr_b)]

    print('Write the following data to block {}:'.format(block_index))
    print(data)


def decimal_2_4B(d):

    '''
    The function converts a decimal value to the hexadecimal format suitable for incrementing/decrementing a block
    '''

    data = '{:08x}'.format(d)
    data = data[-2] + data[-1] + data[-4] + data[-3] + data[-6] + data[-5] + data[-8] + data[-7]
    data = [eval('0x' + data[0:2]), eval('0x' + data[2:4]), eval('0x' + data[4:6]), eval('0x' + data[6] + data[7])]

    print('if you want to increment/decrement a block by a value of {}, you should send the following data to the card:'.format(data))
    print(data)
