import requests
from bs4 import BeautifulSoup
def stock():
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=3481"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
    soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
    soup3 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
    soup4 = soup3.find("a").text.split("\xa0")
    soup_1 = soup.find("td",{"style":"padding:0 18px 5px 0;text-align:right;"})
    context = "{} {} 最新資訊 \n-------------------------- \n{}\n最新成交價 : {} \n開盤價 : {} \n最高價 : {} \n最低價 : {} \n漲跌幅 : {} \n--------------------------\n".format(soup4[0],soup4[1],soup_1.text,soup2[0],soup2[5],soup2[6],soup2[7],soup2[3])
    return context
