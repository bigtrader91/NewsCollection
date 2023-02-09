# NewsCollection
네이버와 다음의 실시간 뉴스 수집

## 필요성
- 네이버나 다음의 경우 검색API를 제공하나 특정 키워드로 검색했을 때의 뉴스를 확인할 수 있으므로 키워드 없이 전체뉴스를 수집하기 위해서는 
별도의 수집의 필요성을 느낌. 
- API에서는 제목, 링크, 본문 상단 몇줄 정도의 text만 제공하므로 본문 전체내용이 필요할 수 있음

## 활용
- 주식 관련 프로젝트를 진행할 때 텍스트마이닝을 통해 피처로 활용
- 기타 등등

![image](https://user-images.githubusercontent.com/88607278/217497060-34bbcd99-a7d6-40b1-8a72-266ef69c4d1a.png)


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
