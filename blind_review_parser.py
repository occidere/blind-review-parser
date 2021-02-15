# -*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime
from typing import *

import dateutil.parser
import requests
from bs4 import BeautifulSoup
from requests import Response


class Review:

    def __init__(self, company: str, title: str, url: str, score: float, auth: str):
        self.url_hash = str(hashlib.sha1(url.encode('utf-8-sig')).hexdigest())
        self.title = ''.join(title[1:-1])  # 제목의 " 제거
        self.company, self.url, self.score = company, url, score
        self.__parse_auth(auth)

    def __parse_auth(self, auth: str) -> None:
        arr = auth.strip().split(' ')
        self.masked_id, self.job_group, self.rgst_ymd = arr[1], ' '.join(
            arr[3:-2]), f"{datetime.strptime(arr[-1], '%Y.%m.%d').isoformat()}+09:00"

    def to_json_str(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


class BlindParser:

    def __init__(self, company: str, es_endpoint: str) -> None:
        self.company, self.es_endpoint = company, es_endpoint

    def run(self, p_num_start: int = 1, p_num_end: int = 100) -> None:
        print(f'{self.company} 리뷰 수집 시작')
        self.__parse_reviews(self.company, p_num_start, p_num_end)
        print(f'{self.company} 리뷰 수집 완료')

    def __parse_reviews(self, company: str, p_num_start: int, p_num_end: int) -> None:
        for p_num in range(p_num_start, p_num_end + 1):
            try:
                reviews = self.__parse_page(f'https://www.teamblind.com/kr/company/{company}/reviews?page={p_num}')
                if reviews:
                    self.__bulk_upsert_to_es(reviews)
                    print(f'{p_num} 페이지 파싱 & ES 색인 완료 (리뷰 개수: {len(reviews)})')
                else:
                    break
            except Exception as e:
                print(f'리뷰 처리 실패: {e}')

    @staticmethod
    def __create_bs(url: str, encoding: str = 'utf-8') -> BeautifulSoup:
        resp: Response = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        resp.encoding = encoding
        return BeautifulSoup(markup=resp.text, features='html.parser')

    def __parse_page(self, review_url: str) -> List[Review]:
        reviews: List[Review] = []
        for review_item in self.__create_bs(review_url).find_all(name='div', attrs={'class', 'review_item'}):
            try:
                score_element = review_item.find(name='strong', attrs={'class', 'num'})
                score_element.find(name='i').decompose()
                rvtit = review_item.find(name='h3', attrs={'class': 'rvtit'}).find(name='a')
                auth_element = review_item.find(name='div', attrs={'class': 'auth'})
                auth_element.find(name='strong').decompose()

                reviews.append(Review(
                    company=self.company,
                    title=rvtit.text,
                    url=rvtit['href'],
                    score=float(score_element.text),
                    auth=auth_element.text.strip())
                )
            except Exception as e:
                print(f'리뷰 파싱 실패: {e}')

        return reviews

    def __bulk_upsert_to_es(self, reviews: List[Review]) -> None:
        bulk_req: List[str] = []
        for review in reviews:
            bulk_req += [
                json.dumps({
                    "index": {
                        "_index": f'blind-review-{dateutil.parser.parse(review.rgst_ymd).strftime("%y%m%d")}',
                        "_id": review.url_hash
                    }
                }, ensure_ascii=False), '\n',
                review.to_json_str(), '\n'
            ]
        requests.post(
            url=f'{self.es_endpoint}/_bulk',
            headers={'Content-Type': 'application/x-ndjson'},
            data=(''.join(bulk_req).encode('utf-8-sig'))
        )


if __name__ == '__main__':
    companies = [
        'NAVER', '카카오', '라인플러스', 'COUPANG', '우아한형제들',  # 네카라쿠배
        'NEXON', '넷마블', 'NCSOFT'  # 3N
    ]
    for c in companies:
        blind_parser = BlindParser(company=c, es_endpoint='http://localhost:9200')
        blind_parser.run()
