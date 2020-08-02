#coding:gbk

# 手术xml输出

import xlrd
import xml.dom.minidom as minidom
import sys
reload(sys)
sys.setdefaultencoding('gbk')

class Config1(object):
	def __init__(self):
		self.key = ""
		self.title = ""
		self.url = ""
		self.expert_name = ""
		self.expert_pic = ""
		self.expert_title = ""
		self.expert_hospital = ""
		self.expert_hospital_level = ""
		self.expert_department = ""
		self.expert_url = ""
		self.expert_pc_url = ""
		self.authority = ""
		self.authority_url = ""

class Config2(object):
	def __init__(self):
		self.key = ""
		self.title = ""
		self.tab_summary1 = ""
		self.tab_url1 = ""
		self.tab_summary2 = ""
		self.tab_url2 = ""
		self.tab_summary3 = ""
		self.tab_url3 = ""
		self.tab_summary4 = ""
		self.tab_url4 = ""
		self.tab_summary5 = ""
		self.tab_url5 = ""
		

class Config3(object):
	def __init__(self):
		self.key = ""
		self.title = ""
		self.tap_tip_value1 = ""
		self.tap_tip_value2 = ""
		self.tap_tip_value3 = ""

class Config4(object):
	def __init__(self):
		self.key = ""
		self.title = ""
		self.tab_qas_answer1 = ""
		self.tab_qas_url1 = ""
		self.tab_qas_answer2 = ""
		self.tab_qas_url2 = ""
		self.tab_qas_answer3 = ""
		self.tab_qas_url3 = ""
		self.tab_qas_answer4 = ""
		self.tab_qas_url4 = ""
		self.tab_qas_answer5 = ""
		self.tab_qas_url5 = ""
		self.tab_qas_answer6 = ""
		self.tab_qas_url6 = ""
		self.tab_qas_answer7 = ""
		self.tab_qas_url7 = ""

class Config5(object):
	def __init__(self):
		self.key = ""
		self.title = ""
		self.tab_pic_title = ""	
		self.tab_pic_url = ""	
	
def parseConfig1(tab):
	nrows = tab.nrows
	cfgs = []
	for i in range(nrows):
		if i == 0:
			continue
		cfg1 = Config1()
		row = tab.row(i)
		cfg1.key = row[0].value
		cfg1.title = row[1].value
		cfg1.url = row[2].value
		cfg1.expert_name = row[3].value
		cfg1.expert_pic = row[4].value
		cfg1.expert_title = row[5].value
		cfg1.expert_hospital = row[6].value
		cfg1.expert_hospital_level = row[7].value
		cfg1.expert_department = row[8].value
		cfg1.expert_url = row[9].value
		cfg1.expert_pc_url = row[10].value
		cfg1.authority = row[11].value
		cfg1.authority_url = row[12].value
		cfgs.append(cfg1)
	return cfgs

def parseConfig2(tab):
	nrow = tab.nrows
	cfgs = {}
	for i in range(nrow):
		if i <= 1:
			continue
		cfg2 = Config2()
		row = tab.row(i)
		cfg2.key = row[0].value
		cfg2.title = row[1].value
		cfg2.tab_summary1 = row[2].value
		cfg2.tab_url1 = row[3].value
		cfg2.tab_summary2 = row[4].value
		cfg2.tab_url2 = row[5].value
		cfg2.tab_summary3 = row[6].value
		cfg2.tab_url3 = row[7].value
		cfg2.tab_summary4 = row[8].value
		cfg2.tab_url4 = row[9].value
		cfg2.tab_summary5 = row[10].value
		cfg2.tab_url5 = row[11].value
		cfgs[cfg2.key] = cfg2
	return cfgs

def parseConfig3(tab):
	nrow = tab.nrows
	cfgs = {}
	for i in range(nrow):
		if i <= 1:
			continue
		cfg3 = Config3()
		row = tab.row(i)
		cfg3.key = row[0].value
		cfg3.title = row[1].value
		cfg3.tap_tip_value1 = row[2].value
		cfg3.tap_tip_value2 = row[3].value
		cfg3.tap_tip_value3 = row[4].value
		cfgs[cfg3.key] = cfg3
	return cfgs

