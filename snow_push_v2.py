import datetime
import requests
import json
from flask import Flask, Response, request, jsonify
import requests

app = Flask(__name__)


@app.route('/ansible-post/', methods=['POST', 'GET'])
def snow_post():
    if request.method == 'POST':
        response_ansible = request.json
        print("Response from Ansible:", response_ansible)

        snow_inst = 'dev94486.service-now.com'
        snow_inst_table = 'incident'
        snow_inst_endpoint_url = 'https://' + snow_inst + '/api/now/table/' + snow_inst_table
        snow_username = 'admin'
        snow_password = 'Adminadmin1'
        headers = {"Accept": "application/json"}
        print("SNOW URL endpoint=", snow_inst_endpoint_url)

        current_dt = datetime.datetime.now()
        current_timestamp = current_dt.strftime("%b %d %Y; %H:%M:%S")

        update_details = response_ansible["update"]
        inc_sysid = update_details["extTicketID"]
        automation_exe = update_details["automation_executed"]
        work_notes = update_details["status"]

        if automation_exe == str(1):
            assign_group = 'AnsiblePOC1'
            state = '6'
            close_code = 'Solved (Permanently)'
            close_notes = work_notes
            notes = work_notes

        elif automation_exe == str(2):
            assign_group = 'AnsiblePOC1'
            state = '2'
            notes = work_notes

        else:
            state = '3'
            assign_group = 'AnsiblePOC_L3'
            hold_reason = 'Awaiting Problem'
            notes = work_notes

        snow_put_url = snow_inst_endpoint_url + '/' + inc_sysid
        print(snow_put_url)
        if state == str(6):
            payload = {
                'state': state,
                'close_code': close_code,
                'close_notes': close_notes,
                'work_notes': notes,
                'caller_id': 'Abel Tuter',
                'assignment_group': assign_group
            }
        elif state == str(2):
            payload = {
                'state': state,
                'work_notes': notes,
                'caller_id': 'Abel Tuter',
                'assignment_group': assign_group
            }

        elif state == str(3):
            payload = {
                'state': state,
                'hold_reason': hold_reason,
                'work_notes': notes,
                'caller_id': 'Abel Tuter',
                'assignment_group': assign_group
            }
        print(payload)
        response = requests.put(snow_put_url, auth=(snow_username, snow_password), headers=headers,
                                data=json.dumps(payload))

        print("Response code: ", response.status_code)
        if response.status_code == 200:
            print("Incident updated successfully.")
        else:
            print("Error updating incident.")
    return response_ansible


if __name__ == '__main__':
    app.run(host="192.168.100.100", port=8002, debug=True)
