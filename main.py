import datetime as date
import requests as requests
from block import *
from transaction import *
import simplejson as json
import random
from keys import getEncodedKeys
import os
import time

public_key, _ = getEncodedKeys()

def mineCycle():
    try:
        while True:
            newBlock = mine(getCurrentBlock(), getCurrentTransactions())
            submitNewBlock(newBlock)
    except KeyboardInterrupt:
        pass
    

def mineDebug(previousBlock, transactions):
    os.system('clear')
    print("Status: Currently mining")
    print("Press ctrl+C to return to menu.. ")
    print("")
    print("Previous block: ")
    previousBlock.display()
    print("")

# Attempts to mine a new block
def mine(previousBlock, transactions):
    nonce = 0
    newBlock = nextBlock(previousBlock, json.dumps(transactions), nonce)
    mineDebug(previousBlock, transactions)

    beginTimestamp = date.datetime.now()
    while (not newBlock.validate()):
        nonce = random.randint(1, 100000000000)
        newBlock = nextBlock(previousBlock, json.dumps(transactions), nonce)

        if ((date.datetime.now() - beginTimestamp).total_seconds() > 5):
            beginTimestamp = date.datetime.now()
            previousBlock = getCurrentBlock()
            transactions = getCurrentTransactions()
            mineDebug(previousBlock, transactions)
    return newBlock

def getCurrentBlock():
    req = requests.get('http://localhost:5000/current').json()
    currentBlock = Block(req['index'], req['transactions'], req['nonce'], req['previousHash'], req['hash'])
    return currentBlock

def getCurrentTransactions():
    transactions = requests.get('http://localhost:5000/transactions').json()
    transaction = Transaction("MINER", public_key, 1)
    transactions.append(transaction)
    return transactions

def submitNewBlock(newBlock):
    req = requests.post('http://localhost:5000/mine', json=newBlock)
    if req.status_code == 200:
        print("**Successfully mined block!**")
        time.sleep(3)

def postTransaction(reciever, amount):
    transaction = Transaction(public_key, reciever, amount)
    req = requests.post('http://localhost:5000/transactions', json=transaction)
    return req

def sendCoins():
    os.system('clear')
    reciever = input("Enter address to send coins to: ")
    amount = input("Enter amount to send: ")
    res = postTransaction(reciever, int(amount))
    if res.status_code == 200:
        print("Transaction successfully sent!")
    else:
        print(res.json()["error"])

    input("Press any key to return to menu...")


def checkBalance():
    balanceObject = {"public_key": public_key}
    req = requests.post('http://localhost:5000/balance', json=balanceObject)
    #os.system('cls')
    os.system('clear')
    print("Your public key is: " + public_key)
    print("Your balance is: " + req.text)
    print("")
    input("Press any key to return to menu...")

while(1):
    os.system('clear')
    print("Welcome to Campcoin miner")
    print("")
    print("Select an option:")
    print("(M) Start mining")
    print("(T) Send coins")
    print("(B) Check your balance or view your Public Key")
    print()
    print("Press Ctrl+C to exit")
    print()
    option = input("Enter a selection: ")

    if option == "B":
        checkBalance()

    if option == "M":
        mineCycle()

    if option == "T":
        sendCoins()