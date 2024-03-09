import asyncio
from bleak import BleakScanner, BleakClient

# Run this function to find devices and thier MAC ID


def parse_data_packet(data_packet):
    # Unpack the data_packet based on the format described in the datasheet
    axL, axH, ayL, ayH, azL, azH, wxL, wxH, wyL, wyH, wzL, wzH, RollL, RollH, PitchL, PitchH, YawL, YawH = data_packet[
        2:20]
    # Calculate the acceleration values
    ax = ((axH << 8) | axL) / 32768 * 16  # Acceleration in g (9.8 m/s^2)
    ay = ((ayH << 8) | ayL) / 32768 * 16  # Acceleration in g (9.8 m/s^2)
    az = ((azH << 8) | azL) / 32768 * 16  # Acceleration in g (9.8 m/s^2)
    # Calculate the angular velocity values
    wx = ((wxH << 8) | wxL) / 32768 * 2000  # Angular velocity in °/s
    wy = ((wyH << 8) | wyL) / 32768 * 2000  # Angular velocity in °/s
    wz = ((wzH << 8) | wzL) / 32768 * 2000  # Angular velocity in °/s
    # Calculate the roll, pitch, and yaw angles
    Roll = ((RollH << 8) | RollL) / 32768 * 180  # Roll angle in °
    Pitch = ((PitchH << 8) | PitchL) / 32768 * 180  # Pitch angle in °
    Yaw = ((YawH << 8) | YawL) / 32768 * 180  # Yaw angle in °
    return ax, ay, az, wx, wy, wz, Roll, Pitch, Yaw


async def find():
    devices = await BleakScanner.discover()
    for device in devices:

        # Prints device names
        print(device)

asyncio.run(find())

# And then add MAC address of the device to this variable
device_mac_address = "FA:21:24:A3:8A:02"

# UUIDs for the service and characteristic
service_uuid = "0000ffe5-0000-1000-8000-00805f9a34fb"
characteristic_uuid = "0000FFE4-0000-1000-8000-00805F9A34FB"


async def connect_and_receive_notifications():
    async with BleakClient(device_mac_address) as client:
        print(f"Connected to device with MAC address: {device_mac_address}")

        def notification_handler(sender, data):
            data = parse_data_packet(data)
            print(f"Received notification: {data}")

        await client.start_notify(characteristic_uuid, notification_handler)

        # Stream data for 30 seconds (adjust as needed)
        await asyncio.sleep(30)

        await client.stop_notify(characteristic_uuid)

        print("Data streaming stopped")


async def main():
    await connect_and_receive_notifications()

asyncio.run(main())
