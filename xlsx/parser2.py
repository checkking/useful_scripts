#coding:gbk

# 指标

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
		self.tab_summary1 = ""
		self.tab_url1 = ""
		self.tab_summary2 = ""
		self.tab_url2 = ""
		self.tab_summary3 = ""
		self.tab_url3 = ""

class Config3(object):
	def __init__(self):
		self.key = ""
		self.tap_tip_value1 = ""
		self.tap_tip_value2 = ""

class Config4(object):
	def __init__(self):
		self.key = ""
		self.tab_qas_answer1 = ""
		self.tab_qas_answer2 = ""
		self.tab_qas_answer3 = ""
	
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
		cfg2.tab_summary1 = row[2].value
		cfg2.tab_url1 = row[3].value
		cfg2.tab_summary2 = row[4].value
		cfg2.tab_url2 = row[5].value
		cfg2.tab_summary3 = row[6].value
		cfg2.tab_url3 = row[7].value
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
		cfg3.tap_tip_value1 = row[2].value
		cfg3.tap_tip_value2 = row[3].value
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
		cfg4.tab_qas_answer1 = row[2].value
		cfg4.tab_qas_answer2 = row[3].value
		cfg4.tab_qas_answer3 = row[4].value
		cfgs[cfg4.key] = cfg4
	return cfgs

def withCData(s):
	cd = minidom.CDATASection()
	cd.data = s
	cd.nodeType = cd.TEXT_NODE
	return cd

