import requests
from bs4 import BeautifulSoup
import re

sess=requests.Session()
url_1="http://173.255.199.232:8001/results/getresults"
r=sess.get(url_1)
html=r.text
soup=BeautifulSoup(html,"lxml")

token=soup.find_all('meta',attrs={'name':'csrf-token'})[0].get('content')
reg_dept=re.compile("(?<=1RV\d{2})[A-Z]{2}")
reg_year=re.compile("(?<=1RV)\d{2}")

def get_dept(usn):
	return reg_dept.search(usn).group(0)


def get_year(usn):
	return reg_year.search(usn).group(0)


def change_dept(usn,next_dept):
	return reg_dept.sub(next_dept,usn)


def get_soup(param):


		url_2="http://173.255.199.232:8001/results/showresult?method=post"
		param['authenticity_token']=token

		r=sess.post(url_2,data=param)
		if r.url != url_2:
			return  BeautifulSoup("","lxml")
		return BeautifulSoup(r.text,"lxml")


def write(f,d):
	f.write("USN\t\t\tSGPA\t\t\tNAME\n")
	keys=d.keys()

	keys.sort()
	for x in keys:
			f.write(x)
			f.write("\t\t\t")
			f.write(d[x]['sgpa'])
			f.write("\t\t\t")
			f.write(d[x]['name'])
			f.write("\n")


def next_usn(usn):
	return re.sub('(\d{3})', lambda x: str(int(x.group(0)) + 1).zfill(3), usn)


def run():
	#parameters for filling the form
	param={
			'result[usn]':'1RV12AA000',
			'result[department]':'5687f1d86e95525d0e0000b6',
			'result[sem]':'8',
			'result[year]':'2016',

			}

	dept_keys={
					'BT':"5687ee086e95525d0e000024",
					'CH':"5687f1796e95525d0e0000b4",
					'CV':"5687f1b26e95525d0e0000b5",
					'CS':"5687f1d86e95525d0e0000b6",
					'EC':"5687f1ef6e95525d0e0000b7",
					'EE':"5687f2126e95525d0e0000b8",
					'EI':"568901416e955220e1000017",
					'IS':"5687f2426e95525d0e0000ba",
					'ME':"5687f2e36e95525d0e0000bc",
					'TE':"5687f2fb6e95525d0e0000bd",
					'IM':"5687f2286e95525d0e0000b9",
					'AS':"5688daaf6e955220e1000001",
				  }

	dept=dept_keys.keys()
	dept.sort()
	usn_default=param['result[usn]']

	for x in dept:
		blanks=0
		counter=0
		results_dict={}
		param['result[department]']=dept_keys[x]
		usn=param['result[usn]']=change_dept(usn_default,x)
		present_year=16
		text_file="sem_"+str(param['result[sem]'])+" batch_"+str(get_year(usn))+"_"+get_dept(usn)+".txt"
		usn_default=param['result[usn]']
		print"Department : "+get_dept(usn)

		while True:
			param['result[usn]']=next_usn(usn)
			usn=param['result[usn]']
			counter+=1
			blanks=strip_html(get_soup(param),results_dict,blanks)
			print "done ",counter,
			print "blanks",blanks
			if(counter>30 and blanks>=8):
				break


		if len(results_dict)!=0:
			marks_file=open(text_file,"w")
			write(marks_file,results_dict)
			marks_file.close()

		print "\n\n\n"









def find_stuff(tag):
	return( re.compile('(USN|NAME|SGPA)').search(str(tag.string)))


def strip_html(soup,d,blanks):
	data=[]
	for i in soup.find_all(find_stuff):
		for j in i.parent.stripped_strings:
			data.append(str(j))

	try:
		d.update({data[1]:{'name':data[3],'sgpa':data[5]}})

	except:
		blanks+=1
	else :
		blanks=0

	return  blanks


if __name__=="__main__":
	run()