 1 # Data Format
 2 # CO2 Data0
 3 # THL Temperature Data0, Humidity Data1, Illumination Data2, Battery Data3
 4
 5 import sys
 6 import tos  # TinyOS Python 통신 라이브러리
 7 import datetime  # 현재 시간 기록용
 8 import threading  # (사용은 안 함) 멀티스레딩 지원
 9
10 AM_OSCILLOSCOPE = 0x93  # 메시지 타입 정의 (사용되지 않음)
11
12 # TinyOS 패킷 구조 정의
13 class OscilloscopeMsg(tos.Packet):
14     def __init__(self, packet = None):
15         tos.Packet.__init__(self,
16             [('srcID', 'int', 2),    # 송신 노드 ID
17              ('seqNo', 'int', 4),    # 시퀀스 번호
18              ('type', 'int', 2),     # 데이터 타입 (예: 2 = THL)
19              ('Data0', 'int', 2),    # 온도
20              ('Data1', 'int', 2),    # 습도
21              ('Data2', 'int', 1),    # 조도 (하위 바이트)
22              ('Data3', 'int', 1),    # 조도 (상위 바이트)
23              ('Data4', 'int', 2),    # 배터리 전압
24             ], packet)
25 
26 # 사용법 안내 메시지 (옵션 -h 입력 시)
27 if '-h' in sys.argv:
28     print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
29     sys.exit()
30
31 am = tos.AM()  # Active Message 통신 시작
32
33 while True:
34     p = am.read()  # 패킷 수신
35     msg = OscilloscopeMsg(p.data)  # 패킷 데이터 파싱
36     print p  # 수신된 패킷 출력
37
38 ###### THL 센서 처리 로직 ##########
39     if msg.type == 2:  # 메시지 타입이 THL인 경우만 처리
40         battery = msg.Data4  # 배터리 전압
41
42         Illumi = int(msg.Data2) + int(msg.Data3 * 256)  # 조도 데이터 (2바이트)
43
44         # 습도 계산 공식 (센서 보정 포함)
45         humi = -2.0468 + (0.0367 * msg.Data1) + (-1.5955 * 0.000001) * msg.Data1 * msg.Data1
46
47         # 온도 계산 공식 (센서 보정 포함)
48         temp = -39.6 + (msg.Data0 * 0.01)
49
50         try:
51             with conn.cursor() as curs:  # DB 커서 열기
52                 Now = datetime.datetime.now()  # 현재 시간 기록
53
54                 # DB 삽입 SQL 정의
55                 sql = """insert into JB_Sensor_THL(NODE_ID,SEQ,TEMPERATURE,HUMIDITY,ILLUMINATION,REGDATE)
56                          values(%s, %s, %s, %s, %s, %s)"""
57
58                 # DB에 센서 데이터 저장
59                 curs.execute(sql, (msg.srcID, msg.seqNo, temp, humi, Illumi, Now))
60                 conn.commit()  # 변경사항 커밋
61         except all, e:  # 예외 처리 (오류 발생 시)
62             print e.args  # 오류 메시지 출력
63             conn.close()  # DB 연결 닫기
64
65         # 수신 결과 출력
66         print "id:" , msg.srcID, " Count : ", msg.seqNo, \
