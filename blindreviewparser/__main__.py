from argparse import ArgumentParser

from blindreviewparser.parser.blind_review_parser import BlindParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--es-endpoint', dest='es_endpoint', default='localhost:9200', help='리뷰를 저장할 ES Endpoint 를 지정 (기본값: localhost:9200)')
    parser.add_argument('--es-base64-auth', dest='es_base64_auth', default='', help='ES 보안이 있는경우 id:pw 를 base64 로 인코딩한 값 (기본값: 없음)')
    parser.add_argument('--p-num-start', dest='p_num_start', default=1, help='리뷰 페이지 시작번호 (이상)')
    parser.add_argument('--p-num-end', dest='p_num_end', default=300, help='리뷰 페이지 끝번호 (이하)')
    args = parser.parse_args()

    es_endpoint: str = args.es_endpoint
    es_base64_auth: str = args.es_base64_auth
    p_num_start: int = args.p_num_start
    p_num_end: int = args.p_num_end

    companies = [
        'NAVER', '네이버클라우드', '네이버웹툰', '네이버제트', '네이버랩스', '네이버파이낸셜', '스노우', '라인플러스', '라인프렌즈', '웍스모바일', '엔테크서비스',
        '카카오', '카카오뱅크', '카카오페이', '카카오커머스', '카카오모빌리티', '카카오메이커스', '카카오페이지', '카카오게임즈', '카카오엔터프라이즈',
        'COUPANG', '우아한형제들', '딜리버리히어로코리아', '하이퍼커넥트', '비바리퍼블리카', '당근마켓', '야놀자',
        'NHN', 'AhnLab', '한글과컴퓨터', '티맥스소프트', '카페24', '가비아',
        'NEXON', '넷마블', 'NCSOFT', 'NEOPLE', 'NEOWIZ', 'Smilegate', '펍지', '펄어비스', '크래프톤',
        'SK', 'SK텔레콤', 'SK플래닛', 'SK하이닉스', 'SK브로드밴드', '삼성전자', '삼성SDS', 'LG전자', 'LG CNS', 'LG유플러스', 'KT',
        'Facebook', 'Apple Korea', 'Amazon', '구글코리아', 'Microsoft', 'eBay Korea', '한국IBM', 'SAP코리아', '한국오라클'
    ]
    for company in companies:
        blind_parser = BlindParser(company=company, es_endpoint=es_endpoint, es_base64_auth=es_base64_auth)
        blind_parser.run(p_num_start=p_num_start, p_num_end=p_num_end)
