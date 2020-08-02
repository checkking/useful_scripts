#coding:utf-8

import xlrd
import xlwt
import sys
import time
import MySQLdb
import json
from HTMLParser import HTMLParser
import re
reload(sys)
sys.setdefaultencoding('utf-8')


class SummaryParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.h2 = []
		self.p = []
		self.h2_index = -1
		self.gaishu = ''
		self.fengxian = ''
		self.nandu = ''

	def handle_starttag(self, tag, attrs):
		HTMLParser.handle_starttag(self, tag, attrs)
		if tag == 'h2':
			self.h2_index = self.h2_index + 1
	
	def handle_endtag(self, tag):
		HTMLParser.handle_endtag(self, tag)

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		data = data.strip()
		if data == '':
			return
		if self.lasttag == 'p':
			self.p.append(data)
			if self.h2_index == 0:
				self.gaishu = data
			elif self.h2_index == 2:
				self.fengxian = data
			elif self.h2_index == 3:
				self.nandu = data
		elif self.lasttag == 'h2':
			self.h2.append(data)

class CrowdParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.h2 = []
		# 元素为li的数组
		self.ul_index = -1
		self.shihe = ''
		self.jingji = ''
		self.in_strong = False
		self.h2_index = -1

	def handle_starttag(self, tag, attrs):
		HTMLParser.handle_starttag(self, tag, attrs)
		if tag == 'ul':
			self.ul_index = self.ul_index + 1
		elif tag == 'strong':
			self.in_strong = True
		elif tag == 'h2':
			self.h2_index = self.h2_index + 1
	
	def handle_endtag(self, tag):
		HTMLParser.handle_endtag(self, tag)
		if tag == 'strong':
			self.in_strong = False

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		data = data.strip()
		if data == '':
			return
		if self.in_strong:
			data = data.strip('u：').strip(':')
			if self.h2_index == 0:
				if self.shihe == '':
					self.shihe = data
				else:
					self.shihe = self.shihe + '、' + data
			elif self.h2_index == 1:
				if self.jingji == '':
					self.jingji = data
				else:
					self.jingji = self.jingji + '、' + data
		elif self.lasttag == 'h2':
			self.h2.append(data)

class ShuqianParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.h2 = []
		self.h2_index = -1
		self.ul_depth = 0
		self.in_strong = False
		self.in_ul = False
		self.in_li = False
		self.peihe_start = False
		self.buwei = ''
		self.jiancha = ''
		self.peihe = ''

	def handle_starttag(self, tag, attrs):
		HTMLParser.handle_starttag(self, tag, attrs)
		if tag == 'h2':
			self.h2_index = self.h2_index + 1
		elif tag == 'ul':
			self.ul_depth = self.ul_depth + 1
			self.in_ul = True
		elif tag == 'strong':
			self.in_strong = True
		elif tag == 'li':
			self.in_li = True
	
	def handle_endtag(self, tag):
		HTMLParser.handle_endtag(self, tag)
		if tag == 'ul':
			self.ul_depth = self.ul_depth - 1
			self.in_ul = False
		elif tag == 'strong':
			self.in_strong = False
		elif tag == 'li':
			self.in_li = False

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		data = data.strip()
		if data == '':
			return
		if self.lasttag == 'h2':
			if self.h2_index == 0:
				# matchObj = re.match( r'手术部位：(.*)', data, re.M|re.I)
				# if matchObj:
					#self.buwei = matchObj.group(1)
				pos = data.find('：')
				if pos > 0:
					self.buwei = data[pos+1:]
				elif pos == -1:
					pos = data.find(':')
					if pos > 0:
						self.buwei = data[pos+1:]
			self.h2.append(data)
		elif self.lasttag == 'strong' and self.in_strong:
			if data.find('配合医务人员工作') is not -1:
				self.peihe_start = True
			elif self.h2_index == 3:
				data = data.strip("：").strip(':').strip('：')
				if self.ul_depth == 2 and self.peihe_start:
					if self.peihe == '':
						self.peihe = data
					elif data != u'其他':
						self.peihe = self.peihe + '、' + data
		elif self.h2_index == 2 and self.in_ul and self.ul_depth == 1 and not self.in_strong and self.in_li:
			data = data.strip('：')
			if data == '':
				return
			if self.jiancha == '':
				self.jiancha = data
			else:
				self.jiancha = self.jiancha + ';' + data

class ProcessParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.mazui = ''
		self.juti = ''
		self.mazui_occured = False
		self.juti_occured = False
		self.in_strong = False
		self.li_index = 0
		self.in_li = False
		self.ul_index = 0
		self.juti_index = 0
		self.h2_index = -1

	def handle_starttag(self, tag, attrs):
		HTMLParser.handle_starttag(self, tag, attrs)
		if tag == 'strong':
			self.in_strong = True
		elif tag == 'li':
			self.li_index = self.li_index + 1
			self.in_li = True
		elif tag == 'ul':
			self.ul_index = self.ul_index + 1
		elif tag == 'h2':
			self.h2_index = self.h2_index + 1

	def handle_endtag(self, tag):
		HTMLParser.handle_endtag(self, tag)
		if tag == 'strong':
			self.in_strong = False
		elif tag == 'li':
			self.n_li = True

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		data = data.strip(':').strip('：').strip()
		if data == '':
			return
		if data.find(u'麻醉') is not -1 and self.li_index == 1 and self.in_strong:
			self.mazui_occured = True
		elif data.find(u'手术具体') is not -1 and self.li_index == 2 and self.in_strong:
			self.juti_occured = True
		elif self.li_index == 1 and self.mazui_occured:
			self.mazui = data
		elif self.juti_occured and not self.in_strong and self.ul_index == 2 and self.h2_index == 0:
			self.juti_index = self.juti_index + 1
			if self.juti_index == 1:
				self.juti = data
			else:
				self.juti = self.juti + ";" + data

class ShuhouParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.h2_index = -1
		self.huli_index = 0
		self.kangfu_index = 0
		self.fucha_index = 0
		self.in_li = False
		self.in_strong = False
		self.in_p = False
		self.huli = ''
		self.kangfu = ''
		self.fucha = ''

	def handle_starttag(self, tag, attrs):
		HTMLParser.handle_starttag(self, tag, attrs)
		if tag == 'h2':
			self.h2_index = self.h2_index + 1
		elif tag == 'li':
			self.in_li = True
		elif tag == 'strong':
			self.in_strong = True
		elif tag == 'p':
			self.in_p = True

	def handle_endtag(self, tag):
		HTMLParser.handle_endtag(self, tag)
		if tag == 'li':
			self.in_li = False
		elif tag == 'strong':
			self.in_strong = False
		elif tag == 'p':
			self.in_p = False

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		# data = data.strip(':').strip('：').strip()
		data = data.strip()
		if data == '' or data == ':' or data == u'：':
			return
		if self.h2_index == 1 and self.in_li and not self.in_strong:
			data = data.strip(':').strip('：').strip()
			self.huli_index = self.huli_index + 1
			if self.huli_index == 1:
				self.huli = self.huli + '%d.%s' % (self.huli_index, data)
			else:
				self.huli =  self.huli + '@@@%d.%s' % (self.huli_index, data)
		elif self.h2_index == 2:
			if self.in_li:
				if self.in_strong:
					self.kangfu_index = self.kangfu_index + 1
					pre = ''
					if self.kangfu_index > 1:
						pre = '@@@'
					self.kangfu = self.kangfu + '%s%d.%s' % (pre, self.kangfu_index, data)
				else:
					self.kangfu = self.kangfu + data
			elif self.in_p:
				self.kangfu = data
		elif self.h2_index == 3:
			if self.in_li:
				if self.in_strong:
					self.fucha_index = self.fucha_index + 1
					pre = ''
					if self.fucha_index > 1:
						pre = '@@@'
					self.fucha = self.fucha + '%s%d.%s' % (pre, self.fucha_index, data)
				else:
					self.fucha = self.fucha + data
			elif self.in_p:
				self.fucha = data


def db_query(sql, fetch=True):
	db = MySQLdb.connect(host="tencarepedia.mdb.mig", port=15905, user="readonly", passwd="uDwKLGb2Mf@20o", db="yidian_online", charset="utf8")
	cursor = db.cursor()
	cursor.execute(sql)
	if fetch:
		return cursor.fetchall()


def getContent(docid, ctype):
	sql = "select content from content where docid='{0}' and ctype={1} limit 1".format(docid, ctype)
	results = db_query(sql)
	if len(results) == 1:
		row = results[0]
		content = row[0].replace('\\n', '').replace('\\t', '').replace('&nbsp;', '')
		return content
	return ""

def readDocids(file_path):
	xlsx = xlrd.open_workbook(file_path)
	tab = xlsx.sheet_by_index(0)
	nrows = tab.nrows
	docids = []
	for i in range(nrows):
		if i == 0:
			continue
		row = tab.row(i)
		docid = row[0].value.strip()
		docids.append(docid)
	return docids

def getTitleAndDepart(did):
	sql = "select disease, disdepart from disease where did={0} limit 1".format(did)
	results = db_query(sql)
	if len(results) == 1:
		row = results[0]
		title, depart  = row[0], row[1]
		return title, depart
	return ("", "")


