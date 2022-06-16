#!/usr/bin/env python

import sys
import configparser
import SendManager

from flask import (
    Flask, request,
)

# Creating the application instance
app = Flask(__name__)


# Create a URL route in our application for "/"
@app.route('/GetConfig', methods=['GET'])
# function used to get the configurations of a device
def getconfig():
    get_content = request.get_json()
    get_api_command = get_content["command"]

    config_details = SendManager.SendCommandToDevice(get_api_command, Device_Type, Host, Username, Password)
    if config_details == 0:
        return "error in the function"

    else:
        return config_details


@app.route('/DeleteConfig', methods=['DELETE'])
# function used to get the configurations of a device
def deleteconfig():
    # Parse and store the json  payload in content
    delete_content = request.get_json()
    delete_interface_name = delete_content["name"]
    #    print(delete_interface_name)
    rpc_msg = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">      <interface>
              <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
              <name>%s</name>
              </Loopback>
          </interface>
        </native>
    </config>
    '''

    send_return = SendManager.sendmanager(rpc_msg % delete_interface_name, Host, Port, Username, Password)

    if send_return == 0:
        return "error in the function"
    else:
        return "deleted the interface"


@app.route('/CreateInterface', methods=['POST'])
def create_interface():
    create_content = request.get_json()
    print(create_content)
    loopback_ip = create_content["ip"]
    interface_name = create_content["name"]
    interface_netmask = create_content["netmask"]
    #    print(loopback_ip)
    #    print(interface_name)
    #    print(interfacenet_mask)

    creation_rpc = '''
    <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
    <Loopback>
    <name>%s</name>
    <ip>
    <address>
    <primary>
    <address>%s</address>
    <mask>%s</mask>
    </primary>                    
    </address>
    </ip>
    </Loopback>
    </interface>
    </native>
    </config>
    '''

    sendreturn = SendManager.sendmanager(creation_rpc % (interface_name, loopback_ip, interface_netmask), Host, Port,
                                         Username,
                                         Password)

    if sendreturn == 0:
        return "error in the function"
    else:
        return "Created the interface"


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    config = configparser.ConfigParser()

    # Reading config file
    try:
        config.read("Config.ini")
        Username = config.get('0', "Username")
        Password = config.get('0', "Password")
        Device_Type = config.get('0', "Device_Type")
        Host = config.get('0', "Host")
        Port = config.get('0', "Port")
        Netmask = config.get('0', "Netmask")

    except:
        print("Config file not found")
        sys.exit(0)
    app.run(debug=True)


