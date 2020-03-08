#import zmq # for later 
from time import sleep as do_the_thing
from bluetooth_terminal import BluetoothTerminal


# singleton terminal instance
bluetooth_terminal = BluetoothTerminal(terminal_mode=True) # yes we can use *args for switch statements or....


def print_intro(first_intro = True):
    # i thought intro would be possibly more grandiose.  happens
    if first_intro:
        print("Opening bluetooth terminal")
    return

def query_input():

    available_commands = ["discover devices","list_past_devices", "connect from list", "type commands"]
    print("Available Commands")

    for i,command in enumerate(available_commands):
        print(f"{i+1}) {command} ")
    
    return

def connect_from_list():
    global bluetooth_terminal

    print("choose a device from list bellow to connect to\n")
    bluetooth_terminal.list_devices()

    while 1:
        user_input = input("\n> ")

        if user_input.isdigit():
            break
        else:
            print("input a valid number")
    index = int(user_input)
    success = bluetooth_terminal.connect_from_list(index)

    if not success:
        print("failed to connect to bluetooth device...")
    else:
        print("connected")


def talk_to_terminal():
    """
    Allows user to communicate directly to HC-05 and effectively Arduino as if they were connected over serial.
    """
    global bluetooth_terminal

    bluetooth_terminal.attach_listener()
    bluetooth_terminal.attach_print() 
    print("now talking to bluetooth terminal. Input any valid commands. For a list, input -h, To quit press -q")

    while 1:
        user_input = input("")
        if user_input == "-h":
            print("input 'h' for hello world")
        elif user_input == "-q" or user_input == "-Q":
            break

        else:
            bluetooth_terminal.send(user_input)



    return


def main():
    """
    A simple python CLI (command-line-interface) for the bluetooth terminal.
    """
    # we can all just agree not to randomly turn this variable into a list and everything will be fine
    global bluetooth_terminal # singleton i swear 
    print_intro()
    # switch case statement 
    input_dict = {
        "1":  bluetooth_terminal.discover_devices,
        "2": bluetooth_terminal.list_devices,
        "3": connect_from_list,
        "4": talk_to_terminal
    }

    while 1:
        query_input()
        user_input = input("\n> ")
        if user_input == 'q' or user_input == 'Q':
            bluetooth_terminal.close()
            break
        try:
            func = input_dict[user_input]
            func()
        except KeyError:
            print("Please input a valid number")

        
if __name__ == "__main__":

    main()
