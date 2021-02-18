# -*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime


class Review:

    def __init__(self, company: str, title: str, url: str, score: float, auth: str):
        self.url_hash = str(hashlib.sha1(url.encode('utf-8-sig')).hexdigest())
        self.title = ''.join(title[1:-1])  # 제목의 " 제거
        self.company, self.url, self.score = company, url, score
        self.__parse_auth(auth)

    def __parse_auth(self, auth: str) -> None:
        arr = auth.strip().split(' ')  # ['현직원', '·', 'r*****', '·', 'IT', '엔지니어', '-', '2021.02.12']
        self.emp_status, self.masked_id, self.job_group = arr[0], arr[2], ' '.join(arr[4:-2])
        self.rgst_ymd = f"{datetime.strptime(arr[-1], '%Y.%m.%d').isoformat()}+09:00"

    def to_json_str(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)
