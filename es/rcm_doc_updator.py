#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
import time
import requests
import datetime
import json
import sys

def info(msg):
	now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
	print("[{0}]{1}".format(now_time, msg))

class ArticleInfo(object):
	def __init__(self):
		self.docid = ""
		self.ctype = 0
		self.source = 0
		self.createtime = ""
		self.video_duration = 0
		self.health_tags = []
		self.is_handpick = False
		self.author_id = []
		self.author_hp_id = []
		self.category_one = []
		self.category_two = []
		self.category_three = []
		self.disease = []
		self.symptom = []
		self.examine = []
		self.treatment = []
		self.medication = []
		self.ydtag = []
		self.keywords = []
		self.review_id = []
		self.review_hp_id = []
		self.mask_channel = []
		self.status = 1
		self.doc_score = 0.0
		self.has_thumb = False
		self.num_word = 0

class ESHelper(object):
	def __init__(self, es_addr, es_user, es_passwd):
		self.es_addr = es_addr
		self.es_user = es_user
		self.es_passwd = es_passwd
		self.headers = {'Content-Type': 'application/json'}
	
	def createIndex(self, index_name):
		payload = {
			"settings": {
				"number_of_shards": 1
			},
			"mappings": {
				"article_info": {
					"properties": {
						"docid": {
							"type": "keyword"
						},
						"ctype": {
							"type": "integer"
						},
						"source": {
							"type": "integer"
						},
						"createtime": {
							"type": "date",
							"format": "yyyy-MM-dd HH:mm:ss"
						},
						"video_duration": {
							"type": "integer"
						},
						"health_tags": {
							"type": "keyword"
						},
						"is_handpick": {
							"type": "boolean"
						},
						"author_id": {
							"type": "keyword"
						},
						"author_hp_id": {
							"type": "keyword"
						},
						"category_one": {
							"type": "keyword"
						},
						"category_two": {
							"type": "keyword"
						},
						"category_three": {
							"type": "keyword"
						},
						"disease": {
							"type": "keyword"
						},
						"symptom": {
							"type": "keyword"
						},
						"examine": {
							"type": "keyword"
						},
						"treatment": {
							"type": "keyword"
						},
						"medication": {
							"type": "keyword"
						},
						"ydtag": {
							"type": "keyword"
						},
						"keywords": {
							"type": "keyword"
						},
						"review_id": {
							"type": "keyword"
						},
						"review_hp_id": {
							"type": "keyword"
						},
						"mask_channel": {
							"type": "keyword"
						},
						"doc_score": {
							"type": "float"
						},
						"has_thumb": {
							"type": "boolean"
						},
						"num_word": {
							"type": "integer"
						}
					}
				}
			}
		}
		r = requests.put("http://{0}/{1}".format(self.es_addr, index_name),
				headers=self.headers,
				json=payload,
				auth=(self.es_user, self.es_passwd))
		if r.status_code != 200 and r.status_code != 201:
			info("create mapping failed:{0}".format(r.content))
			return False
		info("create index:{0} succ".format(index_name))
		return True

	def changeAliases(self, oldIndex, newIndex, alias):
		get_r = requests.get("http://{0}/{1}/_alias".format(self.es_addr, oldIndex),
				headers=self.headers,
				auth=(self.es_user, self.es_passwd))
		payload = None
		if get_r.status_code != 200 and get_r.status_code != 201:
			info("index {0} not exist!".format(oldIndex))
			payload = {
				"actions": [
					{"add": {"index": newIndex, "alias": alias}}
				]
			}
		else:
			payload = {
				"actions": [
					{"remove": {"index": oldIndex, "alias": alias}},
					{"add": {"index": newIndex, "alias": alias}}
				]
			}
		info("changeAliases payload={0}".format(payload))
		r = requests.post("http://{0}/_aliases".format(self.es_addr),
				headers=self.headers,
				json=payload,
				auth=(self.es_user, self.es_passwd))
		if r.status_code != 200 and r.status_code != 201:
			info("[ERROR] changeAliases failed, {0}".format(r.content))
			return False
		r = requests.delete("http://{0}/{1}".format(self.es_addr, oldIndex), auth=(self.es_user, self.es_passwd))
		info("delete old index:{0}, return:{1}".format(oldIndex, r.content))
		return True

	def insertOrUpdate(self, article, index_name):
		payload = {
			"docid": article.docid,
			"ctype": article.ctype,
			"source": article.source,
			"createtime": article.createtime,
			"video_duration": article.video_duration,
			"health_tags": article.health_tags,
			"is_handpick": article.is_handpick,
			"author_id": article.author_id,
			"author_hp_id": article.author_hp_id,
			"category_one": article.category_one,
			"category_two": article.category_two,
			"category_three": article.category_three,
			"disease": article.disease,
			"symptom": article.symptom,
			"examine": article.examine,
			"medication": article.medication,
			"ydtag": article.ydtag,
			"keywords": article.keywords,
			"review_id": article.review_id,
			"review_hp_id": article.review_hp_id,
			"mask_channel": article.mask_channel,
			"doc_score": article.doc_score,
			"has_thumb": article.has_thumb,
			"num_word": article.num_word
		}
		try:
			r = requests.put("http://{0}/{1}/article_info/{2}".format(self.es_addr, index_name, payload["docid"]), auth=(self.es_user, self.es_passwd),
					headers=self.headers,
					json=payload)
			if r.status_code != 200 and r.status_code != 201:
				info("add doc failed:{0}".format(r.content))
				return False
			else:
				info("add doc succ, docid:{0}".format(payload['docid']))
				return True
		except Exception:
			info("exception and sleep")
			time.sleep(2)
			return False

