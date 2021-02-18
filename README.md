# blind-review-parser
블라인드의 기업 리뷰를 Elastic Stack 으로 색인 및 시각화 하는 프로젝트


<br>

## 블라인드 기업 리뷰?
- Page: https://www.teamblind.com/kr/company
- Review sample (구글코리아)

    ![구글코리아 공개 리뷰정보](https://user-images.githubusercontent.com/20942871/107968678-01544200-6ff2-11eb-88b9-2c2c65afb387.png)


>### ⚠ Disclaimer
>리뷰 전체 상세내용을 확인하기 위해선 로그인 & 본인 기업 리뷰가 필요하기 때문에, **리뷰 제목과 평점, 직군 등의 오픈된 정보만 수집**하였습니다.
>
>**모든 리뷰의 저작권은 Teamblind. Inc 에 있습니다.**


<br>

## Kibana Demo

>Demo 링크에서 직접 상호작용이 가능합니다. (heroku free tier 인 관계로 다소 느릴 수 있습니다)
>
>아래 샘플차트는 2020-07-01 ~ 2021-02-18 까지 작성된 리뷰 데이터로 생성되었습니다.

<br>

### 단일 기업 평가 대시보드 (Demo: https://me2.do/GozrS73w)

<img src="https://user-images.githubusercontent.com/20942871/108374373-41126800-7244-11eb-84df-0b9068e5e63e.png" width="60%"/>

<br>

### 다중 기업 비교 대시보드 (Demo: https://me2.do/GeWwkXBd)

<img src="https://user-images.githubusercontent.com/20942871/108374652-8898f400-7244-11eb-9665-1c7c613fb292.png" width="60%"/>


<br>

## How to use?

#### 1. Elasticsearch & Kibana 실행
- 참고: https://www.elastic.co/kr/start

#### 2. Blind 기업 리뷰 수집 & ES 색인

1. [`src/__main__.py`](https://github.com/occidere/blind-review-parser/blob/main/src/__main__.py) 파일 내 `companies` 리스트에 블라인드에 등록된 기준의 회사명을 입력
2. `es_endpoint` 에 리뷰를 저장할 Elasticsearch 주소 입력 후 실행

```python
if __name__ == '__main__':
    companies = [
        'NAVER', '카카오', '라인플러스', 'COUPANG', '우아한형제들',  # 네카라쿠배
        'NEXON', '넷마블', 'NCSOFT'  # 3N
    ]
    for company in companies:
        blind_parser = BlindParser(
            company=company,
            es_endpoint='http://localhost:9200',  # ES 주소 입력
            es_base64_auth='zWxdpYzp2z6d-mdtyc2w4Y=='  # id:pw 가 있으면 base64 로 인코딩하여 입력 (없을 시 삭제)
        )
        blind_parser.run(
            p_num_start=1,  # 수집할 리뷰 페이지의 시작번호 (이상)
            p_num_end=300  # 수집할 리뷰 페이지의 마지막 번호 (이하)
        )
```

#### 3. [`blind_review_saved_object.ndjson`](https://github.com/occidere/blind-review-parser/blob/main/blind_review_saved_object.ndjson) 파일 import
- Kibana 에서 Stack Management > Saved objects 메뉴
<img src="https://user-images.githubusercontent.com/20942871/108064772-7bdb9b00-70a0-11eb-839b-50fe0b018b49.png" width="60%" />

#### 4. Kibana 의 Analytics 메뉴에서 Visualize / Dashboard 확인
