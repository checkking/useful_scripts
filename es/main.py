#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import yaml
import os
from rcm_doc_updator import *

def read_config(env):
	with open('config.{0}.yaml'.format(env)) as fh:
		d = yaml.safe_load(fh)
		return d

def main():
	env = os.environ['ENV']
	info("env:{0}".format(env))
	cfg = read_config(env)
	rcm_doc_updator = RcmDocUpdator(cfg)
	rcm_doc_updator.init()
	update_type = sys.argv[1]
	if update_type == "all":
		succ = rcm_doc_updator.total_update()
		if not succ:
			info("[ERROR] total update failed")
		else:
			info("total update succ.")
	elif update_type == "hour":
		succ = rcm_doc_updator.incremental_update()
		if not succ:
			info("[ERROR] incremental update failed")
		else:
			info("incremental update succ.")
	else:
		info("invalid type:{0}".format(update_type))

if __name__ == '__main__':
	main()
