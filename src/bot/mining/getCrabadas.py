"""
Get Crabadas pincer types from API
"""

from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
# from src.helpers.Sms import sendSms
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from typing import List
import pandas as pd
from time import time
from datetime import datetime, timedelta

baseURL = '/home/avalanche/Documents/crabada/'
def getCrabadas(start: int, end: int) -> [str, List]:
    """
    get all crabadas into an excel with their class and also pincer type
    """

    # crabada_dict = {'bulk':[], 'gem':[], 'prime':[], 'surge':[], 'craboid':[], 'organic':[], 'sunken': [], 'ruined':[]}
    df = pd.DataFrame(columns=['crabNo', 'class', 'pincerType', 'eyeType','pureNumber',
                               'hp','speed','damage','critical','armor','bp','mp','birthday','hatchDay', 'dna','owner',
                               'owner_full_name','breed_count'])

    crabPincerList = []
    for crabNo in range(start, end):
        # start = time()
        crab_pincer = crabadaWeb2Client.getCrabada(crabNo)
        if type(crab_pincer[10]) == str:
            birthday = 0
            dna = 0
        else:
            birthday = crab_pincer[10]
            dna = crab_pincer[11]
      # end = time()
        # totalTime = end - start
        # print('request time: ',totalTime)
        crabDict = {'crabNo': [crabNo],
                    'class':[crab_pincer[0]],
                    'pincerType': [crab_pincer[1]],
                    'eyeType': [crab_pincer[15]],
                    'pureNumber': [crab_pincer[2]],
                    'hp': [crab_pincer[3]],
                    'speed': [crab_pincer[4]],
                    'damage': [crab_pincer[5]],
                    'critical': [crab_pincer[6]],
                    'armor': [crab_pincer[7]],
                    'bp': [crab_pincer[8]],
                    'mp': [crab_pincer[9]],
                    'birthday': [datetime.fromtimestamp(birthday)],
                    'hatchDay': [datetime.fromtimestamp(birthday) + timedelta(days=5)],
                    'dna': hex(int(dna)),
                    'owner': [crab_pincer[12]],
                    'owner_full_name': [crab_pincer[13]],
                    'breed_count': [crab_pincer[14]]
                    }

        # start = time()
        tempDf = pd.DataFrame(crabDict).astype({'dna':str})
        df = pd.concat([df, tempDf], ignore_index=True)
        # end = time()
        # totalTime = end - start
        # print('df time: ', totalTime)

        print(crabNo)
        df.to_csv("crabList_cont2.csv")
    return df

def mergeList():

    mainURL = baseURL + 'crabList.csv'
    copyURL = baseURL + 'crabList_cont2.csv'
    main_df = pd.read_csv(mainURL, index_col=0)
    copy_df = pd.read_csv(copyURL, index_col=0)
    main_df = pd.concat([main_df, copy_df], ignore_index = True)
    main_df.to_csv("crabList.csv")


def setEndNumber(start, end):

    start = end
    return start

def getLastAvailableCrabNo():
    """
    TO DO
    """
    pass

def toHTML(df, name: str): # TO DO write it to the Data folder

    df = df.to_html(index=False)
    # write html to file
    nameHTML = name + '.html'
    text_file = open(nameHTML, "w")
    text_file.write(df)
    text_file.close()

def replaceLines(indexPath, newPath,start, end):
    indexFile = baseURL + indexPath
    newFile = baseURL + newPath

    with open(indexFile, 'r', encoding='utf-8') as file:
        dataIndex = file.readlines()

    with open(newPath, 'r', encoding='utf-8') as file:
        newData = file.readlines()

    j = 0
    for i in range(start, end):

        try:
            dataIndex[i] = newData[j]
        except:
            continue

        j += 1

    # writeURL = baseURL + 'data/' + indexPath
    with open(indexFile, 'w', encoding='utf-8') as file:
        file.writelines(dataIndex)



def writeToHTML():
    mainURL = baseURL + 'crabList.csv'
    df = pd.read_csv(mainURL, index_col=0)
    df = df[df['pureNumber'] == '6']
    df2 = df.groupby(['class', 'pincerType']).size().reset_index(name='Count')
    BULK = df2[df2['class'] == 'BULK'].sort_values('Count', ascending=False)
    CRABOID = df2[df2['class'] == 'CRABOID'].sort_values('Count', ascending=False)
    PRIME = df2[df2['class'] == 'PRIME'].sort_values('Count', ascending=False)
    RUINED = df2[df2['class'] == 'RUINED'].sort_values('Count', ascending=False)
    SURGE = df2[df2['class'] == 'SURGE'].sort_values('Count', ascending=False)
    ORGANIC = df2[df2['class'] == 'ORGANIC'].sort_values('Count', ascending=False)
    SUNKEN = df2[df2['class'] == 'SUNKEN'].sort_values('Count', ascending=False)
    GEM = df2[df2['class'] == 'GEM'].sort_values('Count', ascending=False)

    toHTML(BULK,'BULK')
    toHTML(PRIME,'PRIME')
    toHTML(CRABOID,'CRABOID')
    toHTML(RUINED,'RUINED')
    toHTML(SURGE,'SURGE')
    toHTML(ORGANIC,'ORGANIC')
    toHTML(SUNKEN,'SUNKEN')
    toHTML(GEM,'GEM')

def updateIndexHTML():
    replaceLines('index.html', 'BULK.html', 10, 60)
    replaceLines('index.html', 'SURGE.html', 66, 116)
    replaceLines('index.html', 'PRIME.html', 121, 171)
    replaceLines('index.html', 'GEM.html', 176, 226)
    replaceLines('index.html', 'CRABOID.html', 235, 285)
    replaceLines('index.html', 'RUINED.html', 290, 340)
    replaceLines('index.html', 'SUNKEN.html', 345, 395)
    replaceLines('index.html', 'ORGANIC.html', 400, 450)

start = 1
end = 130000
startTime = time()
print(getCrabadas(start, end))
endTime = time()
totalTime = endTime - startTime
print('Minutes:',totalTime/60, 'Seconds:',totalTime % 60) # TO DO implement a better time format

# mergeList()
# writeToHTML()
# updateIndexHTML()








