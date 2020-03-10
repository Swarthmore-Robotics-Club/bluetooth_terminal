import BluetoothTerminal from './bluetooth_terminal'



class FakeTerminal extends BluetoothTerminal
{
    list_devices()
    {
        return (
            {
                'name': "HC-05-Leader",
                'addr': "023:231:123"
            }
        )
    }


    discover_devices()
    {
        return this.list_devices()
    }
}


export default FakeTerminal