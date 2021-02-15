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

### 네카라쿠배

<details>
  <summary>차트보기</summary>

### NAVER
![chart_NAVER](https://user-images.githubusercontent.com/20942871/107969046-88091f00-6ff2-11eb-8e95-fa7d921170bc.PNG)

<br>

#### 카카오
![chart_카카오](https://user-images.githubusercontent.com/20942871/107969221-d28a9b80-6ff2-11eb-858f-fab57c8ed82e.PNG)

<br>

### 라인플러스
![chart_라인플러스](https://user-images.githubusercontent.com/20942871/107969238-d9191300-6ff2-11eb-8354-cb2512e9fdda.PNG)

<br>

### COUPANG
![chart_COUPANG](https://user-images.githubusercontent.com/20942871/107969260-dfa78a80-6ff2-11eb-99a5-7ff3024494ef.PNG)

<br>

### 우아한형제들
![chart_우아한형제들](https://user-images.githubusercontent.com/20942871/107969294-ed5d1000-6ff2-11eb-8aff-a317ca3ba2ad.PNG)

</details>

<br>

### 3N

<details>
  <summary>차트보기</summary>

### NEXON
![chart_NEXON](https://user-images.githubusercontent.com/20942871/107969570-488f0280-6ff3-11eb-9c8b-51b13362a027.PNG)

<br>

### 넷마블
![chart_넷마블](https://user-images.githubusercontent.com/20942871/107969606-547ac480-6ff3-11eb-882c-517a37d0f28e.PNG)

<br>

### NCSOFT
![chart_NCSOFT](https://user-images.githubusercontent.com/20942871/107969637-5d6b9600-6ff3-11eb-9c6f-17122b001815.PNG)

</details>

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
