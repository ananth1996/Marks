import requests
from bs4 import BeautifulSoup
import re
import ast



sess=requests.Session()
url_1="https://pesuacademy.com/Academy/tr/result/01FB14ECS009"
headers = {'User-Agent': 'Mozilla/5.0'}
r=sess.get(url_1,verify=False, headers=headers)
html=r.text
print(html)
'''
soup=BeautifulSoup(html,"lxml")
token = soup.body.findAll(text=re.compile('What is'))[0]
ans = str(token[7:-2])
captcha = eval(ans)
headers = {'User-Agent': 'Mozilla/5.0'}
params = {'usn':'1RV16CS150','captcha':str(captcha)}
r=sess.post(url_1,data=params,headers=headers)
html=r.text


print(html)
'''
