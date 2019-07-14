from urllib import request
from bs4 import BeautifulSoup
import re
import pandas as pd 
import urllib.parse
from collections import defaultdict
​
# ここで検索文字指定。
words = "オシアナス カシオ"
​
url_list = []
review_url_list = []
soruce_url = "https://kakaku.com/search_results/" + urllib.parse.quote(words, encoding='shift-jis')
​
print(soruce_url)
​
html = request.urlopen(soruce_url)
soup = BeautifulSoup(html, "html.parser")
a_tags = soup.find_all("a", attrs={"class", "p-result_item_btn_link p-result_item_btn_link-1 is-biggerlinkBigger"})
for a in a_tags:
  url_list.append(a.attrs['href'])
  
​
pattern = r'https://kakaku.com/item/(.*)/\?.*'
for url in url_list:
  
  m = re.search(pattern, url)
  uid = m.groups()[0]
  review_url = "https://review.kakaku.com/review/" + uid + "#tab" 
  review_url_list.append(review_url)
​
review_url_list = list(set(review_url_list))
print(review_url_list)
​
​
# ここから各ページの口コミタイトル、口コミ、商品名、URL、を取得します。
# もしページ送りがあれば、そのページも取得します。
d = defaultdict(list) 
​
while(review_url_list):
  review_url = review_url_list.pop()
  print(review_url)
  
  try:
    html = request.urlopen(review_url)
    soup = BeautifulSoup(html, "html.parser")
  except:
    continue
​
  # get title
  title_tags = soup.find_all("div", attrs={"class", "reviewTitle"})
  title_list = [t.text for t in title_tags]
​
  # get voc
  voc_tags = soup.find_all("p", attrs={"class", "revEntryCont"})
  voc_list = [v.text for v in voc_tags]
  
  # get product name
  product_name_tag = soup.find(itemprop="name")
  product_name = product_name_tag.text
​
  # next page
  next_page = soup.find("a", attrs={"class", "arrowNext01"})
  if next_page:
    next_path = next_page.get("href")
    next_url = "https://review.kakaku.com" + next_path
    print("next: " + next_url)
    review_url_list.append(next_url)
  
  for title, voc in zip(title_list, voc_list):
    d["product_name"].append(product_name)
    d["voc"].append(voc)
    d["title"].append(title)
    d["review_url"].append(review_url)
​
df = pd.DataFrame(d)
df.to_csv("./" + words + "_scraping.csv", encoding="utf_8_sig", index=False)
