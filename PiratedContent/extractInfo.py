# -*- coding: utf-8 -*-
# pip install pandas
# pip install -U scikit-learn

import os
import webbrowser

import numpy as np
import pandas as pd
import googleapiclient.discovery
import pickle
import argparse, sklearn
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder

api_key = 'AIzaSyAelTBaXBmwUMWLwlWTLI-xcjW5rGhAApA'  # the api code we got
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=api_key)
trump_playlist = 'PLKOAoICmbyV3a0l4Eiuhk_obmaiWcJZ--'

#===========================================================#

def machineLearning(resultPD):
    resultPD = makeDataAsLabels(resultPD)
    X = resultPD.drop('class', axis=1)
    Y = resultPD['class']
    X.fillna(0, inplace=True)
    Y.fillna(0, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    pipe = make_pipeline(StandardScaler(), LogisticRegression())
    pipe.fit(X_train, y_train)
    score = pipe.score(X_test, y_test)
    print(score)

##########=====================================##############
def GetComments(v_id, emoji=None):  # getting the comments of the video
    retlist = []

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=v_id,
        maxResults=100
    )

    response = request.execute()

    while True:

        for item in response['items']:
            comment = str(item['snippet']['topLevelComment']
                          ['snippet']['textDisplay'])
            comment = emoji.demojize(comment)
            comment = comment.encode('ascii', 'ignore').decode('ascii', 'ignore')
            retlist.append(comment)

        request = youtube.commentThreads().list_next(request, response)

        if request is None:
            break

        response = request.execute()

    return retlist


##########=====================================##############
def GetVideoInfo(v_id):  # getting the video's information-metadata
    request = youtube.videos().list(
        part="statistics, contentDetails, liveStreamingDetails, player, recordingDetails, snippet, status, topicDetails",
        id=v_id
    )
    response = request.execute()
    return response


##########=====================================##############
def GetPlatlistVideosId(pl_Id):
    retlist = []
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=pl_Id,
        maxResults=50)

    try:
        response = request.execute()
    except:
        return retlist

    while True:

        for item in response['items']:
            retlist.append(item['contentDetails']['videoId'])

        request = youtube.playlistItems().list_next(request, response)

        if request is None:
            break

        response = request.execute()

    return retlist


##########=====================================##############
def getVideoListInfo(lis):
    listInfo = [GetVideoInfo(x) for x in lis]

    dfListInfo = pd.json_normalize(listInfo, 'items')
    return dfListInfo


##########=====================================##############
def getChannelToPandas(p_id):
    lis = GetPlatlistVideosId(trump_playlist)

    listInfo = [GetVideoInfo(x) for x in lis]

    dfListInfo = pd.json_normalize(listInfo, 'items')
    return dfListInfo


##########=====================================##############
def runOnListOfPlaylists(listOfPlaylists):
    lisOfDfs = [getChannelToPandas(d) for d in listOfPlaylists]

    result = pd.concat(lisOfDfs)
    return result


##########==============MAIN==============##############
def makeDataAsLabels(dfn):
    le = LabelEncoder()
    df1 = pd.DataFrame()
    for col in dfn.select_dtypes(include=['object']).columns:
        df1[col] = dfn[col].apply(le.fit_transform)

    return dfn


# if __name__ == '__main__':
def getData():
    badPL = [trump_playlist, trump_playlist]
    goodPl = [trump_playlist, trump_playlist]
    blackList = ['vdzB3b4XZog',
                 'rmth37-kkr0',
                 'BmPW6yCc1Aw',
                 'b9-WCrPqcCI'
                 ]
    whiteList = ['wQpdlKYlmyY',

                 ]
    blackListPD = getVideoListInfo(blackList)
    whiteListPD = getVideoListInfo(whiteList)
    goodPD = runOnListOfPlaylists(goodPl)

    goodPD = pd.concat([goodPD, whiteListPD])

    goodPD['class'] = 1
    badPD = runOnListOfPlaylists(badPL)
    badPD = pd.concat([badPD, blackListPD])
    badPD['class'] = 0
    resultPD = pd.concat([goodPD, badPD])
    resultPD.to_csv('result.csv')
    data = np.array(pd.read_csv('result.csv'))
    html = '<h2>Here is the table with the data</h2>'
    html += '<table style="width:100%;border-collapse: collapse; margin: 25px 0;font-size: 0.9em;font-family: sans-serif;min-width: 400px;box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);" id=\"my_table1\">'
    html += '<tr style="background-color: #009879;color: #ffffff;text-align: left;" >'
    html += '<th style="padding: 12px 15px;"><b>link</b></th><th style="padding: 12px 15px;"><b>path</b></th><th style="padding: 12px 15px;"><b>class</b></th>'
    html += "</tr>"
    for index, dataRow in enumerate(data):
        if dataRow[-1] == 0:
            if index % 2 == 0:
                html += '<tr style="color: RED;border-bottom: 1px solid #dddddd;background-color: #f3f3f3;">'
            else:
                html += '<tr style="color: RED;border-bottom: 1px solid #dddddd;">'
            html += '<td style="padding: 12px 15px;"><a href='
            html += 'https://www.youtube.com/watch?v='
            html += str(dataRow[3])
            html += '/>'
            html += str(dataRow[6])
            html += '</a>'
            html += '</td><td style="padding: 12px 15px;">'
            html += str(dataRow[3])
            html += '</td><td style="padding: 12px 15px;">'
            html += 'Pirate content'
            html += '</td></tr">'
            html += '</td><td style="padding: 12px 15px;">'
            html += '<button type="button" onclick="alert(\'Reported to YouTube!!\')">Report to youtube!</button>'
            html += '</td></tr">'

        else:
            if index % 2 == 0:
                html += '<tr style="color: GREEN;border-bottom: 1px solid #dddddd;background-color: #f3f3f3;">'
            else:
                html += '<tr style="color: GREEN;border-bottom: 1px solid #dddddd;">'
            html += '<td style="padding: 12px 15px;"><a href='
            html += 'https://www.youtube.com/watch?v='
            html += str(dataRow[3])
            html += '/>'
            html += str(dataRow[6])
            html += '</a>'
            html += '</td><td style="padding: 12px 15px;">'
            html += str(dataRow[3])
            html += '</td><td style="padding: 12px 15px;">'
            html += 'Approved content'
            html += '</td></tr>'
    html += '</table>'

    return html