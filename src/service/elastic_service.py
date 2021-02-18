# -*- coding: utf-8 -*-
import json
from typing import *

import dateutil.parser as d_parser
import requests
from requests import Response

from src.vo.review import Review


class ElasticService:

    def __init__(self, es_endpoint: str = 'http://localhost:9200', base64_auth: str = ''):
        self.es_endpoint, self.base64_auth, self.index = es_endpoint, base64_auth, 'blind-review'

    def bulk_upsert(self, reviews: List[Review]) -> Response:
        bulk_req: List[str] = []
        for review in reviews:
            bulk_req += [
                json.dumps({
                    "index": {
                        "_index": f'blind-review-{d_parser.parse(review.rgst_ymd).strftime("%y%m%d")}',
                        "_id": review.url_hash
                    }
                }, ensure_ascii=False), '\n',
                review.to_json_str(), '\n'
            ]
        # elastic:GKtzvhlwCFPkrsl8ZC8qIafv
        return requests.post(
            url=f'{self.es_endpoint}/_bulk',
            headers={
                'Content-Type': 'application/x-ndjson',
                'Authorization': 'Basic ' + self.base64_auth if self.base64_auth else ''
            },
            data=(''.join(bulk_req).encode('utf-8'))
        )

    def exist_any(self, reviews: List[Review]) -> bool:
        try:
            docs: List[Dict[str, Any]] = []
            for r in reviews:
                docs.append({
                    '_index': f'{self.index}-{d_parser.parse(r.rgst_ymd).strftime("%y%m%d")}',
                    "_id": r.url_hash
                })
            resp: Response = requests.get(
                url=f'{self.es_endpoint}/_mget',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + self.base64_auth if self.base64_auth else ''
                },
                data=(json.dumps({'docs': docs}))
            )
            for doc in resp.json().get('docs', []):
                if doc.get('found', False):
                    return True

        except Exception as e:
            print(f'mget 실패 => {e}')
            return False
