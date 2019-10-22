

import json
import time
import pymysql
import tweepy
from googletrans import Translator
import emoji
import re
from textblob import TextBlob
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from openpyxl import load_workbook
from eunjeon import Mecab
from konlpy.tag import Kkma
import warnings
from plotnine import *
import sys
import os

CONSUMER_KEY='sNvbLosesCCNt2NekT5CRSGXB'
CONSUMER_SECRET = 'afeh7wzvr9MJy6x3NaaFCbPw5rfHSkkSqaDPez6jx5TL2v9ZKi'
ACCESS_TOKEN_KEY = '1160086470100541442-FS2RKchHxI7rd8dEIOUQmzCh9g4uT9'
ACCESS_TOKEN_SECRET = 'AWIQuB48Iad82cyiln8dPaiKfzrOiCb2vYemiAc9mequB'

auth =tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

kkma = Kkma()
warnings.filterwarnings('ignore')

def sentimentt(text):      # 번역 후 감성분석
    translator = Translator()
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])   #이모티콘 제거
    clean_text = re.sub('[-=+,#/?!\:^$.@*\"※~&%ﾟД�ㆍ』\\‘|\(\)\[\]\<\>`\'…》123456789]', '', clean_text)   #특수문자 제거
    try:
        clean_text = translator.translate(clean_text, src='ko', dest='en').text    #영어번역
    except json.decoder.JSONDecodeError:    # 특수문자등 예기치 못한 문장은 걍 좋은 걸로..
        clean_text = "best"
    blob = TextBlob(clean_text)            #감성분석
    return blob.sentiment[0], blob.sentiment[1]

def getNouns(text):            #형태소 분석
    print("형태소분석중")
    p = re.compile("\W+")
    p.sub(" ", text)
    #Emojifuck = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)  #이모티콘 제거
    #Emojifuck.sub(" ", text)
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])  # 이모티콘 제거
    clean_text = re.sub('[-=+,#/?!\:^$.@*\"※~&%ﾟД�ㆍ』\\‘|\(\)\[\]\<\>`\'…》123456789]', '', clean_text)  # 특수문자 제거
    pattern = re.compile("[ㄱ-ㅎㅏ-ㅣ]+")    # ㄱ, ㄴ, ㄷ 이렇게 나오게하는거 방지
    pattern.sub(" ", clean_text)

    nonWords = ["좋은데", "베리", "그리고", "마포구", "나랑", "최", "파라", "커피", "홍대", "망원동", "서울", "연", "연남", "연남동", "남동", "맛집", "카페",
                "숙녀", "그녀", "카톡", "톡친", "뿌셔", "여성", "술집", "가게", "손님", "집", "어제", "오늘", "문의", "친구", "망원", "동네", "문", "동",
                "대관", "얘기", "데이트", "이벤트", "홀더", "맛", "존맛", "소금", "굳", "비투비", "빅스", "러", "나눔", "주세요", "카스", "정일"]
    print(clean_text)
    if len(clean_text) > 0:
        pos = kkma.pos(clean_text)
        for word, type in pos:
           if word not in nonWords:
                if type == "NNP":
                   nounss.append(word)
           time.sleep(0.3)
    return

"""""
def association(dataset):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)  #보기좋게 데이터프레임으로 변경
    frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)   #지지도 0.5로 두고 자주 등장하는 아이템셋 추출
    print(frequent_itemsets)
    print(association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3))  #신뢰도가 0.3이상인 항목들만 보기

    return

"""""

def firstStep() :

    api = tweepy.API(auth, wait_on_rate_limit=True)
    location = "%s,%s,%s" % ("37.564", "127.001", "18km")  # 검색기준(서울 중심) 좌표, 반지름

    keyword = "맛집"                                      # 검색어(키워드)



    # twitter 검색 cursor 선언

    cursor = tweepy.Cursor(api.search,

                            q=keyword,

                            since='2018-10-22',   # 선택된 날짜 이후에 작성된 트윗들로 가져옴

                            count=100,  # 페이지당 반환할 트위터 수 최대 100

                           geocode=location,

                           include_entities=True

                           )

    temp = []

    for i, tweet in enumerate(cursor.items()):
        if 'RT @' not in tweet.text:
            if '다음카페' not in tweet.text:
                if '네이버 카페' not in tweet.text:
                    if '블로그' not in tweet.text:
                        if '팬미팅' not in tweet.text:
                            if '출처' not in tweet.text:
                                if '카페 창업' not in tweet.text:
                                    if '데뷔' not in tweet.text:
                                        if '생일' not in tweet.text:
                                            if '얼굴맛집' not in tweet.text:
                                                if '예능맛집' not in tweet.text:
                                                    if '급상승 검색어' not in tweet.text:
                                                         how, objectivity = sentimentt(tweet.text)
                                                         if how >= 0 and objectivity >= 0.5:
                                                            #print(getNouns(tweet.text))
                                                            getNouns(tweet.text)



    return

nounss = []
#beforeAssociationRules = []
firstStep()
#association(beforeAssociationRules)
print("분석끝")

conn = pymysql.connect(host='localhost', port=3305, user='root', password='ahdwo0900!', db='hong_db',charset='utf8mb4')  # 데이터베이스 커넥션 설정
curs = conn.cursor()  # 데이터 전달하려고 커서 생성

sql = """
           CREATE TABLE morong5 (
                 id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                 hot_place VARCHAR(100),
                 address VARCHAR(1000),
                 PRIMARY KEY(id)
            );
            """

sql2 = """
         DROP TABLE morong5;
    """


try:
    curs.execute(sql)  # 디비와 연동
except pymysql.err.InternalError:
    curs.execute(sql2)
    curs.execute(sql)


cnt = 0

shop = pd.read_csv('C:\\Users\\admin\\Desktop\\hongjae\\Shops.csv', encoding='cp949')
Shops = shop[['상호명', '도로명주소']]
nounss.sort()
data = []


print("상호명 파악중")
for name in nounss:
 cnt = 0
 for sname in Shops.상호명:
    if name == sname:
        try:
            data.append((Shops.상호명[cnt], Shops.도로명주소[cnt]))
        except KeyError:
            pass
    cnt = cnt+1
 time.sleep(1)

print("파악완료 후 디비 저장중")

query = """insert into morong5(hot_place, address) values (%s, %s)"""
curs.executemany(query, tuple(data))
conn.commit()
print(nounss)
print("################단어 빈도수#########################")
print(pd.Series(nounss).value_counts().head(30))