const bluetooth = require('node-bluetooth');



class BluetoothTerminal
{
    constructor(terminal_mode = false)
    {
        this.bluetooth_device = new bluetooth.DeviceINQ();
        this.terminal_mode = terminal_mode;

    }

    connectFromList(index)
    {

    }

    print_to_terminal(message)
    {
        if (this.terminal_mode)
        {
            console.log(message)
        }
    }

    close()
    {

    }

    send()
    {

    }

    read_buffer()
    {

    }

    list_devices()
    {

    }

    list_paired_devices()
    {
        return this.bluetooth_device.listPairedDevices();
    }

    discover_devices()
    {

    }
}


export default BluetoothTerminal