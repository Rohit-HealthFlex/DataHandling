import asyncio
import os
from bleak import BleakClient
import pandas as pd
import time

# MAC addresses of the devices
device_mac_addresses = ["E0:3A:DF:63:BD:23", "E5:96:EB:33:1A:DD"]

# UUIDs for the service and characteristic
service_uuid = "0000ffe5-0000-1000-8000-00805f9a34fb"
characteristic_uuid = "0000FFE4-0000-1000-8000-00805F9A34FB"
null_value = 0

# Function to parse received data packet
def parse_data_packet(data_packet):
    axL, axH, ayL, ayH, azL, azH, wxL, wxH, wyL, wyH, wzL, wzH, RollL, RollH, PitchL, PitchH, YawL, YawH = data_packet[2:20]
    ax = ((axH << 8) | axL) / 32768 * 16
    ay = ((ayH << 8) | ayL) / 32768 * 16
    az = ((azH << 8) | azL) / 32768 * 16
    wx = ((wxH << 8) | wxL) / 32768 * 2000
    wy = ((wyH << 8) | wyL) / 32768 * 2000
    wz = ((wzH << 8) | wzL) / 32768 * 2000
    Roll = ((RollH << 8) | RollL) / 32768 * 180
    Pitch = ((PitchH << 8) | PitchL) / 32768 * 180
    Yaw = ((YawH << 8) | YawL) / 32768 * 180
    return ax, ay, az, wx, wy, wz, Roll, Pitch, Yaw

async def connect_and_receive_notifications(device_mac_address):
    df = pd.DataFrame(columns=["Time", "Device name", "Chip Time()", "Acceleration X(g)", 
                               "Acceleration Y(g)", "Acceleration Z(g)", "Angular velocity X(°/s)", 
                               "Angular velocity Y(°/s)", "Angular velocity Z(°/s)", 
                               "Angle X(°)", "Angle Y(°)", "Angle Z(°)", 
                               "Gyroscope X", "Gyroscope Y", "Gyroscope Z"])

    async with BleakClient(device_mac_address) as client:
        print(f"Connected to device with MAC address: {device_mac_address}")
        alternate = 0  # Variable to alternate between sensors

        def notification_handler(sender, data):
            nonlocal alternate
            # Parse data packet
            ax, ay, az, wx, wy, wz, Roll, Pitch, Yaw = parse_data_packet(data)
            data_in = {"Time": time.time(),
                       "Device name": device_mac_address,
                       "Chip Time()": null_value,
                       "Acceleration X(g)": ax, 
                       "Acceleration Y(g)": ay, 
                       "Acceleration Z(g)": az,
                       "Angular velocity X(°/s)": null_value,
                       "Angular velocity Y(°/s)": null_value,
                       "Angular velocity Z(°/s)": null_value,
                       "Angle X(°)": Pitch,
                       "Angle Y(°)": Roll,
                       "Angle Z(°)": Yaw,
                       "Gyroscope X": wx,
                       "Gyroscope Y": wy,
                       "Gyroscope Z": wz,
                       }

            nonlocal df
            df_row = pd.DataFrame(data_in, index=[0])
            if alternate == 0:
                df = pd.concat([df, df_row], ignore_index=True)
            else:
                df = pd.concat([df_row, df], ignore_index=True)
            alternate = 1 - alternate  # Toggle between 0 and 1

            print(f"Accelerometer (g): X={ax}, Y={ay}, Z={az}")
            print(f"Gyroscope (°/s): X={wx}, Y={wy}, Z={wz}")
            print(f"Orientation (°): Roll={Roll}, Pitch={Pitch}, Yaw={Yaw}\n\n")

        await client.start_notify(characteristic_uuid, notification_handler)

        await asyncio.sleep(10)  # Stream data for 30 seconds (adjust as needed)

        await client.stop_notify(characteristic_uuid)

        print("Data streaming stopped")
        return df

async def main():
    dfs = await asyncio.gather(*[connect_and_receive_notifications(mac_address) for mac_address in device_mac_addresses])
    final_df = pd.concat(dfs)
    final_df["Time"] = pd.to_datetime(final_df["Time"], unit='s')  # Convert Time to datetime
    final_df = final_df.sort_values(by='Time')  # Sort DataFrame based on Time
    final_df.to_csv('data_store.csv', mode='w', index=False)

asyncio.run(main())
