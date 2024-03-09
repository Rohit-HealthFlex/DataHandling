import asyncio
from bleak import BleakScanner, BleakClient


class SensorStreamHelper:
    def __init__(self):
        self.device_mac_address = "FA:21:24:A3:8A:02"
        self.service_uuid = "0000ffe5-0000-1000-8000-00805f9a34fb"
        self.characteristic_uuid = "0000FFE4-0000-1000-8000-00805F9A34FB"
        self.stream_opt = None

    def parse_data_packet(self, data_packet):
        axL, axH, ayL, ayH, azL, azH, wxL, wxH, wyL, wyH, wzL, wzH, RollL, RollH, PitchL, PitchH, YawL, YawH = data_packet[
            2:20]
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

    async def connect_and_receive_notifications(self):
        async with BleakClient(self.device_mac_address) as client:
            print(
                f"Connected to device with MAC address: {self.device_mac_address}")

            def notification_handler(sender, data):
                self.stream_opt = self.parse_data_packet(data)
                # print(f"Received notification: {self.stream_opt}")
                # self.stream_opt

            await client.start_notify(self.characteristic_uuid,
                                      notification_handler)
            await asyncio.sleep(10)

            await client.stop_notify(self.characteristic_uuid)

            print("Data streaming stopped")

    async def main(self):
        await self.connect_and_receive_notifications()


class SensorStreamer(SensorStreamHelper):
    def __init__(self):
        super(SensorStreamer, self).__init__()

    def stream(self):
        yield self.stream_opt


if __name__ == "__main__":
    obj = SensorStream()
    val = obj.stream()
    print(val)
