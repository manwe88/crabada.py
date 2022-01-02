from common.config import nodeUri, contract, users
from libs.Web3Client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setNodeUri(nodeUri)
    .setCredentials(users[0]['address'], users[0]['privateKey']))

# TEST FUNCTIONS
def testGetNonce():
    pprint(client.getNonce())

# EXECUTE
testGetNonce()