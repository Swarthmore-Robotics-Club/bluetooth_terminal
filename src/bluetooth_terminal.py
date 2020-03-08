import bluetooth
import tinydb
#import zmq ---> for later use for message passing protocol
import threading

import os 
# Change working directory to file directory for debbugging
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class BluetoothTerminal():
    """
    The BluetoothTerminal is meant to encapsulate a CLI interface to communicate with external
    serial bluetooth devices (HC-XX series of bluetooth hardware modules)

    """
    def __init__(self, terminal_mode = False):
        # load past bluetooth modules from json file
        cached_bluetooth_db = tinydb.TinyDB("database/bluetooth.json")
        self.cached_bluetooth_devices = []
        for dictionary in cached_bluetooth_db:
            bluetooth_addr = dictionary['addr']
            bluetooth_name = dictionary['name']
            self.cached_bluetooth_devices.append((bluetooth_addr, bluetooth_name))
        # Sometimes one might just want to use this for message passing
        self.terminal_mode = terminal_mode
        self.bluetooth_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.discovered_bluetooth_devices = []
        self.recv_daemons = []
        self.port = 1
        self.connected = False
        self.__buffer = ""
        # for consumer producer problem
        self.condition = threading.Condition()

        return

    def connect_from_name(self, target_name):
        """
        given a bluetooth devices name, it connects to it
        """

        self.print_to_terminal("Looking for bluetooth devices....")

        nearby_devices = bluetooth.discover_devices()
        target_address = None
        for bdaddr in nearby_devices:
            if target_name == bluetooth.lookup_name( bdaddr ):
                
                target_address = bdaddr
                self.bluetooth_socket.connect((target_address, self.port))
                break

        if target_address != None:  
            self.print_to_terminal(f"Connected bluetooth device with address {target_address}")
            
        else:
            self.print_to_terminal(f"Failed to connect to bluetooth device with name: {target_name}")

        return target_address != None

    def connect_from_list(self, index):
        """
            Connects to list of bluetooth devices already found by using the discover_devices command
        """

        cached_devices = self.__choose_cached_list()

        if index > len(cached_devices) - 1:
            self.print_to_terminal("invalid index!")
            return False

        bluetooth_device_addr =cached_devices[index][0]

        try:
            self.bluetooth_socket.connect((bluetooth_device_addr, self.port))
            self.connected = True
            return True

        except bluetooth.BluetoothError:
            return False
    
    def print_to_terminal(self, string):
        """
        print function that only works while in terminal/CLI mode \n
        Might have a plan to use this to make a friendlier GUI version of 
        the terminal this means eliminating printing unless necessary
        """
        if self.terminal_mode:
            print(string)

    def close(self):
        #TODO close bluetooth socket maybe but actually...

        return 

    def send(self, data):
        #TODO might need to encode data for anything larger than a character long
        self.bluetooth_socket.send(data)

        return

    def recv_daemon(self):
        """
        a background_thread function that passively listens for bluetooth signals
        """
        while self.connected:
            data = self.bluetooth_socket.recv(1024)

            # TODO add race condition shtuff
            self.__buffer += data.decode("utf-8") 

    def read_buffer(self):
        #TODO RACE CONDITION SHTUFF GOES HERE
        to_return = self.__buffer
        self.__buffer = ""
        return  to_return

    def print_daemon(self):
        #TODO DID SOMEONE SAY RACE CONDITION?!??!
        # should work if we just fix the read_buffer race condition
        to_print = self.read_buffer()
        self.print_to_terminal(to_print)
        return

    def attach_listener(self):
        # create a background thread that listens for bluetooth messages 
        listener_func = threading.Thread(target= self.recv_daemon)
        listener_func.setDaemon(True)
        listener_func.start()
        return

    def attach_print(self):
        # create a background thread that actively 
        print_func = threading.Thread(target=self.print_daemon)
        print_func.setDaemon(True)
        print_func.start()
        return

    def list_devices(self):

        cached_devices = self.__choose_cached_list()
        if not cached_devices:
            self.print_to_terminal("found no devices! try searching for them.")

        self.print_to_terminal("found the following devices:")

        for i in range(len(cached_devices)):
                self.print_to_terminal(f"\nindex: {i} addr: {cached_devices[i][0]}  name: {cached_devices[i][1]} ")
    
    def discover_devices(self):

        self.print_to_terminal("Looking for devices")

        cached_bluetooth_db = tinydb.TinyDB("database/bluetooth.json")
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        
        if len(nearby_devices) > 0:
            self.print_to_terminal("found the following bluetooth devices")
            for i in range(len(nearby_devices)):
                bluetooth_addr = nearby_devices[i][0]
                bluetooth_name = nearby_devices[i][1]
                # search db to see if we can cached bluetooth addrr
                bluetooth_document = tinydb.Query()
                if len( cached_bluetooth_db.search(bluetooth_document.name ==bluetooth_name)) == 0:
                    document = {
                        'addr': bluetooth_addr,
                        'name' : bluetooth_name
                    }
                    cached_bluetooth_db.insert(document)
                self.print_to_terminal(f"index: {i} addr: {bluetooth_addr}  name: {bluetooth_name} ")
            self.discovered_bluetooth_devices = nearby_devices
        else:
            self.print_to_terminal("failed to find any bluetooth devices")
        return

    def can_read(self):

        return len(self.__buffer) == 0

    def __choose_cached_list(self):

        """
        Theres two ways to cache a device and we need to choose one to show users

        1) persistent cache from a json based database to avoid looking for devices everytime
        2) a volatile cache from returning results of reading available devices in discover_devices method
        """

        # give preference to latest set of bluetooth devices discovered
        if len( self.discovered_bluetooth_devices) > 0:
            return self.discovered_bluetooth_devices
        # else if we have a cached from database
        elif len(self.cached_bluetooth_devices) > 0:
            return self.cached_bluetooth_devices

        return []
