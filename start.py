#encoding=utf-8
import csv,json,sys
from capi import capi

api_key=''
secret_key=''

api=capi(api_key,secret_key)

def get_domain_id(domain):
	domain_list=json.loads(api.domain_list(),encoding='utf-8')['data']
	#print(domain_list)
	for i in domain_list:
		if(i['domain'][:-1]==domain):
			return i['id']
	
	return ''

def get_domain_record(domain_id):
	#print(api.domain_host_record_list(domain_id,0,0,2000))
	record_list=json.loads(api.domain_host_record_list(domain_id,0,0,2000),encoding='utf-8')['data']
	return record_list
	
def transform(record):
	detect_code=detect(record['type'])
	if(detect_code==-1):
		return None
	if(detect_code==3):
		print("请自行转换LINK记录")
		return None
		
	new_record={}
	new_record['host']=record['host']
	new_record['line']='默认'
	new_record['value']=record['value']
	new_record['priority']='-'
	new_record['weight']='-'
	new_record['status']=2 if record['status']=='ok' else 4
	new_record['ttl']=record['ttl']
	new_record['last_update']=record['update_time']
	
	if(detect_code==1):
		new_record['type']=record['type'][:-1] if record['type'][-1]=='X' else record['type']
		new_record['weight']=1 if record['mx']==None else record['mx']
		
	if(detect_code==2):
		new_record['type']=record['type']
		new_record['priority']=1 if record['mx']==None else record['mx']
	
	if(detect_code==0):
		new_record['type']=record['type']
		if(new_record['type']=='DR301X' or new_record['type']=='DR302X'):
			new_record['type']='显性URL'
			new_record['value']=new_record['value'].replace('$uri','')
	
	return new_record
	
def detect(record_type):
	record_type_list=['A','AX','AAAA','CNAME','CNAMEX','MX','LINK','DR301X','DR302X','TXT','NS']
	if(record_type not in record_type_list):
		return -1
	if(record_type in ['A','AX','AAAA','CNAME','CNAMEX']):
		return 1
	if(record_type in ['MX']):
		return 2
	if(record_type in ['LINK']):
		return 3
	return 0
	
if __name__=="__main__":
	if(len(sys.argv)!=2):
		print("参数错误")
		sys.exit(0)
	
	domain=sys.argv[1]
	domain_id=get_domain_id(domain)
	domain_record=get_domain_record(domain_id)
	with open(domain+'.csv', 'w',encoding='utf-8',newline='') as csvfile:
		with open('disable-'+domain+'.csv', 'w',encoding='utf-8',newline='') as disable_csv_file:
			filewriter = csv.writer(csvfile, delimiter=',',
				quotechar='|', quoting=csv.QUOTE_MINIMAL)
			disable_file_writer = csv.writer(disable_csv_file, delimiter=',',
				quotechar='|', quoting=csv.QUOTE_MINIMAL)
			
			filewriter.writerow(['主机记录', '记录类型', '解析线路', '记录值', '优先级',
				'权重', 'TTL', '状态', '最后操作时间'])
			disable_file_writer.writerow(['主机记录', '记录类型', '解析线路', '记录值', '优先级',
				'权重', 'TTL', '状态', '最后操作时间'])
				
			for r in domain_record:
				new_record=transform(r)
				if(new_record==None):
					print("不支持的记录类型:")
					print(r)
					continue
				
				# If the record is disabled before.
				if(new_record['status']==4):
					disable_file_writer.writerow([new_record['host'], new_record['type'], new_record['line'],
					new_record['value'], new_record['priority'], new_record['weight'],
					new_record['ttl'], new_record['status'], new_record['last_update']])
					continue
					
				#print(new_record)
				filewriter.writerow([new_record['host'], new_record['type'], new_record['line'],
					new_record['value'], new_record['priority'], new_record['weight'],
					new_record['ttl'], new_record['status'], new_record['last_update']])
			
