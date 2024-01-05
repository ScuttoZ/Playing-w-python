#########################################################################################
#########################################################################################
####                                                                                 ####
####  Concept:                                                                       ####
####  Python implementation of bitcoin-cli commands executed through ssh connection  ####
####  to someone's personal bitcoin node. Code is designed for bitcoin core-based    ####
####  clients, such as Raspiblitz, BTCpayserver, Umbrel and others, by prioritizing  ####
####  readability and ease of use.                                                   ####
####                                                                                 ####
#########################################################################################
#########################################################################################

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

# GetBlockHash                                                          # Returns the hash (str) of the best (tip) block in the most-work fully-validated chain.
def getblockhash(block_height):
    command = f'bitcoin-cli getblockhash {block_height}'
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    return(output) 

# GetBlock                                                              # If verbosity is 0, returns a string (str) that is serialized, hex-encoded data for block ‘block_hash’.
def getblock(block_hash, verbosity=1):                                # If verbosity is 1, returns an object (dict) with information about block ‘block_hash’.
    command = f'bitcoin-cli getblock "{block_hash}" {verbosity}'        # If verbosity is 2, returns an object (dict) with information about block ‘block_hash’
    stdin, stdout, stderr = ssh.exec_command(command)                   #  and information about each transaction.
    output = stdout.read().decode('utf-8')    
    if verbosity == 0:                                                      # Translation from hex / json to human-readable text customized on the verbosity parameter
        print(output)                                                       # (totally optional, to remove the "print"s comment out line 41 and lines 44 to 55)
        return(output)
    load = json.loads(output)                                                  
    if verbosity == 1:
        for key in load:
            if key != 'tx':
                print(key + ': ' + str(load[key]))
            else:  
                print(key + ':\n  ' + str(load[key]).replace(',','\n ').replace('[','').replace(']',''))
    elif verbosity == 2:
        for key in load:
            if key != 'tx':
                print(key + ': ' + str(load[key]))
            else:  
                pprint.pprint(load[key])
    return(load)

# GetBlockchainInfo                                                          # Returns an object (dict) containing various state info regarding blockchain processing.
def getblockchaininfo():
    command = f'bitcoin-cli getblockchaininfo'       
    stdin, stdout, stderr = ssh.exec_command(command)                  
    output = stdout.read().decode('utf-8')
    load = json.loads(output)
    for key in load:                                                            # 
            if key != 'tx':                                                     # Translation to human-readable text (optional, lines 64 to 66)
                print(key + ': ' + str(load[key]))                              #
    return(load)
            
# GetBlockCount                                                              # Returns the height (int) of the most-work fully-validated chain.
def getblockcount():
    command = f'bitcoin-cli getblockcount'       
    stdin, stdout, stderr = ssh.exec_command(command)                  
    output = stdout.read().decode('utf-8')
    return(output)

# GetBlockFilter                                                             # Retrieve a BIP 157 content filter for a particular block.
#def getblockfilter(block_hash, filter_type='basic'):
#    command = f'bitcoin-cli getblockfilter {block_hash} {filter_type}'       





#getblockhash(0)
getblockfilter('00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09')
#getblockchaininfo()

ssh.close()
