# blind-review-parser
블라인드의 기업 리뷰를 파싱한 뒤 ES 에 색인하는 스크립트

<br>

## 블라인드 기업 리뷰
- Page: https://www.teamblind.com/kr/company
- Review sample (구글코리아)

    ![구글코리아 공개 리뷰정보](https://user-images.githubusercontent.com/20942871/107968678-01544200-6ff2-11eb-88b9-2c2c65afb387.png)


>### ⚠ Disclaimer
> 리뷰 전체 상세내용을 확인하기 위해선 로그인 & 본인 기업 리뷰가 필요하기 때문에, **리뷰 제목과 평점, 직군 등의 오픈된 정보만 수집**하였습니다.


<br>


## Kibana Chart

- 아래 차트는 2020-07-01 ~ 2021-02-15 까지 작성된 리뷰 데이터로 생성되었습니다.

<br>

### NAVER 기업 분석 차트

![chart_NAVER](https://user-images.githubusercontent.com/20942871/108014349-02688c00-7051-11eb-8a0c-a3fb558c7a1e.PNG)

<br>

### 네카라 기업 비교 차트

![chart_기업비교](https://user-images.githubusercontent.com/20942871/108013900-0e078300-7050-11eb-8a74-1af6581dbe16.PNG)

<br>

## How to use?

1. `companies` 리스트에 블라인드에 등록된 기준의 회사명을 입력
2. `es_endpoint` 에 리뷰를 저장할 Elasticsearch 주소 입력

```python
if __name__ == '__main__':
    companies = [
        'NAVER', '카카오', '라인플러스', 'COUPANG', '우아한형제들',  # 네카라쿠배
        'NEXON', '넷마블', 'NCSOFT'  # 3N
    ]
    for c in companies:
        blind_parser = BlindParser(company=c, es_endpoint='http://localhost:9200')
        blind_parser.run()
```
