Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import serial
from influxdb_client import InfluxDBClient
import time

serial_port = 'COM17'
baud_rate = 9600
timeout = 2

# InfluxDB v2 설정
influxdb_url = "http://localhost:8086"
... influxdb_token ="D_H5-onznz2vOB-3AQradLUg8B5DTd9uHJS-OOwF3Mqrbt1RudfJK7xmE3VEB048l6Y7ni-bq8_6dFADbGi_6A=="
... influxdb_org = "test"
... influxdb_bucket = "dust"
... 
... # InfluxDB 클라이언트 초기화
... client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
... write_api = client.write_api()
... 
... # 시리얼 포트 열기
... try:
...     ser=serial.Serial(serial_port, baud_rate, timeout=timeout)
...     print(f"Connected to {serial_port} at {baud_rate} baud")
... except:
...     print("Failed to connect to serial port")
...     exit()
... try:
...     while True:
...         if ser.in_waiting>0:
...             # 아두이노로부터 시리얼 데이터를 읽음
...             line=ser.readline().decode('utf-8').strip()
... 
...             # 데이터가 유효한 경우 InfluxDB에 기록
...             if"=" in line:
...                 key, value = line.split("=")
...                 try:
...                     value=float(value)
...                     data=f"sensor_data,device=arduino {key}={value}"
...                     write_api.write(bucket=influxdb_bucket, record=data)
...                     print(f"Data written to influxDB: {key}={value}")
...                 except ValueError:
...                     print("Invalid data format")
... 
...         time.sleep(1)
... 
... except KeyboardInterrupt:
...     print("프로그램이 종료되엇습니다.")
... finally:
