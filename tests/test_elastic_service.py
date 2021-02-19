import unittest

from blindreviewparser.parser.blind_review_parser import *


class TestElasticService(unittest.TestCase):

    def setUp(self) -> None:
        self.es_endpoint = 'http://localhost:9200'
        self.elastic_service = ElasticService(self.es_endpoint)
        self.sample = Review(
            company='occidere',
            title='"테스트 리뷰"',
            url='/kr/company/occidere/review/af9-0df3j',
            score=5.0,
            auth='현직원 · i*********", · IT 엔지니어 - 2021.02.17'
        )

    def tearDown(self) -> None:
        self.__delete_sample()

    def test_exist_any(self):
        # BUILD
        self.__index_sample()

        # OPERATE
        exist = self.elastic_service.exist_any([self.sample])

        # CHECK
        self.assertTrue(exist)

    def test_bulk_upsert(self):
        # BUILD
        self.__delete_sample()

        # OPERATE
        self.elastic_service.bulk_upsert([self.sample])

        # CHECK
        resp = requests.get(f'{self.es_endpoint}/blind-review-210217/_doc/{self.sample.url_hash}')
        self.assertEqual(resp.status_code, 200)

    def __index_sample(self) -> None:
        requests.post(
            url=f'{self.es_endpoint}/blind-review-210217/_doc/{self.sample.url_hash}',
            headers={'Content-Type': 'application/json'},
            data=self.sample.to_json_str().encode('utf-8')
        )

    def __delete_sample(self) -> None:
        requests.delete(f'{self.es_endpoint}/blind-review-210217/_doc/{self.sample.url_hash}')
