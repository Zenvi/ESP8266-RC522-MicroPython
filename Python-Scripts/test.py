if __name__ == '__main__':

    action = input('What do you want to do with your card? Read(R), Write(W), Increment(+), or Decrement(-):')

    if action == 'R':
        from utils import do_read
        block_index = eval(input('Which block you intend to READ? Please input a number ranged 0~63: '))
        do_read(block_index)

    elif action == 'W':
        from utils import do_write
        block_index = eval(input('Which block you intend to WRITE? Please input a number ranged 1~63: '))
        data = eval(input('What data you intend to WRITE to block {}? Please input a list: '))
        do_write(block_index, data)

    elif action == '+':
        from utils import do_value
        block_index = eval(input('Which block you intend to INCREMENT? Please input a number ranged 1~63: '))
        data = eval(input('How much you want block {} to increment? Please input a list: '))
        do_value(block_index, data, cmd='increment')

    elif action == '-':
        from utils import do_value
        block_index = eval(input('Which block you intend to DECREMENT? Please input a number ranged 1~63: '))
        data = eval(input('How much you want block {} to decrement? Please input a list: '))
        do_value(block_index, data, cmd='decrement')