def _row2ArticleInfo(row):
	json_str = row[0]
	d = json.loads(json_str)
	article = ArticleInfo()
	article.docid = d['docid']
	article.ctype = int(d['ctype'])
	article.source = int(d['source'])
	article.createtime = d['createtime']
	article.video_duration = int(d['video_duration'])
	article.health_tags = d['health_tags']
	article.author_id = d['author_id']
	article.author_hp_id = d['author_hp_id']
	article.category_one = d['category_one']
	article.category_two = d['category_two']
	article.category_three = d['category_three']
	article.disease = d['disease']
	article.symptom = d['symptom']
	article.examine = d['examine']
	article.treatment = d['treatment']
	article.medication = d['medication']
	article.ydtag = d['ydtag']
	article.keywords = []
	kwds = d['keyword']
	for kw in kwds:
		article.keywords.append(kw[0])
	article.review_id = d['review_id']
	article.review_hp_id = d['review_hp_id']
	mc = row[2].split(';')
	article.mask_channel = mc
	article.status = int(row[1])
	article.is_handpick = True if len(row[2]) > 0 and int(row[2]) == 1 else False
	body_ner = d['body_ner']
	body_kwd = d['body_kwd']
	for ner in body_ner:
		if int(ner['freq']) < 2:
			continue
		if ner['type'] is 'symptom':
			article.symptom.append(ner['word'])
		elif ner['type'] is 'treatment':
			article.treatment.append(ner['treatment'])
		elif ner['type'] is 'examine':
			article.examine.append(ner['examine'])
		elif ner['type'] is 'disease':
			article.disease.append(ner['disease'])
	for kwd in body_kwd:
		if float(kwd[1]) < 0.1:
			continue
			article.keywords.append(kwd[0])
	article.has_thumb = bool(d['has_thumb'])
	article.num_word = int(d['num_word'])
	return article

