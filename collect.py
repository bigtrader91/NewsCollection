import os
import logging
import traceback
from dotenv import load_dotenv
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from category import naver_news_category
import telegram
from set_log import set_log
load_dotenv()
token = os.environ.get('token')
chatid = os.environ.get('chatid')
preview = os.environ.get('preview')
bot = telegram.Bot(token = token)
logger=set_log()
class CollectNews:
    def __init__(self, search_keyword, negative_keyword) :
        self.search_keyword=search_keyword
        self.negative_keyword=negative_keyword
        self.check_link=[]
        self.bot= telegram.Bot(token = token)


    def get_text(self, site:str, url:str) -> str :
        """
        site : 네이버, 다음 url을 바탕으로 뉴스기사의 제목과 본문을 return 하는 함수

        """

        ua = UserAgent()
        headers={"user-agent": ua.random }

        response=requests.get(url, headers=headers)
        time.sleep(0.3)
        if site == '네이버':
            try:
                if response.status_code == 200:
                    soup2 = BeautifulSoup(response.content, "html.parser")
                    title=soup2.select_one("#title_area > span").text
                    text=soup2.select_one("#dic_area").text

                    return title, text
                else:
                    logger.debug(f'get 요청실패 상태코드 : {response.status_code}')
                    response=requests.get(url, headers=headers)
                    time.sleep(2)
                    soup2 = BeautifulSoup(response.content, "html.parser")

                    title=soup2.select_one("#title_area > span").text
                    text=soup2.select_one("#dic_area").text

                    return title, text

            except Exception as e:
                title=''
                text=''
                tb = traceback.format_exc()
                logger.debug(f"html 파싱에러 URL : {url}")
                logger.error("get_text 함수 naver에서 에러발생\n URL:{}\n error:{}\nTraceback: {}".format(e, tb))
                return title, text
        if site == '다음':
            try:
                soup3 = BeautifulSoup(response.content, "html.parser")
                title=soup3.select_one("#mArticle > div.head_view > h3").text
                text=soup3.select_one("#mArticle > div.news_view.fs_type1 > div.article_view > section").text

            except Exception as e:
                title=''
                text=''
                tb = traceback.format_exc()
                logger.debug(f"html 파싱에러 URL : {url}")
                logger.error("get_text 함수 daum에서 에러발생\n URL:{}\n error:{}\nTraceback: {}".format(e, tb))


            return title, text




    def collect_news_list(self, base_url: str,date,page: int) -> list:
        """
        특정 뉴스 카테고리의 링크들을 수집하는 함수
        base_url : ex) "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=100&sid2=264"
        date : "yyyymmdd"
        page : 1
        """
        base_url_date_page = base_url + f"&date={date}&page={page}"
        ua = UserAgent()
        headers={"user-agent": ua.random }
        response=requests.get(base_url_date_page, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(response.content, "html.parser")

        news_body=soup.select_one("#main_content > div.list_body.newsflash_body")
        news_href_list=list(set([a["href"] for  a in news_body.find_all("a")]))
        return news_href_list


    def collect_naver(self, cat_num: int):
        """
        cat =>
        0: 정치
        1: 경제
        2: 사회
        3: 생활문화
        4: IT과학세계
        """
        import datetime
        date=datetime.datetime.today().date().strftime("%Y%m%d")
        page=1
        site='네이버'

        df_list = []

        for base_url in tqdm(naver_news_category[cat_num].keys()):
            news_href_list=self.collect_news_list(base_url,date,page)
            category=naver_news_category[cat_num][base_url]
            for url in news_href_list:

                title, text = self.get_text(site,url)
                text=text.replace("\n","").replace("\t","")

                df_temp=pd.DataFrame({"카테고리":category, "title":[title],"text":[text], "링크":[url]})
                df_temp['site']=site
                df_list.append(df_temp)

        df=pd.concat(df_list)
        return df




    def collect_daum(self):
        """
        다음 최신 뉴스 15개씩 수집하여 DataFrame으로 반환하는 함수

        """
        site='다음'
        ua = UserAgent()
        headers={"user-agent": ua.random }
        url='https://news.daum.net/breakingnews?page=1'
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,  "html.parser")
        urls=list(map(lambda x: x.attrs['href'] , soup.select('a.link_txt')))

        df_list=[]
        for url in urls[0:15]:
            title, text =self.get_text(site, url)
            text=text.replace("\n","").replace("\t","")
            df_temp=pd.DataFrame({"title":title,"text":[text], "링크":[url]})
            df_temp['site']=site
            df_list.append(df_temp)
        df=pd.concat(df_list)
        return df

    def thread_naver(self, num):
        """
        네이버 뉴스를 쓰레드로 돌리기위한 함수
        num : 네이버 카테고리 번호(0~4)
        """
        data=self.collect_naver(num)
        for keyword in self.search_keyword :
            data['keyword'] = data['text'].apply(lambda x: keyword if keyword in x else 0  )
        data=data[data["keyword"] != 0]
        for i in self.negative_keyword:
            try:
                data=data[data['text'].apply(lambda x: i not in x )]
            except Exception as e:
                tb = traceback.format_exc()
                logger.error("내용이 없습니다: {}\nTraceback: {}".format(e, tb))

        for i in range(len(data)):
            try:
                카테고리 = data.iloc[i,0]
                타이틀 = data.iloc[i,1]
                텍스트 = data.iloc[i,2]
                링크 = data.iloc[i,3]
                사이트= data.iloc[i,4]
                검색단어=data.iloc[i,5]
                if 링크 not in self.check_link:

                    bot.sendMessage(
                        chat_id = chatid,
                        text=f'포털 : #{사이트}\n카테고리 : #{카테고리}\n검색단어 : #{검색단어}\n타이틀 : {타이틀}\n링크 : {링크}',
                        disable_web_page_preview=preview
                        )


                    self.check_link.append(링크)
            except Exception as e:
                tb = traceback.format_exc()
                logger.error("thread_naver 함수: {}\nTraceback: {}".format(e, tb))

                pass

    def thread_daum(self):
        """
        다음 뉴스 수집을 쓰레드로 돌리기 위한 함수
        """
        data=self.collect_daum()

        for keyword in self.search_keyword:
            data['keyword'] = data['text'].apply(lambda x: keyword if keyword in x else 0  )
        data=data[data["keyword"] != 0]

        for i in self.negative_keyword:
            try:
                data=data[data['text'].apply(lambda x: i not in x )]
            except Exception as e:
                tb = traceback.format_exc()
                logger.error("내용이 없습니다: {}\nTraceback: {}".format(e, tb))

        for i in range(len(data)):
            try:
                타이틀 = data.iloc[i,0]
                텍스트 = data.iloc[i,1]
                링크 = data.iloc[i,2]
                사이트= data.iloc[i,3]
                검색단어=data.iloc[i,4]
                if 링크 not in self.check_link:
                    bot.sendMessage(
                        chat_id = chatid,
                        text=f'포털 : #{사이트}\n검색단어 : #{검색단어}\n타이틀 : {타이틀}\n링크 : {링크}' ,
                        disable_web_page_preview=preview
                        )
                    self.check_link.append(링크)
            except Exception as e:
                tb = traceback.format_exc()
                logger.error("thread_daum 함수: {}\nTraceback: {}".format(e, tb))


                pass
