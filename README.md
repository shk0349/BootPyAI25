# BootPyAI25
Spring-Boot &amp; Python AI Module

# 개발 환경 구축
1. Python Interpreter : http://www.python.org/ -> 3.12 ver Install (3.8이상필수)
2. IDE Install : https://www.jetbrains.com/ko-kr/pycharm/download/?section=windows -> Community Ver Install
3. FastAPI Install : pip install fastapi uvicorn
- ASGI(Asynchronus Server Gateway Interface)는 Python에서 비동기 Web Server와 Web Appication 간의 Interface / 표준 ASGI는 기존 WSGI(Web Server Gateway Interface)의 비동기 버전으로, Python에서 비동기 처리를 지원하는 Web Application을 구축하기 위함 
- 참고 URL / https://velog.io/@hwaya2828/WSGI-ASGI
4. ASGI 특징
- 비동기 지원 : ASGI는 비동기 코드 실행을 지원하며 높은 성능과 동시성을 제공, WebSocket이나 Server Push와 같은 비동기 통신이 필요한 Application에 유용
- 범용성 : HTTP뿐만 아니라, WebSocket, gRPC와 같은 다른 Protocal로 지원
- 유연성 : ASGI Application은 다양한 Server 및 Framework와 호환되며, Module식으로 구성
5. FastAPI와 ASGI
- FastAPI는 ASGI 표준을 따르는 Web Framdwork
- FastAPI Application은 비동기 처리를 기본으로 하며, Uvicorn과 같은 ASGI Server를 사용하여 높은 성능을 제공
- FastAPI Server 실행 -> main.py 실행 -> Terminal에서 D:\phthonWorkSpace> uvicorn main:app --reload --port 8001 (위치확인)

![image](https://github.com/user-attachments/assets/cbafc721-f6f9-4896-87c6-f30920d9e80b)

![image](https://github.com/user-attachments/assets/199264fc-7bb4-4d06-8345-ac4c66f368a3)
