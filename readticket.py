from flask import Flask,jsonify,request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import easyocr
from difflib import get_close_matches
import datetime
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
FRONT_URL = config['FRONT_URL']

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app, resources={r'*': {'origins': FRONT_URL}})

@app.route("/ocr",methods=['POST'])
def ticketreader():
    n=4
    cutoff=0.7
    f=request.files['file']
    f.save(secure_filename(f.filename))
    path=secure_filename(f.filename)
    reader = easyocr.Reader(['ko','en'], gpu = False)
    result = reader.readtext(str(path),detail=0)
    os.remove(str(path))
    theather=["세종문화회관","예술의전당 오페라극장","예술의전당 CJ 토월극장",
"샤롯데씨어터",
"LG아트센터",
"블루스퀘어 신한카드홀",
"블루스퀘어 인터파크홀",
"블루스퀘어 아이마켓홀 (구 삼성카드홀)",
"충무아트센터",
"대성 디큐브아트센터",
"국립극장 해오름",
"한전아트센터",
"우리금융아트홀",
"경기아트센터",
"성남아트센터 오페라하우스",
"용인포은아트홀",
"창원 성산아트홀",
"부산 드림씨어터",
"부산문화회관",
"부산 소향씨어터 신한카드홀",
"대구오페라하우스",
"계명대학교 계명아트센터",
"대전예술의전당 아트홀",
"광주문화예술회관",
"광림아트센터 BBCH홀",
"제주문화예관",
"동서울대학교",
"광주빛고을시민문화회관",
"예스24 스테이지",
"두산아트센터 연강홀",
"홍익대 대학로 아트센터",
"세종문화회관 M씨어터",
"아트원 씨어터", "TOM", "유니플렉스",
"악스 코리아","경희대 평화의 전당","올림픽핸드볼경기장",
"코엑스 컨벤션홀 Hall D","잠실실내체육관","올림픽체조경기장",
"고척스카이돔","잠실올림픽보조경기장","상암월드컵경기장","잠실올림픽주경기장"]
    date=""
    location=""
    seat=""
    for i in result:
        if "년" in i or "월" in i or "일" in i and "모바일" not in i and "예매" not in i:
            date+=i
        t=get_close_matches(i, theather, n, cutoff)
        if t:
            location+=" ".join(t)
        if "층" in i or "열" in i or "번" in i and "번호" not in i:
            seat+=i
    date=date.replace('일 시:','')
    date=date.replace(' ','')
    dateformat=datetime.datetime.strptime(date,'%Y년%m월%d일').strftime('%Y-%m-%d')
    return jsonify(ticketDate=dateformat,ticketLocation=location,ticetSeat=seat)

if __name__=='__main__':
    app.run(debug=False,host="127.0.0.1",port=5000)

