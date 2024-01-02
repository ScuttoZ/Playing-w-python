import paramiko
import json
import pprint

# SSH CONNECTION SETTING
ssh_host = '192.168.0.19'
ssh_port = 22
ssh_user = 'admin'
ssh_password = 'Scutti97'

# CONNECT
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_host, ssh_port, ssh_user, ssh_password)

# GetBlockHash
def getblockhash(block_height):
    command = f'bitcoin-cli getblockhash {block_height}'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    print(output)  

# GetBlock           WORK IN PROGRESS
def getblock(block_hash, verbosity):
    command = f'bitcoin-cli getblock "{block_hash}" {verbosity}'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    if verbosity == 0:                              # Custom desirialization from hex / json to human-readable text
        print(output)
    elif verbosity == 1 or verbosity == 2:
        output_deserial = '{\n' + ',\n'.join(f'  {key}: {value}' for key, value in json.loads(output).items()) + '\n}'
        pprint.pprint(output_deserial)  




getblockhash(123220)
getblock('0000000000000f669dfab4b2308cb3be0bb14a3b463e06ff6608335411ad4eac',1)


ssh.close()