class RcmDocUpdator(object):
	def __init__(self, config):
		self.config = config
		self.db_conn = None
		self.score_db_conn = None
		self.es_helper = None
	
	def __del__(self):
		if self.db_conn is not None:
			self.db_conn.close()

	def init(self):
		db_host = self.config['db_host']
		db_user = self.config['db_user']
		db_passwd = self.config['db_passwd']
		db_name = self.config['db_name']
		es_addr = self.config['es_addr']
		es_user = self.config['es_user']
		es_passwd = self.config['es_passwd']
		self.db_conn = pymysql.connect(host=db_host,user=db_user,password=db_passwd,db=db_name,charset='utf8')
		self.es_helper = ESHelper(es_addr, es_user, es_passwd)

	def _query_score(self, docid):
		db_host = self.config['db_host']
		db_user = self.config['db_user']
		db_passwd = self.config['db_passwd']
		db_name = self.config['db_name']
		sql = "select score from article_recall_score where docid='{0}'".format(docid)
		if self.score_db_conn is None or not self.score_db_conn.open:
			self.score_db_conn = pymysql.connect(host=db_host,user=db_user,password=db_passwd,db=db_name,charset='utf8')
		with self.score_db_conn.cursor() as cur:
			cur.execute(sql)
			row = cur.fetchone()
			if row is not None and len(row) > 0:
				return float(row[0])
			return 0.0


	def _add_score(self, articleInfo):
		score = self._query_score(articleInfo.docid)
		articleInfo.doc_score = score
		return articleInfo

	def _fetch_and_update(self, sql, min_cnt, max_err_rate, index_name):
		info(sql)
		if self.db_conn is None or not self.db_conn.open:
			db_host = self.config['db_host']
			db_user = self.config['db_user']
			db_passwd = self.config['db_passwd']
			db_name = self.config['db_name']
			self.db_conn = pymysql.connect(host=db_host,user=db_user,password=db_passwd,db=db_name,charset='utf8')
		cnt = 0
		err_cnt = 0
		with self.db_conn.cursor(pymysql.cursors.SSDictCursor) as cur:
			cur.execute(sql)
			for row in cur:
				r = []
				r.append(row['json_str'])
				r.append(row['status'])
				r.append(row['mask_channel'])
				articleInfo = None
				try:
					articleInfo = _row2ArticleInfo(r)
					articleInfo = self._add_score(articleInfo)
				except Exception as e:
					print(e)
					articleInfo = None
					info("|ERROR:_row2ArticleInfo failed")
				cnt = cnt + 1
				if articleInfo is not None:
					if not self.es_helper.insertOrUpdate(articleInfo, index_name):
						info("[ERROR] insert or update failed, docid:{0}".format(articleInfo.docid))
						err_cnt = err_cnt + 1
					time.sleep(0.01)
		self.db_conn.commit()
		if cnt <= min_cnt or float(err_cnt)/(cnt + 1) > max_err_rate:
			info("end totalUpdate docs failed, cnt:{0}. err_rate:{1}".format(cnt, float(err_cnt)/cnt))
			return False
		info("end totalUpdate docs succ, cnt:{0}, err_rate:{1}".format(cnt, float(err_cnt) / (cnt + 1)))
		return True

	def total_update(self):
		info("start totalUpdate docs...")
		t = datetime.datetime.now()
		today = t.strftime("%Y%m%d")
		yesday = (t + datetime.timedelta(days=-1)).strftime("%Y%m%d")
		alias = "rcm_recall_article_index"
		yes_index = "{0}_{1}".format(alias, yesday)
		today_index = "{0}_{1}".format(alias, today)
		succ = self.es_helper.createIndex(today_index)
		if not succ:
			return
		sql = "select json_str, status, mask_channel from article_features order by docid asc"
		succ = self._fetch_and_update(sql, 100000, 0.01, today_index)
		if not succ:
			return False
		succ = self.es_helper.changeAliases(yes_index, today_index, alias)
		return succ

	def incremental_update(self):
		info("start update docs...")
		# 1 hour ago
		t = datetime.datetime.now()
		t = (t - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
		sql = "select json_str, status, mask_channel,is_handpick from article_features where updatetime>='" + t + "'"
		succ = self._fetch_and_update(sql, -1, 2, "rcm_recall_article_index")
		if not succ:
			return False
		return True