def getRelatedContents(related_docids):
	contents = []
	for docid in related_docids:
		content = getContent(docid, 313)
		d = json.loads(content)
		contents.append(d['content'])
	return contents

def filterRawdata(data):
	data = data.replace('\\n', '').replace('\\t', '')
	return data

def getInnerContent(raw_content):
	d = json.loads(raw_content)
	content = d['content']
	return content



def parseContent(docid, content):
	d = json.loads(content)
	did = int(d['title'])
	raw_content = d['content']
	related_docids = d['related_docid']
	# get title and depart
	title, depart = getTitleAndDepart(did)
	# get related_docids
	if len(related_docids) is not 5:
		raise RuntimeError("docid:{0} related_docid invalid:{1}".format(docid, related_docids))
	related_contents = getRelatedContents(related_docids)
	# parse contents
	parsers = []
	# summary
	summ_content = filterRawdata(raw_content)
	summ_parser = SummaryParser()
	summ_parser.feed(summ_content)
	parsers.append(summ_parser)
	# crowd
	crowd_content = filterRawdata(related_contents[0])
	crowd_parser = CrowdParser()
	crowd_parser.feed(crowd_content)
	parsers.append(crowd_parser)
	# shuqian
	shuqian_content = filterRawdata(related_contents[1])
	shuqian_parser = ShuqianParser()
	shuqian_parser.feed(shuqian_content)
	parsers.append(shuqian_parser)
	# process
	process_content = filterRawdata(related_contents[2])
	process_parser = ProcessParser()
	process_parser.feed(process_content)
	parsers.append(process_parser)
	# shuhou
	shuhou_content = filterRawdata(related_contents[3])
	shuhou_parser = ShuhouParser()
	shuhou_parser.feed(shuhou_content)
	parsers.append(shuhou_parser)
	return title, depart, parsers

def main():
	file_path = './data/20200605/shoushu_input.xlsx'
	out_path = './data/output.xls'
	output_excel = xlwt.Workbook()
	sheet1 = output_excel.add_sheet('Sheet1')
	titles_cn = ['docid', u'词条名', u'概述', u'适应症', u'禁忌症', u'就诊科室', u'手术部位', u'麻醉方式', u'风险', u'难度', u'需要做哪些检查', u'需要配合医务人员', u'过程', u'护理', u'康复过程', u'如何复查']
	titles_en = ['key', 'title', 'tab_summary', 'tab_qas_question', 'tab_qas_question', 'tap_tip_value', 'tap_tip_value', 'tap_tip_value', 'tab_summary', 'tab_qas_answer', 'tab_qas_answer', 'tab_qas_answer', 'tab_summary', 'tab_summary', 'tab_qas_answer', 'tab_qas_answer']
	for i in range(len(titles_cn)):
		sheet1.write(0, i, titles_cn[i])
	for i in range(len(titles_en)):
		sheet1.write(1, i, titles_en[i])
	docids = readDocids(file_path)
	row = 1
	for docid in docids:
		content = getContent(docid, 13)
		try:
			title, depart, parsers = parseContent(docid, content)
		except RuntimeError as e:
			print(e)
			continue
		row = row + 1
		summ_parser = parsers[0]
		crowd_parser = parsers[1]
		shuqian_parser = parsers[2]
		process_parser = parsers[3]
		shuhou_parser = parsers[4]
		# docid
		sheet1.write(row, 0, docid)
		# title
		sheet1.write(row, 1, title)
		# 概述
		sheet1.write(row, 2, summ_parser.gaishu)
		#适应症
		sheet1.write(row, 3, crowd_parser.shihe)
		# 禁忌
		sheet1.write(row, 4, crowd_parser.jingji)
		# 科室
		sheet1.write(row, 5, depart)
		# 手术部位
		sheet1.write(row, 6, shuqian_parser.buwei)
		# 麻醉方式
		sheet1.write(row, 7, process_parser.mazui)
		# 风险
		sheet1.write(row, 8, summ_parser.fengxian)
		# 难度
		sheet1.write(row, 9, summ_parser.nandu)
		# 需要做哪些检查
		sheet1.write(row, 10, shuqian_parser.jiancha)
		# 需要配合医务人员
		sheet1.write(row, 11, shuqian_parser.peihe)
		# 过程
		sheet1.write(row, 12, process_parser.juti)
		# 护理
		sheet1.write(row, 13, shuhou_parser.huli)
		# 康复过程
		sheet1.write(row, 14, shuhou_parser.kangfu)
		# 如何复查
		sheet1.write(row, 15, shuhou_parser.fucha)
		time.sleep(0.01)
	output_excel.save(out_path)

if __name__ == '__main__':
	main()

