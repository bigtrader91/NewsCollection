# NewsCollection
네이버와 다음의 실시간 뉴스 수집

## 수집범위
- 네이버 : 뉴스탭의 정치, 경제, 사회, 생활문화, IT/과학, 세계 (https://news.naver.com/)
- 다음 : 전체기사(https://news.daum.net/breakingnews)

## 실행해보기

1.  코드 복사
```
git clone https://github.com/bigtrader91/NewsCollection.git
```

2. 필요한 패키치 설치
```
$ pip install -r requirements.txt
```

4. 텔레그램 봇 생성후 token , chatid 확인

5. .env 파일 생성 및 설정

```
$ vi .env
```

```
#.env
token=생성한 봇의 token
chatid=생성한 채팅방의 chatid
preview=True #링크 미리보기 설정(True/False)
```
6. 실행
```
$ python3 main.py
```
