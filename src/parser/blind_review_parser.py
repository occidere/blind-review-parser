# -*- coding: utf-8 -*-
from typing import *

import requests
from bs4 import BeautifulSoup
from requests import Response

from src.vo.review import Review
from src.service.elastic_service import ElasticService


class BlindParser:

    def __init__(self, company: str, es_endpoint: str, es_base64_auth: str = '') -> None:
        self.company, self.es_endpoint = company, es_endpoint
        self.es_service = ElasticService(es_endpoint, es_base64_auth)

    def run(self, p_num_start: int = 1, p_num_end: int = 300) -> None:
        print(f'[{self.company} 리뷰 수집 시작]')
        self.__parse_reviews(self.company, p_num_start, p_num_end)

    def __parse_reviews(self, company: str, p_num_start: int, p_num_end: int) -> None:
        """
        지정한 페이지의 리뷰들을 수집한 뒤 신규 리뷰가 있는 경우 ES 색인, 없으면 종료
        :param company: 리뷰를 수집할 회사명
        :param p_num_start: 리뷰 수집할 페이지 시작번호 (이상)
        :param p_num_end: 리뷰 수집할 페이지 끝 번호 (이하)
        """
        p_num, finished = p_num_start, False
        while p_num <= p_num_end and not finished:
            try:
                reviews = self.__parse_page(f'https://www.teamblind.com/kr/company/{company}/reviews?page={p_num}')
                if reviews:
                    # 수집한 리뷰가 1개라도 이미 ES 에 존재하면 종료 (최신 리뷰만 수집)
                    finished = self.es_service.exist_any(reviews)
                    bulk_resp = self.es_service.bulk_upsert(reviews)
                    if 200 <= bulk_resp.status_code < 300:
                        print(f'> {p_num} 페이지 ES 색인 완료 (리뷰 개수: {len(reviews)})')
                    else:
                        print(f'> {p_num} 페이지 ES 색인 실패 (리뷰 개수: {len(reviews)}) => {bulk_resp.text}')
                else:  # 페이지 내 리뷰가 없는경우 종료
                    finished = True
                p_num += 1
            except Exception as e:
                print(f'리뷰 처리 실패: {e}')

    def __parse_page(self, review_url: str) -> List[Review]:
        reviews: List[Review] = []
        for review_item in self.__create_bs(review_url).find_all(name='div', attrs={'class', 'review_item'}):
            try:
                score_element = review_item.find(name='strong', attrs={'class', 'num'})
                score_element.find(name='i').decompose()
                rvtit = review_item.find(name='h3', attrs={'class': 'rvtit'}).find(name='a')
                auth_element = review_item.find(name='div', attrs={'class': 'auth'})
                auth_element.find(name='span').decompose()

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

    @staticmethod
    def __create_bs(url: str, encoding: str = 'utf-8') -> BeautifulSoup:
        resp: Response = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        resp.encoding = encoding
        return BeautifulSoup(markup=resp.text, features='html.parser')
