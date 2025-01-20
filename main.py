from fastapi import FastAPI    # python web devtool
from pydantic import BaseModel    # 유효성 검사
from starlette.middleware.base import BaseHTTPMiddleware
# 요청(Request)과 응답(Response) 사이에 특정 작업 수행
# 미들웨어는 모든 요청에 대해 실행되며, 요청 처리 전, 응답 반환 전에 특정 작업을 수행할 수 있음
# 예을 들어 로깅, 인증, cors(Cross Origin Resource Sharing) 처리, 압축 등
import logging    # 로그 출력

app = FastAPI(    # 생성자를 통하여 postman을 대체하는 문서화 툴
    title = "MBC AI Project Test",
    description = "Python과 Spring-Boot를 연동한 AI Application",
    version = "1.0.0",
    docs_url = None,    # /docs / 보안상 None 처리
    # redoc_url = None    # /redoc
)    # fastapi 객체 생성 후 app 변수에 넣음

class LoggingMiddleware(BaseHTTPMiddleware):    # 로그를 콘솔에 출력
    logging.basicConfig(level = logging.INFO)    # 로그 출력 추가
    async def dispatch(self, request, call_next):
        logging.info(f"Reg : {request.method} / {request.url}")
        response = await call_next(request)
        logging.info(f"Status Code : {response.status_code}")
        return response
app.add_middleware(LoggingMiddleware)    # 모든 요청에 대해 로그를 남기는 미들웨어 클래스 사용

class Item(BaseModel):   # item 객체 생성(BaseModel : 객체 연결 -> 상속)
    name : str    # 상품명 : 문자열
    description : str = None    # 상품설명 : 문자열(null)
    price : float    # 가격 : 실수형
    tax : float = None    # 세금 : 실수형(null)

    # 컨트롤러 검증은 postman으로 활용, 내장된 back 검증툴 사용 가능

@app.get("/")    # http://ip주소:port/ (root context)
async def read_root():
    return {"Hello" : "World"}

@app.post("/items/")    # post 매서드 응답
async def create_item(item : Item):    # BaseModel은 데이터 모델링을 쉽게 도와주고, 유효성 검사를 수행함
    # 잘못된 데이터가 들어오면 422 오류코드 반환
    return item

@app.get("/items/{item_id}")    # http://ip주소:port/items/1
async def read_item(item_id : int, q : str = None):
    return {"item_id" : item_id, "q" : q}
    # item_id : 상품의 번호 -> 경로 매개변수
    # q : query 매개변수 (Default : None)

