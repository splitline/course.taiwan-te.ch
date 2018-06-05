from parser.models import Courses
import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep

# Courses.objects.all().delete()

t = requests.get("http://140.118.31.215/querycourse/ChCourseQuery/QueryCondition.aspx")
soup = BeautifulSoup(t.text,'html.parser')
all_input = soup.find_all("input")
now_semester = soup.find("select").find('option').get('value')

DAYS = {
	"M": 1,
	"T": 2, 
	"W": 3, 
	"R": 4,
	"F": 5, 
	"S": 6, 
	"U": 7, 
}



TIMES = {
	'0':  '07:10-08:00',
	'1':  '08:10-09:00',
	'2':  '09:10-10:00',
	'3':  '10:20-11:10',
	'4':  '11:20-12:10',
	'5':  '12:20-13:10',
	'6':  '13:20-14:10',
	'7':  '14:20-15:10',
	'8':  '15:30-16:20',
	'9':  '16:30-17:20',
	'10': '17:30-18:20',
	'A':  '18:25-19:15',
	'B':  '19:20-20:10',
	'C':  '20:10-21:05',
	'D':  '21:10-22:00'
}

# code_list = ["AC","FL","AD","FN","AT","GE","BA","GX","BB","HC","BE","IB","CC","IM","CD","MA","MB","CE","MB","CH","ME","CI","MG","CS","MI","CT","MS","CX","PA","DE","PE","DT","RD","EC","SA","EE","TB","EN","TC","EO","TE","EP","TM","ET","TX","FB","VE","FE"]
code_list = ['GE', 'GX', 'CD', 'MS', 'DE', 'SA', 'TE', 'FE']
failed = []
# outline_link = "http://info.ntust.edu.tw/faith/edua/app/qry_linkoutline.aspx?semester=1061&courseno=CS2003301"

for code in code_list:
	print("==================", code, "==================")
	courses_list = requests.post(
		"http://140.118.31.215/querycourse/ChCourseQuery/QueryCondition.aspx",
		data = {
			"__VIEWSTATE": all_input[0].get('value'),
			"__VIEWSTATEGENERATOR": all_input[1].get('value'),
			"__EVENTVALIDATION": all_input[2].get('value'),
			"semester_list": now_semester,
			"__EVENTARGUMENT": "",
			"__LASTFOCUS": "",
			"__EVENTTARGET": "",
			"Acb0101": "on",
			"BCH0101": "on",
			"Ctb0101": code, 
			"Ctb0201": "",
			"Ctb0301": "",
			"QuerySend": "送出查詢"
		}
	)
	soup = BeautifulSoup(courses_list.text.encode('utf-8'),'html.parser')
	if len(soup.find_all('tr', bgcolor="White")) == 0:
		failed.append(code)
	for item in soup.find_all('tr', bgcolor="White"):
		course = item.find_all('td')
		course_id = str(course[0].string).strip() 
		if course_id != "":
			outline = requests.get("http://info.ntust.edu.tw/faith/edua/app/qry_linkoutline.aspx?semester="+now_semester[:4]+"&courseno="+course_id)
			sleep(1.23) # _(:з」∠)_
			outline_soup = BeautifulSoup(outline.text, 'html.parser')
			class_time = str(outline_soup.find(id='lbl_timenode').string).strip()
			ntuTri = course_id.startswith("3T") or course_id.startswith("3N")
			if ntuTri:
				classroom = str(course[9].string).strip()
			else:
				classroom = class_time

			periods = []
			print(course_id, class_time, class_time.split("   "))
			
			for time in list(filter(None, class_time.split("   "))):
				period = {}
				if re.match('(\w\w)\((\S+)?\)', time) is not None:
					result = re.match('(\w\w)\((\S+)?\)', time)
					period['day_code'] = result[1]
					period['location'] = result[2]
				else:
					period['day_code'] = time
					period['location'] = ""
					
				if ntuTri:
					period['location'] = classroom
				period['day'] = DAYS[period['day_code'][0]]
				period['time'] = TIMES[period['day_code'][1:]]
				periods.append(period)
			periods = json.dumps(periods)
			
			print(course[2].string, course[7], str(course[7].string).strip(), course[7].string)
			course_obj = Courses(
					semester = now_semester[:4],
					course_id = course_id,
					ge_type = str(course[1].string).strip(),
					name = str(course[2].string).strip(),
					outline_link = str(course[3].a['href']).strip(),
					credit = int(str(course[4].string).strip()),
					required_subject = (str(course[5].string) == "必"),
					lecturer = str(course[7].text).strip(),
					classroom = classroom,
					periods = periods,
					note = str(course[14].string).strip(),
				)
			course_obj.save()


print(failed)

# Courses(
# 	semester = "1061",
# 	course_id = "CS101",
# 	ge_type = "",
# 	name = "CSIEEEE",
# 	outline_link = "goo.gl",
# 	credit = 3,
# 	required_subject = True,
# 	lecturer = "OWO",
# 	classroom = "classroom-212",
# 	periods = "[]",
# 	note = "",
# )
# for i in courses :
#     print(i.outline)
# print(len(courses))