import json
import datetime
import os
import platform
import requests
from flask import Flask, jsonify

app = Flask(__name__)

snow_inst = 'dev94486.service-now.com'
snow_inst_table = 'incident'
snow_inst_endpoint_url = 'https://' + snow_inst + '/api/now/table/' + snow_inst_table
snow_inst_get_url = snow_inst_endpoint_url + \
                    '?json&sysparm_query=state=1^short_descriptionLIKEAnsible&sysparm_display_value=true'
snow_username = 'admin'
snow_password = 'Adminadmin1'
headers = {"Accept": "application/json"}
print("SNOW URL endpoint=", snow_inst_endpoint_url)
ansible_automation_engine_url = " "
payload_snow = "test"


def snow_get_req():
    response = requests.get(snow_inst_get_url, auth=(snow_username, snow_password), headers=headers)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
        exit()
    else:
        print("Response code: ", response.status_code)
        json_response = json.loads(response.content)
        print("JSON response=\n", json_response)
    return json_response


def parse_response():
    global payload_snow
    j_response = snow_get_req()
    inc_number = []
    inc_sys_id = []
    cmdb_ci_arr = []
    cmdb_ci_value = []
    assignment_group_arr = []
    assignment_group = []
    description = []
    payload = []
    length = len(j_response["result"])
    print("Number of incidents:", length)

    for i in range(0, length):
        inc_number.append(j_response["result"][i]["number"])
        inc_sys_id.append(j_response["result"][i]["sys_id"])
        cmdb_ci_arr.append(j_response["result"][i]["cmdb_ci"])
        cmdb_ci_value.append(cmdb_ci_arr[i]["display_value"])
        assignment_group_arr.append(j_response["result"][i]["assignment_group"])
        assignment_group.append(assignment_group_arr[i]["display_value"])
        description.append(j_response["result"][i]["description"])

        print("Incident number:", inc_number[i])
        print("Incident sys id:", inc_sys_id[i])
        print("cmdb_ci:", cmdb_ci_value[i])
        print("Assignment group:", assignment_group[i])
        print("Ticket Description:", description[i])

        desc = str(description[i])
        index1 = desc.find("Service Name:")
        Service_Name = desc[index1+13:]
        Service_Name = Service_Name.strip()
        print("Service Name:", Service_Name)

        payload_snow = '{"extra_vars":{' + '"Service_Name":' + '"' + Service_Name + '", ' + '"Server_name":' + '"' + cmdb_ci_value[i] + '", ' \
                       + '"Ticket_ID":' + '"' + inc_number[i] + '", ' + '"sys_id":' + '"' + inc_sys_id[i] + '", ' + \
                       '"cmdb_ci_value":' + '"' + cmdb_ci_value[i] + '", ' + '"automation_executed": "1"}}'
        payload.append(json.dumps(payload_snow))
        print("Payload: ", json.dumps(payload_snow))


payload_snow = json.dumps(payload_snow)
payload_snow = payload_snow.replace('\\','')
print("payload_snow:", payload_snow)

@app.route('/ansible-get')
def post_data():
    token_endpoint_url = 'http://192.168.100.100/api/v2/tokens/'
    headers_basic = {"Authorization": "Basic YWRtaW46cGFzc3dvcmQ=", "content-type": "application/json"}
    data = requests.post(url=token_endpoint_url, headers=headers_basic)
    response_json = data.json()
    print(response_json)
    token_value = response_json["token"]
    print("SSO token value:", token_value)

    url = 'http://192.168.100.100/api/v2/job_templates/14/launch/'
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token_value}
    print("Final payload:", payload_snow)

    response = requests.post(url, headers=headers, data=payload_snow)
    print('Response code =', response.status_code)
    print('\nResponse headers =', response.headers)
    print('\nResponse =', response.content)

    job_id_num = json.loads(response.content)["job"]
    if job_id_num:
        print("\nJob id received:\nJob id = ", job_id_num)
        current_dt = datetime.datetime.now()
        current_timestamp = current_dt.strftime("%b %d %Y; %H:%M:%S")
        get_sys_id = json.loads(payload_snow)["extra_vars"]
        sys_id_value = get_sys_id["sys_id"]

        SNOW_put_url = 'https://dev94486.service-now.com/api/now/table/incident/' + str(sys_id_value)
        print(SNOW_put_url)
        payload = {
            'state': '2',
            'work_notes': 'Job id as received from Ansible: ' + str(job_id_num) + '\nCurrent timestamp: ' + (
                current_timestamp) + '.',

        }
        response = requests.put(SNOW_put_url, auth=(snow_username, snow_password), headers=headers,
                                data=json.dumps(payload))

        if response.status_code != 201:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            print("\nIncident updated successfully")
        else:
            print("Response code: ", response.status_code)
            print("Incident update failed")
    return response.content


if __name__ == '__main__':
    snow_get_req()
    parse_response()
    app.run(host="192.168.100.100", port=8004, debug=True)