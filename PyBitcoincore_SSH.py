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
ssh_password = 'raspiblitz'

# CONNECT
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_host, ssh_port, ssh_user, ssh_password)

# GetBestBlockHash                                                                           # Returns the hash (str) of the best (tip) block in the most-work fully-validated chain.
def getbestblockhash():
    command = f'bitcoin-cli getbestblockhash'
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:                                             # [NOTE] : Error handling is only done on the machine we are connected to via ssh by checking the command's exit status
        output = stdout.read().decode('utf-8')
        return output.rstrip('\n')
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 

# GetBlock                                                                                   # If verbosity is 0, returns a string (str) that is serialized, hex-encoded data for block ‘block_hash’.
def getblock(block_hash:str, verbosity:int=1):                                                       # If verbosity is 1, returns an object (dict) with information about block ‘block_hash’.
    command = f'bitcoin-cli getblock {block_hash} {verbosity}'                               # If verbosity is 2, returns an object (dict) with information about block ‘block_hash’
    stdin, stdout, stderr = ssh.exec_command(command)                                        #  and information about each transaction.
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')    
        if verbosity == 0:                                                                           # Translation from hex / json to human-readable text customized on the verbosity parameter
#            print(output)                                                                           #   (totally optional, to remove the "print"s comment out line 48 and lines 51 to 62)
            return output.rstrip('\n')
        load = json.loads(output)                                                  
#        if verbosity == 1:
#            for key in load:
#                if key != 'tx':
#                    print(key + ': ' + str(load[key]))
#                else:  
#                    print(key + ':\n  ' + str(load[key]).replace(',','\n ').replace('[','').replace(']',''))
#        elif verbosity == 2:
#            for key in load:
#                if key != 'tx':
#                    print(key + ': ' + str(load[key]))
#                else:  
#                    pprint.pprint(load[key])
        return load
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 

# GetBlockchainInfo                                                                         # Returns an object (dict) containing various state info regarding blockchain processing.
def getblockchaininfo():
    command = f'bitcoin-cli getblockchaininfo'       
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        load = json.loads(output)
#        for key in load:
#                if key != 'tx':                                                                   # Translation to human-readable text (optional, lines 76 to 78)
#                    print(key + ': ' + str(load[key]))
        return load
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 
           
# GetBlockCount                                                                             # Returns the height (int) of the most-work fully-validated chain.
def getblockcount():
    command = f'bitcoin-cli getblockcount'       
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        return output
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 
    
# GetBlockFilter                                                                            # Retrieve a BIP 157 content filter (dict) for a particular block. 
def getblockfilter(block_hash:str, filter_type:str='basic'):                                        #   (requires blockfilterindex=basic in bitcoin.conf file)
    command = f'bitcoin-cli getblockfilter {block_hash.replace('\n','')} {filter_type}'       
    stdin, stdout, stderr = ssh.exec_command(command)                  
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        load = json.loads(output)
#        for key in load:                                                                         # Translation to human-readable text (optional, lines 104-105)
#            print(key + ': ' + str(load[key])) 
        return load
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 
    
# GetBlockHash                                                                               # Returns hash (str) of block in best-block-chain at height provided.
def getblockhash(block_height:int):
    command = f'bitcoin-cli getblockhash {block_height}'
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        return output.rstrip('\n')
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 

#GetBlockHeader
def getblockheader(block_hash:str, verbose:str='true'):                                                # If verbose is false, returns a string (str) that is serialized, hex-encoded data for blockheader ‘hash’.
    command = f'bitcoin-cli getblockheader {block_hash} {verbose.lower()}'                             # If verbose is true, returns an Object (dict) with information about blockheader ‘hash’.
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')                                        # [NOTE] : verbose must NOT be boolean, but a lowercase string.
        if verbose.lower() == 'false':
#            print(output)                                                                                   # Translation from hex / json to human-readable text customized on the verbosity parameter
            return output.rstrip('\n')                                                                       #   (optional, lines 131 and 134 to 139)
        load = json.loads(output)
#        if verbose.lower() == 'true':
#            for key in load:
#                if key != 'tx':
#                    print(key + ': ' + str(load[key]))
#                else:  
#                    print(key + ':\n  ' + str(load[key]).replace(',','\n '))
        return load
    else: 
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 

#GetBlockStats
def getblockstats(block_hash_or_height, stats:str=''):                                                   # [WORK IN PROGRESS] Compute per block statistics for a given window. All amounts are in satoshis.
    command = f"bitcoin-cli getblockstats {block_hash_or_height} '{stats}'"                              #   It won’t work for some heights with pruning.    
    stdin, stdout, stderr = ssh.exec_command(command)  
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        return output
    else:
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}') 

#GetChainTips
def getchaintips():                                                                                      # Return information (list) about all known tips in the block tree, including the main chain as well as orphaned branches.
    command = f'bitcoin-cli getchaintips'
    stdin, stdout, stderr = ssh.exec_command(command)  
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        load = json.loads(output)
#        print(output.replace('[','').replace(']','').replace('{','').replace('}','').replace('"',''))        # Optional translation to human-readable text (line 165)
        return load
    else:
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}')
    
#GetChainTxStats
def getchaintxstats(nblocks:int='' , block_hash:str=''):                                                 # Compute statistics (dict) about the total number and rate of transactions in the chain.
    command = f'bitcoin-cli getchaintxstats {nblocks} {block_hash}'
    stdin, stdout, stderr = ssh.exec_command(command)  
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        load = json.loads(output)
#        for key in load:                                                                                    # Optional translator to human-readable text (lines 179-180)
#           print(key + ': ' + str(load[key])) 
        return load
    else:
        err = stdout.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}')

#print(getblockstats('00000000000000001a2a29708d38505ec20d8f51b4ca28f6b526d1d22073c7e0','[''avgfee'']'))
#getblockstats(getblockhash(1233))
print(getchaintips())


ssh.close()
