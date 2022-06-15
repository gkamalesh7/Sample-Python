#!/usr/bin/env python

import requests
import sys
import configparser

from ncclient import manager
RTR1_MGR = manager.connect(host= "ios-xe-mgmt.cisco.com",
                           port = 830,
                           username = "developer",
                           password = "C1sco12345",
                           hostkey_verify = False)



from flask import (
    Flask,
    render_template
)

# Creating the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/GetConfig')
# function used to get the configurations of a device
def GetConfig():

    # Show command that we need to execute
    command = "show ip int brief"

    config_details = SendCommandToDevice(command)
    if config_details == 0:
        return "error in the function"

    else:
        return config_details

@app.route('/DeleteConfig')

# function used to get the configurations of a device
def DeleteConfig():

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

    send_return = sendmanager(rpc_msg %InterfaceName)

    if send_return == 0:
        return "error in the function"
    else:
        return "deleted the interface"



@app.route('/CreateInterface')
def CreateInterface():
    print(addressLoopback)
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

    sendreturn = sendmanager(creation_rpc %(InterfaceName,addressLoopback,Netmask))


    if sendreturn == 0:
        return "error in the function"
    else:
        return "Created the interface"


## Function to send the required interface level details to the deice using connect manager
def sendmanager(rpc_msg):

    with manager.connect(host= Host, port= Port, username= Username, password= Password,hostkey_verify=False) as m:
        send = m.edit_config(rpc_msg , target='running')

def SendCommandToDevice(command):
    from netmiko import ConnectHandler
    from getpass import getpass

# hardcoded data for the device
#    cisco1 = {
#        "device_type": Device_Type,
#        "host": Host,
#        "username": Username,
#        "password": Password,
#    }
    cisco1 = {
            "device_type": Device_Type,
            "host": Host,
            "username": Username,
            "password": Password,
        }

    with ConnectHandler(**cisco1) as net_connect:
        output = net_connect.send_command(command)

    # Automatically cleans-up the output so that only the show output is returned
    return output


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    config = configparser.ConfigParser()

    # Reading config file
    try:
        config.read("Config.ini")
        addressLoopback = config.get('0', "LoopBackIP")
        InterfaceName = config.get('0', "InterfaceName")
        Username = config.get('0', "Username")
        Password = config.get('0', "Password")
        Device_Type = config.get('0', "Device_Type")
        Host =  config.get('0', "Host")
        Port = config.get('0', "Port")
        Netmask = config.get('0', "Netmask")

    except:
        print
        "Config file not found"
        print
        "v2x_exec.exe -h for help"
        sys.exit(0)
    app.run(debug=True)