import requests
from bs4 import BeautifulSoup
import re

sess=requests.Session()
url_1="http://results.rvce.edu.in/viewresult2.php"
reg_dept=re.compile("(?<=1RV\d{2})[A-Z]{2}")
reg_year=re.compile("(?<=1RV)\d{2}")
semester = '8'

def get_dept(usn):
	return reg_dept.search(usn).group(0)


def get_year(usn):
	return reg_year.search(usn).group(0)


def change_dept(usn,next_dept):
	return reg_dept.sub(next_dept,usn)

def next_usn(usn):
	return re.sub('(\d{3})', lambda x: str(int(x.group(0)) + 1).zfill(3), usn)

def getElementFromResults(soup,pattern):
	return str(soup.find(attrs={'data-title':pattern}).string)

def getAllElementsFromResult(soup,pattern):
	return soup.find_all(attrs={'data-title':pattern})

def stripHtml(soup,resulatDict={},courseArray=[],blanks=0):
	if((soup.find(text=re.compile('(Result Not Found)|(Wrong Captcha Enter Again)')) == None ) and (len(soup(text=re.compile('Semester {0}'.format(semester))))!=0)) :
		if(len(courseArray)==0):
			for tag in getAllElementsFromResult(soup,'COURSE CODE'):
				courseArray.append(tag.text)

		usn = getElementFromResults(soup,'USN')
		resulatDict[usn]={}
		name = getElementFromResults(soup,'NAME')
		resulatDict[usn]['name'] = name
		sgpa = getElementFromResults(soup,'SGPA')
		resulatDict[usn]['sgpa'] = sgpa
		for i,tag in enumerate(getAllElementsFromResult(soup,'GRADE')):
			resulatDict[usn][courseArray[i]]=str(tag.string)
		blanks=0
	else:
		blanks+=1

	return blanks


def getLoginHtml(url):
	r = sess.get(url)
	return r.text

def getCaptchAns(soup):
	token = soup.body.find(text=re.compile('What is'))
	ans = str(token[7:-2])
	captcha = eval(ans)
	#print("The captcha answer is: {0}".format(captcha))
	return captcha

def getResultHtml(url,usn,captcha):
	headers = {'User-Agent': 'Mozilla/5.0'}
	params = {'usn':usn,'captcha':str(captcha)}
	r=sess.post(url_1,data=params,headers=headers)
	return(r.text)

def write(file,resultDict,courseArray):
	file.write('%-10s %14s'%('USN','SGPA'))
	for course in courseArray:
		file.write("%15s "%course)
	file.write('%30s\n'%('NAME'))
	for usn,data in resultDict.items():
			file.write('%-10s %14s'%(usn,data['sgpa']))
			for course in courseArray:
				file.write("%15s "%(data[course]))
			file.write('%30s\n'%(data['name']))





def run():
	resultDict = {}
	courseArray =[]
	blanks=0
	count =0
	usn = "1RV14CS000"
	deptList = ['BT','CH','CV','CS','EC','EE','EI','IS','ME','TE','IM','AS']
	for dept in deptList:
		usn = "1RV14CS000"
		resultDict = {}
		courseArray = []
		blanks = 0
		count = 0
		usn = change_dept(usn,dept)
		text_file = "sem_" + semester + " batch_" + str(get_year(usn)) + "_" + get_dept(usn) + ".txt"
		print("Department : " + get_dept(usn))
		while(True):
			loginHtml = getLoginHtml(url_1)
			captcha = getCaptchAns(BeautifulSoup(loginHtml,"lxml"))
			usn = next_usn(usn)
			resultHtml = getResultHtml(url_1,usn,captcha)
			soup = BeautifulSoup(resultHtml, "lxml")
			blanks = stripHtml(soup,resultDict,courseArray,blanks)
			count+=1
			print("done ",count,"blanks: ",blanks)
			if(count >30 and blanks>9):
				break

		resultFile = open(text_file,"w")
		write(resultFile,resultDict,courseArray)
		resultFile.close()


if __name__ == "__main__":
	run()