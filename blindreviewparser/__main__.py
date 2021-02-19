from blindreviewparser.parser.blind_review_parser import BlindParser

if __name__ == '__main__':
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
        blind_parser = BlindParser(company=company, es_endpoint='http://localhost:9200')
        blind_parser.run()
