#!/usr/bin/env python3

import string	
import requests
import json
import urllib3
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
debug_flag = logging.INFO # To get better information change to DEBUG
logging_file = 'fmg_script.log'
logging.basicConfig(level=debug_flag,format='%(asctime)s:%(levelname)s:%(message)s')
# If you want to log to file comment out above and uncomment below.
#logging.basicConfig(filename=logging_file,level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

""""
	This script will create a model device on FMG with the ZTP reset flag on then applies a pre-cli-template.  
	This requires 7.0.5 FMG or greater. It also requires to land on FortiOS 7.0.6 and later because it uses
	a new factory reset that saves the central management settings on reset.
	Created the week of 12DEC22 by Andy Faulkner a.k.a The Evil Bastard.
"""

fmg_ip = "<YOUR FMG IP"
fmg_passwd = "<YOUR FMG USER PASSWORD"
fmg_user = "api-user"
url_base="https://" + fmg_ip + "/jsonrpc" 
fgt_device = "FGT60E-A"
module_sn = "FGT60ETK18002189"
adom_name = "LAB_7_0"
template_name = "admin_stuff"
client = ""
sid = ""

def fmg_login():
	global sid,client
	client = requests.session()
	logging.info("Logging into FMG and getting session ID.")
	#Login request
	payload = {
		"id": 1,
		"method": "exec",
		"params": [
			{
				"data": {
					"passwd": fmg_passwd,
					"user": fmg_user
				},
				"url": "/sys/login/user"
			}
		]
	}
	r = client.post(url_base, json=payload, verify=False )
	#Retrieve session id. Add to HTTP header for future messages parsed_json = json.loads(r.text)
	parsed_json = json.loads(r.text)
	logging.debug(r.text)
	sid = parsed_json['session']
	logging.debug("Session ID from FMG: " + sid)

def create_model():
	global sid, client
	logging.info("Creating model device " + fgt_device + " in ADOM " + adom_name)
	
	data = {
		"method": "set",
		"params": [
			{
				"data": [
					{
						"adm_pass": [
							""
						],
						"adm_usr": "admin",
						"branch_pt": 410,
						"build": 410,
						"checksum": "",
						"conf_status": 0,
						"conn_mode": 1,
						"conn_status": 0,
						"db_status": "unknown",
						"desc": "Created from API",
						"dev_status": 1,
#						"flags": [
#							"is_model", "linked_to_model", "need_reset"
#						],
						"flags" : 34427109408,
						"fsw_cnt": 0,
						"ha_group_id": 0,
						"ha_group_name": "",
						"ha_mode": "standalone",
						"hostname": "FGT60ETK18002189",
						"hw_rev_major": 0,
						"hw_rev_minor": 0,
						"ip": "",
						"latitude": "27.9269",
						"longitude": "-82.7483",
						"maxvdom": 10,
						"meta fields": {
							"Voice_VLAN": "20",
							"Address": "1906 Sandpiper Drive, Clearwater, FL 33764",
							"Company/Organization": "EvilBast Corp",
							"Contact Email": "evil@evilbast.com",
							"Contact Phone Number": "614-578-4722"
						
						},
						"mgmt_id": 0,
						"mgmt_if": "",
						"mgmt_mode": "unreg",
						"mgt_vdom": "",
						"module_sn": module_sn,
						"mr": 0,
						"name": fgt_device,
						"nsxt_service_name": "",
						"os_type": "",
						"os_ver": "",
						"patch": 0,
						"platform_str": "FortiGate-60E",
						"prefer_img_ver": "7.0.9-b444",
						"prio": 128,
						"private_key": "",
						"private_key_status": 0,
						"psk": "",
						"role": "",
						"sn": "FGT60ETK18002189",
						"version": 700,
					}
				],
				"url": "/dvmdb/adom/" + adom_name + "/device"
			}
		],
		"session": sid,
		"id": 1
	}
	headers = {'session' : sid }
	
	r = client.post(url_base, headers=headers, json=data, verify=False)
	parsed_json = json.loads(r.text)
	logging.debug(json.dumps(parsed_json, indent=4, sort_keys=True))

	if parsed_json['result'][0]['status']['message'] == "OK":
		logging.info("Device created.")
	else:
		logging.info("Something went wrong, turn on Debug flag and check.")
		# I know this is crappy debug

def template_set():
	global sid,client
	headers = {'session' : sid }
	logging.info("Setting template " + template_name + " on device " + fgt_device)
	
	data = {
		"method": "add",
		"params": [
			{

				"url":"/pm/config/adom/" + adom_name + "/obj/cli/template/" + template_name + "/scope member",
					"data":
					[{"name":fgt_device,"vdom":"root"}]
				
			}
		],
		"session": sid,
		"id": 1,
		"loadsub" : 0
	}
	
	headers = {'session' : sid }
	
	r = client.post(url_base, headers=headers, json=data, verify=False)
	parsed_json = json.loads(r.text)
	logging.debug(json.dumps(parsed_json, indent=4, sort_keys=True))
	if parsed_json['result'][0]['status']['message'] == "OK":
		logging.info("Template applied.")
	else:
		logging.info("Something went wrong, turn on Debug flag and check.")
		
def fmg_log_out():
	global sid, client
	client = requests.session()
	payload = {
		"id": 1,
		"method": "exec",
		"params": [
			{
				"url": "/sys/logout"
			}
		],
		"session": sid
	}
	
	headers = {'session' : sid }
	
	r = client.post(url_base, headers=headers, json=payload, verify=False)
	parsed_json = json.loads(r.text)
	logging.info("logging out of session...")
	

# Logging into FMG
fmg_login()
# Creating the device Model
create_model()
# Setting the template
template_set()
# Logging out of FMG
fmg_log_out()
