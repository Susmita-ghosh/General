import requests
import json

'''
Retrieving Attachments from the ticket
Query to sys_attachment table
Input: Customer SN domain, Auth details,Table Name,sys_id
'''

def attach_content(cust_dom,table_name,sys_id,user,pwd):

    url = f'https://{cust_dom}.service-now.com/api/now/attachment?sysparm_query=table_name%3D{table_name}%5Etable_sys_id%3D{sys_id}&sysparm_limit=10'
    
    user = user
    pwd = pwd
    
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    att_data = response.json()['result']
    for attach in att_data:
        attach_sys_id = attach['sys_id']
        print(attach_sys_id)

#Retriving Attacchment Content from the Task
        url = f'https://{cust_dom}.service-now.com/api/now/attachment/{attach_sys_id}/file'

        user = user
        pwd = pwd

        headers = {"Content-Type":"application/json","Accept":"*/*"}

        response = requests.get(url, auth=(user, pwd), headers=headers )

        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()
#Parsing Bytes to dict value:
        obj_str=response.content.decode('utf-8')
        lines = obj_str.strip().split('\r\n')
        header = lines[0].split(',')
        obj = {}
        for line in lines[1:]:
            key,value = line.split(',')
            obj[key] = value
        print(obj)
#---------------------------------------------


'''
I: GET Requests with Basic Auth:
1. Fetch the tasks to get the sys_id, short_decription, Task Number
2. Fetch individual request sys_id
3. Read Associated CSV details and parse to json
'''
def get_info_initial(cust_dom,table_name,user,pwd):
#Fetch the list of Incidents associated to the Table
        url = f'https://{cust_dom}.service-now.com/api/now/table/{table_name}?sysparm_limit=10'

        user = user
        pwd = pwd

        headers = {"Content-Type":"application/json","Accept":"application/json"}

        response = requests.get(url, auth=(user, pwd), headers=headers )

        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error:',response.json())
            exit()

        data = response.json()['result']
        for value in data:
            sys_id = value['sys_id']
            print('Task_Number:',value['task_effective_number'])

#Fetch Attachment Metadata for each incident discovered earlier from table
            print(sys_id)
            attach_content(cust_dom=cust_dom,table_name=table_name,sys_id=sys_id,user=user,pwd=pwd)
#--------------------------------------------------------

'''
II: PATCH Update single record
1. Fetch the incident/ Task sys_id
2. Fixing Fields to be updated: Workorder: with specific notes and changing the state of the incident
'''
def update_ticket(cust_dom,sys_id,table_name,user,pwd,data):
        url = f'https://{cust_dom}.service-now.com/api/now/table/{table_name}/{sys_id}'

        user = user
        pwd = pwd

        headers = {"Content-Type":"application/json","Accept":"application/json"}

        response = requests.patch(url, auth=(user, pwd), headers=headers ,data=data)

        # Check for HTTP codes other than 200
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        value = response.json()
        status = response.status_code
        print(status)
#----------------------------------------------------------
'''
III: Retrieve any specific records
1. Pass in customer domain, table_name,sys_id and the auth details
2. Required to fetch an individual ticket
'''
def get_ticket(cust_dom,table_name,sys_id,user,pwd):
        url = f'https://{cust_dom}.service-now.com/api/now/table/{table_name}/{sys_id}'

        user = user
        pwd = pwd

        headers = {"Content-Type":"application/json","Accept":"application/json"}

        response = requests.get(url, auth=(user, pwd), headers=headers )

        # Check for HTTP codes other than 200
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        result = response.json()['result']
        print('Task Number:',result['task_effective_number'],'\nShort_Description:',result['short_description'])
        attach_content(cust_dom=cust_dom,table_name=table_name,sys_id=sys_id,user=user,pwd=pwd)


# get_info_initial(cust_dom='iamcyberlab',table_name='u_workorder',user='svc_cybiex_auto',pwd='Solution@123')

# update_ticket(cust_dom='iamcyberlab',sys_id='cab783b747f5da10f32d17df016d438a',table_name='u_workorder',user='svc_cybiex_auto',pwd='Solution@123',data='{\"work_notes\":\"Automation Pending\",\"state\":\"-5\"}')

get_ticket(cust_dom='iamcyberlab',table_name='u_workorder',sys_id='cab783b747f5da10f32d17df016d438a',user='svc_cybiex_auto',pwd='Solution@123')