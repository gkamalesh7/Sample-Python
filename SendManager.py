from ncclient import manager
RTR1_MGR = manager.connect(host= "ios-xe-mgmt.cisco.com",
                           port = 830,
                           username = "developer",
                           password = "C1sco12345",
                           hostkey_verify = False)

## Function to send the required interface level details to the deice using connect manager
def sendmanager(rpc_msg, Host, Port, Username, Password):

    with manager.connect(host= Host, port= Port, username= Username, password= Password,hostkey_verify=False) as m:
        send = m.edit_config(rpc_msg , target='running')

def SendCommandToDevice(command, Device_Type, Host, Username, Password):
    from netmiko import ConnectHandler
    from getpass import getpass


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

