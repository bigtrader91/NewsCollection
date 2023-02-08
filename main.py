
import threading
from collect import CollectNews
import traceback
from set_log import set_log


def main():
    logger=set_log()

    검색어=['속보', '단독', '인공지능','파이썬',"튀르키예","가수","동거녀","박용진"]
    제외단어=[ '골프','비트코인','대통령']

    collectnews=CollectNews(  검색어, 제외단어)
    while True:
        try:
            logger.info(f"뉴스 검색을 시작합니다 검색어는 : {검색어} 입니다.")
            t0 = threading.Thread(target=collectnews.thread_naver, args=(0,))
            t1 = threading.Thread(target=collectnews.thread_naver, args=(1,))
            t2 = threading.Thread(target=collectnews.thread_naver, args=(2,))
            t3 = threading.Thread(target=collectnews.thread_naver, args=(3,))
            t4 = threading.Thread(target=collectnews.thread_naver, args=(4,))
            t5= threading.Thread(target=collectnews.thread_daum)
            t0.start()
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t0.join()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
        except Exception as e:
            tb = traceback.format_exc()
            logger.error("main 함수에서 에러 발생: {}\nTraceback: {}".format(e, tb))


if __name__ == '__main__':
    main()
