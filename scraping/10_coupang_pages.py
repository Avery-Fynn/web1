import requests
import re
from bs4 import BeautifulSoup

headers = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

for i in range(1, 6):
    # print("페이지:", i)
    url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=1=5&backgroundColor=".format(
        i)

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    items = soup.find_all("li", attrs={"class": re.compile("^search-product")})
    # print(items[0].find("div", attrs={"class": "name"}).get_text())

    for item in items:

        ad_badge = item.find("span", attrs={"class": "ad-badge-text"})
        if ad_badge:
            # print("<광고 상품 제외>")
            continue

        name = item.find("div", attrs={"class": "name"}).get_text()
        if "Apple" in name:
            # print("<Apple 상품 제외>")
            continue

        price = item.find("strong", attrs={"class": "price-value"})
        if price:
            price = price.get_text()
        else:
            # print("<가격 없는 상품 제외>")
            continue

        # 리뷰 100개 이상, 평점 4.7 이상만 조회

        rate = item.find("em", attrs={"class": "rating"})
        if rate:
            rate = rate.get_text()
        else:
            # print("<평점 없는 상품 제외>")
            continue

        rate_cnt = item.find(
            "span", attrs={"class": "rating-total-count"})
        if rate_cnt:
            rate_cnt = rate_cnt.get_text()[1:-1]
        else:
            # print("<평점 수 없는 상품 제외>")
            continue

        link = item.find("a", attrs={"class": "search-product-link"})["href"]

        if float(rate) >= 4.98 and int(rate_cnt) >= 700:
            print(f"제품명 : {name}")
            print(f"가격 : {price}")
            print(f"평점 : {rate}점 ({rate_cnt}개)")
            print("바로가기 : {}".format("http://www.coupang.com" + link))
            print("-"*100)
