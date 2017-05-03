# -*- coding: utf-8 -*-
# for more information on Plantower sensor refer to
# Appendix I:PMS7003 transport protocol-Active Mode at technical specification
import serial
import time
import requests
import json

api_endpoint = 'https://api.measureofquality.com/v2/nodes/push'
data_size = 32  # (32 bytes) refer to Appendix I:PMS7003
rate = 9600 # bps

sensors = dict(
    test_plantower_7003_1='/dev/ttyUSB0',
    test_plantower_7003_2='/dev/ttyUSB1'
)


def read_data(device, uuid, size=32):
    one_byte=''

    try:
        while one_byte != '424d001c':
            one_byte = device.read(4)
            one_byte = one_byte.encode("hex")
    except ():
        return None

    data_bin = device.read(size)

    data_hex = one_byte + data_bin.encode("hex")
    pm1 = int(data_hex[8:12], 16)  # PM1.0 concentration unit μg/m3(CF=1, standard particle)
    pm25 = int(data_hex[12:16], 16)  # PM2.5 concentration unit μg/m3(CF=1, standard particle)
    pm10 = int(data_hex[16:20], 16)  # PM10 concentration unit μg/m3(CF=1,standard particle)
    pm1atm = int(data_hex[20:24], 16)  # PM1.0 concentration unit μg/m3(under atmospheric environment)
    pm25atm = int(data_hex[24:28], 16)  # PM2.5 concentration unit μg/m3(under atmospheric environment)
    concentr_atm = int(data_hex[28:32], 16)  # concentration unit (under atmospheric environment) μg/m3
    pc03 = int(data_hex[32:36], 16)  # the number of particles with diameter beyond 0.3 um in 0.1 L of air.
    pc05 = int(data_hex[36:40], 16)  # the number of particles with diameter beyond 0.5 um in 0.1 L of air.
    pc1 = int(data_hex[40:44], 16)  # the number of particles with diameter beyond 1.0 um in 0.1 L of air.
    pc25 = int(data_hex[44:48], 16)  # the number of particles with diameter beyond 2.0 um in 0.1 L of air.
    pc5 = int(data_hex[52:56], 16)  # the number of particles with diameter beyond 5.0 um in 0.1 L of air.
    pc10 = int(data_hex[56:60], 16)  # the number of particles with diameter beyond 10 um in 0.1 L of air.

    return dict(
        uuid=uuid,
        records=[dict(
                    fields=dict(
                        pm1=pm1,
                        pm25=pm25,
                        pm10=pm10,
                        pm1atm=pm1atm,
                        pm25atm=pm25atm,
                        concentr_atm=concentr_atm,
                        pc03=pc03,
                        pc05=pc05,
                        pc1=pc1,
                        pc25=pc25,
                        pc5=pc5,
                        pc10=pc10),
                    ts=int(time.time()))]
    )


def send_data(data, url):
    r = requests.request(method='POST',
                         url=url,
                         headers={
                             'Content-Type': 'application/json',
                             'User-Agent': 'plantower'
                         },
                         data=json.dumps(data))

if __name__ == '__main__':

    for uuid, device in sensors.items():
        device = serial.Serial(device, rate)
        data = read_data(device, uuid, data_size)

        if data is not None:
            send_data(data, api_endpoint)