def outputXml(tab1Datas, tab2Datas, tab3Datas, tab4Datas):
	dom = minidom.getDOMImplementation().createDocument(None,'DOCUMENT',None)
	root = dom.documentElement
	for t1_data in tab1Datas:
		t2_data = None
		t3_data = None
		t4_data = None
		if t1_data.key in tab2Datas:
			t2_data = tab2Datas[t1_data.key]
		else:
			raise RuntimeError('tabs not matched! key: {0} not in tab2'.format(t1_data.key))
		if t1_data.key in tab3Datas:
			t3_data = tab3Datas[t1_data.key]
		if t1_data.key in tab4Datas:
			t4_data = tab4Datas[t1_data.key]
		if t2_data is None or t3_data is None or t4_data is None:
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
		tabTipsTabName = dom.createElement('tab_name')
		tabTipsTabName.appendChild(withCData(u'检测目的'))
		tabTipsNode.appendChild(tabTipsTabName)
		# -- add tap_tip_value
		tabTipsTipValue = dom.createElement('tap_tip_value')
		tabTipsTipValue.appendChild(withCData(t3_data.tap_tip_value1))
		tabTipsNode.appendChild(tabTipsTipValue)
		tabLNode.appendChild(tabTipsNode)
		# add tab tips 2
		tabTipsNode2 = dom.createElement('tab_tips')
		# -- add tab_name 2
		tabTipsTabName2 = dom.createElement('tab_name')
		tabTipsTabName2.appendChild(withCData(u'采集方法'))
		tabTipsNode2.appendChild(tabTipsTabName2)
		# -- add tap_tip_value 2
		tabTipsTipValue2 = dom.createElement('tap_tip_value')
		tabTipsTipValue2.appendChild(withCData(t3_data.tap_tip_value2))
		tabTipsNode2.appendChild(tabTipsTipValue2)
		tabLNode.appendChild(tabTipsNode2)

		# add tab_qas
		tabQasNode = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode = dom.createElement('tab_qas_question')
		tabQasQNode.appendChild(withCData(u'正常值'))
		tabQasNode.appendChild(tabQasQNode)
		tabLNode.appendChild(tabQasNode)

		# -- add tab_qas_answer
		tabQasANode = dom.createElement('tab_qas_answer')
		tabQasANode.appendChild(withCData(t4_data.tab_qas_answer1))
		tabQasNode.appendChild(tabQasANode)
		tabLNode.appendChild(tabQasNode)

		displayNode.appendChild(tabLNode)

		# add tab_list
		tabLNode2 = dom.createElement('tab_list')
		# add tab name
		tabNameNode2 = dom.createElement('tab_name')
		tabNameNode2.appendChild(withCData(u'异常分析'))
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
		tabTipsNode2 = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName2 = dom.createElement('tab_name')
		tabTipsTabName2.appendChild(withCData(u''))
		tabTipsNode2.appendChild(tabTipsTabName2)
		# -- add tap_tip_value
		tabTipsTipValue2 = dom.createElement('tap_tip_value')
		tabTipsTipValue2.appendChild(withCData(''))
		tabTipsNode2.appendChild(tabTipsTipValue2)
		tabLNode2.appendChild(tabTipsNode2)
		# add tab_qas
		tabQasNode2 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode2 = dom.createElement('tab_qas_question')
		tabQasQNode2.appendChild(withCData(u'偏高原因'))
		tabQasNode2.appendChild(tabQasQNode2)
		# -- add tab_qas_answer
		tabQasANode2 = dom.createElement('tab_qas_answer')
		tabQasANode2.appendChild(withCData(t4_data.tab_qas_answer2))
		tabQasNode2.appendChild(tabQasANode2)
		tabLNode2.appendChild(tabQasNode2)
		# add tab_qas
		tabQasNode3 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode3 = dom.createElement('tab_qas_question')
		tabQasQNode3.appendChild(withCData(u'偏低原因'))
		tabQasNode3.appendChild(tabQasQNode3)
		# -- add tab_qas_answer
		tabQasANode3 = dom.createElement('tab_qas_answer')
		tabQasANode3.appendChild(withCData(t4_data.tab_qas_answer3))
		tabQasNode3.appendChild(tabQasANode3)
		tabLNode2.appendChild(tabQasNode3)
		displayNode.appendChild(tabLNode2)


		# add tab_list (注意事项)
		tabLNode3 = dom.createElement('tab_list')
		# add tab name
		tabNameNode3 = dom.createElement('tab_name')
		tabNameNode3.appendChild(withCData(u'注意事项'))
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
		tabTipsNode3 = dom.createElement('tab_tips')
		# -- add tab_name
		tabTipsTabName3 = dom.createElement('tab_name')
		tabTipsTabName3.appendChild(withCData(u''))
		tabTipsNode3.appendChild(tabTipsTabName3)
		# -- add tap_tip_value
		tabTipsTipValue3 = dom.createElement('tap_tip_value')
		tabTipsTipValue3.appendChild(withCData(''))
		tabTipsNode3.appendChild(tabTipsTipValue3)
		tabLNode3.appendChild(tabTipsNode3)
		# add tab_qas
		tabQasNode4 = dom.createElement('tab_qas')
		# -- add tab_qas_question
		tabQasQNode4 = dom.createElement('tab_qas_question')
		tabQasQNode4.appendChild(withCData(''))
		tabQasNode4.appendChild(tabQasQNode4)
		# -- add tab_qas_answer
		tabQasANode4 = dom.createElement('tab_qas_answer')
		tabQasANode4.appendChild(withCData(''))
		tabQasNode4.appendChild(tabQasANode4)
		tabLNode3.appendChild(tabQasNode4)
		displayNode.appendChild(tabLNode3)

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
		tab2Node.appendChild(withCData(u'异常分析'))
		displayNode.appendChild(tab2Node)

		tab3Node = dom.createElement('tab3')
		tab3Node.appendChild(withCData(u'注意事项'))
		displayNode.appendChild(tab3Node)

		item.appendChild(displayNode)
		root.appendChild(item)
	with open('./zhibiao.xml', 'w') as fh:
		fh.write(dom.toprettyxml(indent = "  ", newl = "\n", encoding = "utf-8"))  

def parse_xlsx(filepath):
	xlsx = xlrd.open_workbook(filepath)
	tab1 = xlsx.sheet_by_index(2)
	tab2 = xlsx.sheet_by_index(3)
	tab3 = xlsx.sheet_by_index(4)
	tab4 = xlsx.sheet_by_index(5)
	tab1Datas = parseConfig1(tab1)
	tab2Datas = parseConfig2(tab2)
	tab3Datas = parseConfig3(tab3)
	tab4Datas = parseConfig4(tab4)
	outputXml(tab1Datas, tab2Datas, tab3Datas, tab4Datas)

def main():
	parse_xlsx("./data/20200716/zhibiao-v4-0611_2.xlsx")

if __name__ == '__main__':
    main()