def parseConfig4(tab):
	nrow = tab.nrows
	cfgs = {}
	for i in range(nrow):
		if i <= 1:
			continue
		cfg4 = Config4()
		row = tab.row(i)
		cfg4.key = row[0].value
		cfg4.title = row[1].value
		cfg4.tab_qas_answer1 = row[2].value
		cfg4.tab_qas_url1 = row[3].value
		cfg4.tab_qas_answer2 = row[4].value
		cfg4.tab_qas_url2 = row[5].value
		cfg4.tab_qas_answer3 = row[6].value
		cfg4.tab_qas_url3 = row[7].value
		cfg4.tab_qas_answer4 = row[8].value
		cfg4.tab_qas_url4 = row[9].value
		cfg4.tab_qas_answer5 = row[10].value
		cfg4.tab_qas_url5 = row[11].value
		cfg4.tab_qas_answer6 = row[12].value
		cfg4.tab_qas_url6 = row[13].value
		cfg4.tab_qas_answer7 = row[14].value
		cfg4.tab_qas_url7 = row[15].value

		cfgs[cfg4.key] = cfg4
	return cfgs

def parseConfig5(tab):
	nrow = tab.nrows
	cfgs = {}
	for i in range(nrow):
		if i <= 0:
			continue
		cfg5 = Config5()
		row = tab.row(i)
		cfg5.key = row[0].value
		cfg5.title = row[1].value
		cfg5.tab_pic_title = row[2].value
		cfg5.tab_pic_url = row[3].value
		cfgs[cfg5.key] = cfg5
	return cfgs

def withCData(s):
	cd = minidom.CDATASection()
	cd.data = s
	cd.nodeType = cd.TEXT_NODE
	return cd

