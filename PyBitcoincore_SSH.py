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

# SSH CONNECTION SETTING
ssh_host = '192.168.0.19'
ssh_port = 22
ssh_user = 'admin'
ssh_password = 'raspiblitz'

# CONNECT
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_host, ssh_port, ssh_user, ssh_password)

def run_command(command:str)->str:
    stdin, stdout, stderr = ssh.exec_command(command)                                        #  and information about each transaction.
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        return stdout.read().decode('utf-8')
    else:
        err = stderr.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}')

# GetBestBlockHash                                                                           # Returns the hash (str) of the best (tip) block in the most-work fully-validated chain.
#def getbestblockhash():
#    command = f'bitcoin-cli getbestblockhash'
#    stdin, stdout, stderr = ssh.exec_command(command)
#    exit_status = stdout.channel.recv_exit_status()
#    if exit_status == 0:                                             # [NOTE] : Error handling is only done on the machine we are connected to via ssh by checking the command's exit status
#        output = stdout.read().decode('utf-8')
#        return output.rstrip('\n')
#    else: 
#        err = stderr.read().decode('utf-8')
#        return(f'Exit status: {exit_status}\n{err}') 
#
# GetBlock                                                                                   # If verbosity is 0, returns a string (str) that is serialized, hex-encoded data for block ‘block_hash’.
def getblock(block_hash:str, verbosity:int=1):                                                       # If verbosity is 1, returns an object (dict) with information about block ‘block_hash’.
    command = f'bitcoin-cli getblock {block_hash} {verbosity}'                               # If verbosity is 2, returns an object (dict) with information about block ‘block_hash’    
    if verbosity == 0:                                                                           # Translation from hex / json to human-readable text customized on the verbosity parameter
        return run_command(command).rstrip('\n')
    elif verbosity == 1: 
        load = json.loads(output)                                                  
        return load
    

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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
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
        err = stderr.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}')

#GetDifficulty
def getdifficulty():                                                                                       # Returns the proof-of-work difficulty (float) as a multiple of the minimum difficulty.
    command = f'bitcoin-cli getdifficulty'
    stdin, stdout, stderr = ssh.exec_command(command)  
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        return float(output)
    else:
        err = stderr.read().decode('utf-8')
        return(f'Exit status: {exit_status}\n{err}')

#GetMempoolAncestors
def getmempoolancestors(txid:str, verbose:str='true'):
    command = f'bitcoin-cli getmempoolancestors {txid} {verbose.lower()}'                             # If verbose is true, returns an Object (dict) with information about blockheader ‘hash’.
    stdin, stdout, stderr = ssh.exec_command(command)                                                 # If verbose is false, returns an array (list) of transaction ids.
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')  
        if verbose.lower() == 'false':
            return output.rstrip('\n')                                                                      
        load = json.loads(output)
        return load
    else:
        err = stderr.read().decode('utf-8')
        print(f'Exit status: {exit_status}\n{err}')

#GetMempoolInfo
def getmempoolinfo():                                                                   # Returns details (dict) on the active state of the TX memory pool.
    command = f'bitcoin-cli getmempoolinfo'
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')
        load = json.loads(output)
#        for key in load:                                                                                    # Optional translator to human-readable text (lines 221-222)
#           print(key + ': ' + str(load[key])) 
        return(load)
    else:
        err = stderr.read().decode('utf-8')
        print(f'Exit status: {exit_status}\n{err}')

#GetRawMempool                                                                                             [WORK IN PROGRESS]
def getrawmempool(verbose:str='false',mempool_sequence:str='false'):                                       # Returns all transaction ids in memory pool as a json array of string transaction ids.
    command = f'bitcoin-cli getrawmempool {verbose.lower()} {mempool_sequence.lower()}'                    # 
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        output = stdout.read().decode('utf-8')  
        print(output)
    else:
        err = stderr.read().decode('utf-8')
        print(f'Exit status: {exit_status}\n{err}')


@command
def getbestblockhash():
    ''' GetBestBlockHash wrapped '''                                                                          # Returns the hash (str) of the best (tip) block in the most-work fully-validated chain.


#print(getbestblockhash())

ssh.exec_command('exit')
