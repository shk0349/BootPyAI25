# 선행 준비 : ip camera 설치 및 준비
# ip camera 제조사 홈페이지를 참조하여 관련 네트워크 설정 마무리
# 제조사의 vms 프로그램 설치 / ip, pw, rtsp protocol 활성화
    # rtsp : //admin:mbc312AI!!@192.168.0.4:554/mbcai_2
# python과 Front를 연동하는 mqtt api 활용
    # mqtt : 실시간 출력 protocol / 참고 URL : https://underflow101.tistory.com/22
    # mqtt 브로커용 프로그램으로 모스키토 api 활용
    # 참고 URL : https://mosquitto.org/download/ ver은 2.0.18 사용
    # 모스키토 환경결정 변경 : C:\Program Files\mosquitto\mosquitto.conf
    # 메모장을 관리자 권한으로 열어서 listener 부분에 아래 내용 기입
        # # MQTT 기본 리스너 설정
        # listener 1883
        # protocol mqtt
        #
        # # WebSocket Listener 설정
        # listener 9001
        # protocol websockets
        #
        # # 익명 접속 허용
        # allow_anonymous true

    # 방화벽 추가 / 실행 -> wf.msc -> 인바운드 규칙 -> 새 규칙 -> 포트 -> 1883, 9001
    # 모스키토 환경설정 적용 실행 : cmd 실행 -> cd\ -> cd "Program Files" -> cd mosquitto -> mosquitto -c mosquitto.conf -v
        # 실행 불가 시 services.msc(서비스)에서 서비스 재실행

import base64
import io
from PIL import Image
import numpy as np
import json
from ultralytics import YOLO
import paho.mqtt.client as mqtt    # 브로커 추가 / mosquitto 지속실행 필요
import cv2
import time

model = YOLO("yolov8n.pt")
client = mqtt.Client()    # mosquitto -c mosquitto.conf
topic = '/camera/objects'    # 경로
client.connect('localhost', 1883, 60)

# 연결용 함수
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# 객체 감지용 색상 함수
def get_colors(num_colors):
    np.random.seed(0)
    colors = [tuple(np.random.randint(0, 255, 3).tolist()) for _ in range(num_colors)]
    return colors

class_names = model.names    # 모델에서 받은 클래스 이름
num_classes = len(class_names)    # 클래스 번호
colors = get_colors(num_classes)    # 시각박스 컬러색

client.on_connect = on_connect    # 클라이언트 연결 정보
cap = cv2.VideoCapture('rtsp://admin:mbc312AI!!@192.168.0.4:554/mbcai_2')    # rtsp 정보(vms 참고)
    # 참고 URL : https://deep-learning-study.tistory.com/107
    # 세팅 예시
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # bRec = False
        # prevTime = 0

# ============================================== 전처리단계 종료 ==============================================

# 모델을 이용한 객체탐지 함수
def detect_objects(image: np.array):
    results = model(image, verbose = False)
    class_names = model.names

    for result in results:
        boxes = result.boxes.xyxy
        confidences = result.boxes.conf
        class_ids = result.boxes.cls
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = class_names[int(class_id)]
            cv2.rectangle(image, (x1, y1), (x2, y2), colors[int(class_id)], 2)
            cv2.putText(image, f'{label} {confidence:.2f}', (x1, y1),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, colors[int(class_id)], 2)
    return image

# 객체 탐지 반복용 루프
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    result_image = detect_objects(frame)

    _, buffer = cv2.imencode('.jpg', result_image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    payload = json.dumps({'image':jpg_as_text})
    client.publish(topic, payload)
    # cv2.imshow('Frame', result_image)

    # 영상 출력 중 q가 입력 시 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()    # VideoCapture
cv2.destroyAllWindows()    # 창 닫기
client.disconnect()    # 연결 해제