def outputXml(tab1Datas, tab2Datas, tab3Datas, tab4Datas, tab5Datas):
	dom = minidom.getDOMImplementation().createDocument(None,'DOCUMENT',None)
	root = dom.documentElement
	for t1_data in tab1Datas:
		t2_data = None
		t3_data = None
		t4_data = None
		t5_data = None
		if t1_data.key in tab2Datas:
			t2_data = tab2Datas[t1_data.key]
		else:
			raise RuntimeError('tabs not matched! key: {0} not in tab2'.format(t1_data.key))
		if t1_data.key in tab3Datas:
			t3_data = tab3Datas[t1_data.key]
		if t1_data.key in tab4Datas:
			t4_data = tab4Datas[t1_data.key]
		if t1_data.key in tab5Datas:
			t5_data = tab5Datas[t1_data.key]
		if t2_data is None or t3_data is None or t4_data is None or t5_data is None:
			raise RuntimeError('tabs not matched! key:' + t1_data.key)
		item = dom.createElement('item')
		#  add key
		keyNode = dom.createElement('key')
		keyNode.appendChild(withCData(t1_data.key))
		item.appendChild(keyNode)
		# add display
		displayNode = dom.createElement('display')
		# add title
		titleNode = dom.createElement('title')
		titleNode.appendChild(withCData(t1_data.title))
		displayNode.appendChild(titleNode)
		# add url
		urlNode = dom.createElement('url')
		urlNode.appendChild(withCData(t1_data.url))
		displayNode.appendChild(urlNode)
		# add pc url
		pcUrlNode = dom.createElement('pc_url')
		pcUrlNode.appendChild(withCData(t1_data.url))
		displayNode.appendChild(pcUrlNode)
		# add tab list
		tabLNode = dom.createElement('tab_list')
		# add tab name
		tabNameNode = dom.createElement('tab_name')
		tabNameNode.appendChild(withCData(u'概述'))
		tabLNode.appendChild(tabNameNode)
		# add tab url
		tabUrlNode = dom.createElement('tab_url')
		tabUrlNode.appendChild(withCData(t2_data.tab_url1))
		tabLNode.appendChild(tabUrlNode)
		# add tab pc url
		tabPcUrlNode = dom.createElement('tab_pc_url')
		tabPcUrlNode.appendChild(withCData(t2_data.tab_url1))
		tabLNode.appendChild(tabPcUrlNode)
		# add tab summary
		tabSummNode = dom.createElement('tab_summary')
		tabSummNode.appendChild(withCData(t2_data.tab_summary1))
		tabLNode.appendChild(tabSummNode)
		# add tab tips
		tabTipsNode = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName = dom.createElement('tab_tips_name')
		tabTipsTabName.appendChild(withCData(u'就诊科室'))
		tabTipsNode.appendChild(tabTipsTabName)
		# -- add tap_tip_value
		tabTipsTipValue = dom.createElement('tap_tip_value')
		tabTipsTipValue.appendChild(withCData(t3_data.tap_tip_value1))
		tabTipsNode.appendChild(tabTipsTipValue)
		tabLNode.appendChild(tabTipsNode)
		# add tab tips 2
		tabTipsNode2 = dom.createElement('tab_tips')
		# -- add tab_name 2
		tabTipsTabName2 = dom.createElement('tab_tips_name')
		tabTipsTabName2.appendChild(withCData(u'手术部位'))
		tabTipsNode2.appendChild(tabTipsTabName2)
		# -- add tap_tip_value 2
		tabTipsTipValue2 = dom.createElement('tap_tip_value')
		tabTipsTipValue2.appendChild(withCData(t3_data.tap_tip_value2))
		tabTipsNode2.appendChild(tabTipsTipValue2)
		tabLNode.appendChild(tabTipsNode2)
		# add tab tips 3
		tabTipsNode3 = dom.createElement('tab_tips')
		# -- add tab_name 3
		tabTipsTabName3 = dom.createElement('tab_tips_name')
		tabTipsTabName3.appendChild(withCData(u'麻醉方式'))
		tabTipsNode3.appendChild(tabTipsTabName3)
		# -- add tap_tip_value 3
		tabTipsTipValue3 = dom.createElement('tap_tip_value')
		tabTipsTipValue3.appendChild(withCData(t3_data.tap_tip_value3))
		tabTipsNode3.appendChild(tabTipsTipValue3)
		tabLNode.appendChild(tabTipsNode3)

		# add tab_qas
		tabQasNode = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode = dom.createElement('tab_qas_question')
		tabQasQNode.appendChild(withCData(u'适应症'))
		tabQasNode.appendChild(tabQasQNode)

		# -- add tab_qas_answer
		tabQasANode = dom.createElement('tab_qas_answer')
		tabQasANode.appendChild(withCData(t4_data.tab_qas_answer1))
		tabQasNode.appendChild(tabQasANode)

		# -- add tab_qas_url
		tabQasUrlNode = dom.createElement('tab_qas_url')
		tabQasUrlNode.appendChild(withCData(t4_data.tab_qas_url1))
		tabQasNode.appendChild(tabQasUrlNode)

		# -- add tab_qas_pc_url
		tabQasPcUrlNode = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode.appendChild(withCData(t4_data.tab_qas_url1))
		tabQasNode.appendChild(tabQasPcUrlNode)

		tabLNode.appendChild(tabQasNode)

		# add tab_qas 2
		tabQasNode2 = dom.createElement('tab_qas')
		# -- add tab_qas_question 2
		tabQasQNode2 = dom.createElement('tab_qas_question')
		tabQasQNode2.appendChild(withCData(u'禁忌症'))
		tabQasNode2.appendChild(tabQasQNode2)

		# -- add tab_qas_answer 2
		tabQasANode2 = dom.createElement('tab_qas_answer')
		tabQasANode2.appendChild(withCData(t4_data.tab_qas_answer2))
		tabQasNode2.appendChild(tabQasANode2)

		# -- add tab_qas_url 2
		tabQasUrlNode2 = dom.createElement('tab_qas_url')
		tabQasUrlNode2.appendChild(withCData(t4_data.tab_qas_url2))
		tabQasNode2.appendChild(tabQasUrlNode2)

		# -- add tab_qas_pc_url 2
		tabQasPcUrlNode2 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode2.appendChild(withCData(t4_data.tab_qas_url2))
		tabQasNode2.appendChild(tabQasPcUrlNode2)

		tabLNode.appendChild(tabQasNode2)
		displayNode.appendChild(tabLNode)

		# add tab_list 2
		tabLNode2 = dom.createElement('tab_list')
		# add tab name
		tabNameNode2 = dom.createElement('tab_name')
		tabNameNode2.appendChild(withCData(u'风险'))
		tabLNode2.appendChild(tabNameNode2)
		# add tab url
		tabUrlNode2 = dom.createElement('tab_url')
		tabUrlNode2.appendChild(withCData(t2_data.tab_url2))
		tabLNode2.appendChild(tabUrlNode2)
		# add tab pc url
		tabPcUrlNode2 = dom.createElement('tab_pc_url')
		tabPcUrlNode2.appendChild(withCData(t2_data.tab_url2))
		tabLNode2.appendChild(tabPcUrlNode2)
		# add tab summary
		tabSummNode2 = dom.createElement('tab_summary')
		tabSummNode2.appendChild(withCData(t2_data.tab_summary2))
		tabLNode2.appendChild(tabSummNode2)
		# add tab tips
		tabTipsNode4 = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName4 = dom.createElement('tab_tips_name')
		tabTipsTabName4.appendChild(withCData(u''))
		tabTipsNode4.appendChild(tabTipsTabName4)
		# -- add tap_tip_value
		tabTipsTipValue4 = dom.createElement('tap_tip_value')
		tabTipsTipValue4.appendChild(withCData(''))
		tabTipsNode4.appendChild(tabTipsTipValue4)
		tabLNode2.appendChild(tabTipsNode4)
		# add tab_qas 3
		tabQasNode3 = dom.createElement('tab_qas')
		# -- add tab_qas_question 3
		tabQasQNode3 = dom.createElement('tab_qas_question')
		tabQasQNode3.appendChild(withCData(u'难度'))
		tabQasNode3.appendChild(tabQasQNode3)
		# -- add tab_qas_answer 3
		tabQasANode3 = dom.createElement('tab_qas_answer')
		tabQasANode3.appendChild(withCData(t4_data.tab_qas_answer3))
		tabQasNode3.appendChild(tabQasANode3)
		# -- add tab_qas_url 3
		tabQasUrlNode3 = dom.createElement('tab_qas_url')
		tabQasUrlNode3.appendChild(withCData(t4_data.tab_qas_url3))
		tabQasNode3.appendChild(tabQasUrlNode3)

		# -- add tab_qas_pc_url 3
		tabQasPcUrlNode3 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode3.appendChild(withCData(t4_data.tab_qas_url3))
		tabQasNode3.appendChild(tabQasPcUrlNode3)

		tabLNode2.appendChild(tabQasNode3)

		displayNode.appendChild(tabLNode2)

		# add tab_list
		tabLNode3 = dom.createElement('tab_list')
		# add tab name
		tabNameNode3 = dom.createElement('tab_name')
		tabNameNode3.appendChild(withCData(u'准备'))
		tabLNode3.appendChild(tabNameNode3)
		# add tab url
		tabUrlNode3 = dom.createElement('tab_url')
		tabUrlNode3.appendChild(withCData(t2_data.tab_url3))
		tabLNode3.appendChild(tabUrlNode3)
		# add tab pc url
		tabPcUrlNode3 = dom.createElement('tab_pc_url')
		tabPcUrlNode3.appendChild(withCData(t2_data.tab_url3))
		tabLNode3.appendChild(tabPcUrlNode3)
		# add tab summary
		tabSummNode3 = dom.createElement('tab_summary')
		tabSummNode3.appendChild(withCData(t2_data.tab_summary3))
		tabLNode3.appendChild(tabSummNode3)
		# add tab tips
		tabTipsNode5 = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName5 = dom.createElement('tab_tips_name')
		tabTipsTabName5.appendChild(withCData(u''))
		tabTipsNode5.appendChild(tabTipsTabName5)
		# -- add tap_tip_value
		tabTipsTipValue5 = dom.createElement('tap_tip_value')
		tabTipsTipValue5.appendChild(withCData(''))
		tabTipsNode5.appendChild(tabTipsTipValue5)
		tabLNode3.appendChild(tabTipsNode5)
		# add tab_qas
		tabQasNode4 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode4 = dom.createElement('tab_qas_question')
		tabQasQNode4.appendChild(withCData(u'需要哪些检查'))
		tabQasNode4.appendChild(tabQasQNode4)
		# -- add tab_qas_answer
		tabQasANode4 = dom.createElement('tab_qas_answer')
		tabQasANode4.appendChild(withCData(t4_data.tab_qas_answer4))
		tabQasNode4.appendChild(tabQasANode4)
		# --- add tab_qas_url
		tabQasUrlNode4 = dom.createElement('tab_qas_url')
		tabQasUrlNode4.appendChild(withCData(t4_data.tab_qas_url4))
		tabQasNode4.appendChild(tabQasUrlNode4)
		# --- add tab_qas_pc_url
		tabQasPcUrlNode4 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode4.appendChild(withCData(t4_data.tab_qas_url4))
		tabQasNode4.appendChild(tabQasPcUrlNode4)

		tabLNode3.appendChild(tabQasNode4)

		# add tab_qas
		tabQasNode5 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode5 = dom.createElement('tab_qas_question')
		tabQasQNode5.appendChild(withCData(u'需要配合医务人员'))
		tabQasNode5.appendChild(tabQasQNode5)
		# -- add tab_qas_answer
		tabQasANode5 = dom.createElement('tab_qas_answer')
		tabQasANode5.appendChild(withCData(t4_data.tab_qas_answer5))
		tabQasNode5.appendChild(tabQasANode5)
		# --- add tab_qas_url
		tabQasUrlNode5 = dom.createElement('tab_qas_url')
		tabQasUrlNode5.appendChild(withCData(t4_data.tab_qas_url5))
		tabQasNode5.appendChild(tabQasUrlNode5)
		# --- add tab_qas_pc_url
		tabQasPcUrlNode5 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode5.appendChild(withCData(t4_data.tab_qas_url5))
		tabQasNode5.appendChild(tabQasPcUrlNode5)

		tabLNode3.appendChild(tabQasNode5)

		displayNode.appendChild(tabLNode3)

		# add tab list
		tabLNode4 = dom.createElement("tab_list")
		# add tab name
		tabNameNode4 = dom.createElement('tab_name')
		tabNameNode4.appendChild(withCData(u'过程'))
		tabLNode4.appendChild(tabNameNode4)
		# add tab url
		tabUrlNode4 = dom.createElement('tab_url')
		tabUrlNode4.appendChild(withCData(t2_data.tab_url4))
		tabLNode4.appendChild(tabUrlNode4)
		# add tab pc url
		tabPcUrlNode4 = dom.createElement('tab_pc_url')
		tabPcUrlNode4.appendChild(withCData(t2_data.tab_url4))
		tabLNode4.appendChild(tabPcUrlNode4)
		# add tab summary
		tabSummNode4 = dom.createElement('tab_summary')
		tabSummNode4.appendChild(withCData(t2_data.tab_summary4))
		tabLNode4.appendChild(tabSummNode4)
		# add tab tips
		tabTipsNode6 = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName6 = dom.createElement('tab_tips_name')
		tabTipsTabName6.appendChild(withCData(u''))
		tabTipsNode6.appendChild(tabTipsTabName6)
		# -- add tap_tip_value
		tabTipsTipValue6 = dom.createElement('tap_tip_value')
		tabTipsTipValue6.appendChild(withCData(''))
		tabTipsNode6.appendChild(tabTipsTipValue6)
		tabLNode4.appendChild(tabTipsNode6)

		# add tab_qas
		tabQasNode6 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode6 = dom.createElement('tab_qas_question')
		tabQasQNode6.appendChild(withCData(u''))
		tabQasNode6.appendChild(tabQasQNode6)
		# -- add tab_qas_answer
		tabQasANode6 = dom.createElement('tab_qas_answer')
		tabQasANode6.appendChild(withCData(''))
		tabQasNode6.appendChild(tabQasANode6)
		# --- add tab_qas_url
		tabQasUrlNode6 = dom.createElement('tab_qas_url')
		tabQasUrlNode6.appendChild(withCData(''))
		tabQasNode6.appendChild(tabQasUrlNode6)
		# --- add tab_qas_pc_url
		tabQasPcUrlNode6 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode6.appendChild(withCData(''))
		tabQasNode6.appendChild(tabQasPcUrlNode6)
		tabLNode4.appendChild(tabQasNode6)

		# add tab_pics
		tabPicNode = dom.createElement('tab_pic')
		tabPicTitleNode = dom.createElement('tab_pic_title')
		if t5_data.tab_pic_url.strip() != "":
			tabPicTitleNode.appendChild(withCData(u'配图'))
		else:
			tabPicTitleNode.appendChild(withCData(u''))
		tabPicNode.appendChild(tabPicTitleNode)
		tabPicUrlNode = dom.createElement('tab_pic_url')
		tabPicUrlNode.appendChild(withCData(t5_data.tab_pic_url))
		tabPicNode.appendChild(tabPicUrlNode)
		tabPicPcUrlNode = dom.createElement('tab_pic_pc_url')
		tabPicPcUrlNode.appendChild(withCData(t5_data.tab_pic_url))
		tabPicNode.appendChild(tabPicPcUrlNode)
		tabLNode4.appendChild(tabPicNode)

		displayNode.appendChild(tabLNode4)


		# add tab_list
		tabLNode5 = dom.createElement("tab_list")
		# add tab name
		tabNameNode5 = dom.createElement('tab_name')
		tabNameNode5.appendChild(withCData(u'护理'))
		tabLNode5.appendChild(tabNameNode5)
		# add tab url
		tabUrlNode5 = dom.createElement('tab_url')
		tabUrlNode5.appendChild(withCData(t2_data.tab_url5))
		tabLNode5.appendChild(tabUrlNode5)
		# add tab pc url
		tabPcUrlNode5 = dom.createElement('tab_pc_url')
		tabPcUrlNode5.appendChild(withCData(t2_data.tab_url5))
		tabLNode5.appendChild(tabPcUrlNode5)
		# add tab summary
		tabSummNode5 = dom.createElement('tab_summary')
		tabSummNode5.appendChild(withCData(t2_data.tab_summary5))
		tabLNode5.appendChild(tabSummNode5)
		# add tab tips
		tabTipsNode7 = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName7 = dom.createElement('tab_tips_name')
		tabTipsTabName7.appendChild(withCData(u''))
		tabTipsNode7.appendChild(tabTipsTabName7)
		# -- add tap_tip_value
		tabTipsTipValue7 = dom.createElement('tap_tip_value')
		tabTipsTipValue7.appendChild(withCData(''))
		tabTipsNode7.appendChild(tabTipsTipValue7)
		tabLNode5.appendChild(tabTipsNode7)

		# add tab_qas
		tabQasNode7 = dom.createElement('tab_qas')
		# -- add tab_qas_question`
		tabQasQNode7 = dom.createElement('tab_qas_question')
		tabQasQNode7.appendChild(withCData(u'康复过程'))
		tabQasNode7.appendChild(tabQasQNode7)
		# -- add tab_qas_answer
		tabQasANode7 = dom.createElement('tab_qas_answer')
		tabQasANode7.appendChild(withCData(t4_data.tab_qas_answer6))
		tabQasNode7.appendChild(tabQasANode7)
		# --- add tab_qas_url
		tabQasUrlNode7 = dom.createElement('tab_qas_url')
		tabQasUrlNode7.appendChild(withCData(t4_data.tab_qas_url6))
		tabQasNode7.appendChild(tabQasUrlNode7)
		# --- add tab_qas_pc_url
		tabQasPcUrlNode7 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode7.appendChild(withCData(t4_data.tab_qas_url6))
		tabQasNode7.appendChild(tabQasPcUrlNode7)
		tabLNode5.appendChild(tabQasNode7)

		# add tab_qas
		tabQasNode8 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode8 = dom.createElement('tab_qas_question')
		tabQasQNode8.appendChild(withCData(u'如何复查'))
		tabQasNode8.appendChild(tabQasQNode8)
		# -- add tab_qas_answer
		tabQasANode8 = dom.createElement('tab_qas_answer')
		tabQasANode8.appendChild(withCData(t4_data.tab_qas_answer7))
		tabQasNode8.appendChild(tabQasANode8)
		# --- add tab_qas_url
		tabQasUrlNode8 = dom.createElement('tab_qas_url')
		tabQasUrlNode8.appendChild(withCData(t4_data.tab_qas_url7))
		tabQasNode8.appendChild(tabQasUrlNode8)
		# --- add tab_qas_pc_url
		tabQasPcUrlNode8 = dom.createElement('tab_qas_pc_url')
		tabQasPcUrlNode8.appendChild(withCData(t4_data.tab_qas_url7))
		tabQasNode8.appendChild(tabQasPcUrlNode8)
		tabLNode5.appendChild(tabQasNode8)		

		displayNode.appendChild(tabLNode5)

		# add expert
		expertNode = dom.createElement('expert')
		expertName = dom.createElement('expert_name')
		expertName.appendChild(withCData(t1_data.expert_name))
		expertNode.appendChild(expertName)
		expertPic = dom.createElement('expert_pic')
		expertPic.appendChild(withCData(t1_data.expert_pic))
		expertNode.appendChild(expertPic)
		expertTitle = dom.createElement('expert_title')
		expertTitle.appendChild(withCData(t1_data.expert_title))
		expertNode.appendChild(expertTitle)
		expertHospital = dom.createElement('expert_hospital')
		expertHospital.appendChild(withCData(t1_data.expert_hospital))
		expertNode.appendChild(expertHospital)
		expertHospitalLevel = dom.createElement('expert_hospital_level')
		expertHospitalLevel.appendChild(withCData(t1_data.expert_hospital_level))
		expertNode.appendChild(expertHospitalLevel)
		expertDepartment = dom.createElement('expert_department')
		expertDepartment.appendChild(withCData(t1_data.expert_department))
		expertNode.appendChild(expertDepartment)
		expertUrl = dom.createElement('expert_url')
		expertUrl.appendChild(withCData(t1_data.expert_url))
		expertNode.appendChild(expertUrl)
		expertPcUrl = dom.createElement('expert_pc_url')
		expertPcUrl.appendChild(withCData(t1_data.expert_pc_url))
		expertNode.appendChild(expertPcUrl)
		displayNode.appendChild(expertNode)
		
		# authority
		authority = dom.createElement('authority')
		authority.appendChild(withCData(t1_data.authority))
		displayNode.appendChild(authority)

		authority_url = dom.createElement('authority_url')
		authority_url.appendChild(withCData(t1_data.authority_url))
		displayNode.appendChild(authority_url)

		authority_pc_url = dom.createElement('authority_pc_url')
		authority_pc_url.appendChild(withCData(t1_data.authority_url))
		displayNode.appendChild(authority_pc_url)

		tab1Node = dom.createElement('tab1')
		tab1Node.appendChild(withCData(u'概述'))
		displayNode.appendChild(tab1Node)

		tab2Node = dom.createElement('tab2')
		tab2Node.appendChild(withCData(u'风险'))
		displayNode.appendChild(tab2Node)

		tab3Node = dom.createElement('tab3')
		tab3Node.appendChild(withCData(u'准备'))
		displayNode.appendChild(tab3Node)

		tab4Node = dom.createElement('tab4')
		tab4Node.appendChild(withCData(u'过程'))
		displayNode.appendChild(tab4Node)

		tab4Node = dom.createElement('tab5')
		tab4Node.appendChild(withCData(u'护理'))
		displayNode.appendChild(tab4Node)

		item.appendChild(displayNode)
		root.appendChild(item)
	with open('./shouhu.xml', 'w') as fh:
		fh.write(dom.toprettyxml(indent = "  ", newl = "\n", encoding = "utf8"))  

def parse_xlsx(filepath):
	xlsx = xlrd.open_workbook(filepath)
	tab1 = xlsx.sheet_by_index(2)
	tab2 = xlsx.sheet_by_index(3)
	tab3 = xlsx.sheet_by_index(4)
	tab4 = xlsx.sheet_by_index(5)
	tab5 = xlsx.sheet_by_index(6)
	tab1Datas = parseConfig1(tab1)
	tab2Datas = parseConfig2(tab2)
	tab3Datas = parseConfig3(tab3)
	tab4Datas = parseConfig4(tab4)
	tab5Datas = parseConfig5(tab5)
	outputXml(tab1Datas, tab2Datas, tab3Datas, tab4Datas, tab5Datas)

def main():
	parse_xlsx("./data/shoushu-v4-0608.xlsx")

if __name__ == '__main__':
    main()
