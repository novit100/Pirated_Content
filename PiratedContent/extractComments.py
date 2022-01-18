# -*- coding: utf-8 -*-
# pip install pandas
# pip install -U scikit-learn

import pandas as pd
import googleapiclient.discovery
import pickle
import argparse, sklearn
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder

api_key ='AIzaSyCpInxXHXr6yQMejlkwcxrv6seqcDeke7M'  # the api code we got
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=api_key)

plGood1 = 'PL355D512277EFFA06'
plGood2 = 'PLF-BDTAHX0p5upMCX1X2cbmLDhSkz6k0G'
plBad1 = 'PLqaWdnCe3FecWs9VN4B6GnMKYLuFkNmj0'
plBad2 = 'PLTQrToH18n95KPlgYnwovi8_yKy7RiiAL'


# trump_playlist = 'PLKOAoICmbyV3a0l4Eiuhk_obmaiWcJZ--'

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
            # if isinstance(NoneType,emoji)==false
            # comment = emoji.demojize(comment)
            comment = comment.encode('ascii', 'ignore').decode('ascii', 'ignore')
            retlist.append({"v_id":v_id,'comment': comment})

        request = youtube.commentThreads().list_next(request, response)

        if request is None:
            break

        response = request.execute()

    return retlist


##########=====================================##############
def GetVideoInfo(v_id):  # getting the video's information
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


def getVideoListInfo(lis):
    # listInfo = [GetVideoInfo(x) for x in lis]
    listComments = [GetComments(x) for x in lis]
    listComments =[ x for y in listComments for x in y]
    return listComments


##########=====================================##############
def getChannelToPandas(p_id):
    # lis = GetPlatlistVideosId(trump_playlist)
    lis = GetPlatlistVideosId(p_id)
    listComments = [GetComments(x) for x in lis]
    listComments =[ x for y in listComments for x in y]
    return listComments


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


if __name__ == '__main__':
    badPL = [plGood1, plGood2]
    goodPl = [plBad1, plBad2]
    blackList = ['vdzB3b4XZog',
                 'rmth37-kkr0',
                 'BmPW6yCc1Aw',
                 ]
    whiteList = ['wQpdlKYlmyY',
                 'KM4Xe6Dlp0Y',
                 'GfO-3Oir-qM',
                 'MhNHR2qkNSY',
                 'D4a6SSQ3hKw'
                 ]
    blackListPD = getVideoListInfo(blackList)

    whiteListPD = getVideoListInfo(whiteList)
    goodPD = pd.DataFrame(whiteListPD)
    #
    # goodPD = runOnListOfPlaylists(goodPl)
    #
    # goodPD = pd.concat([goodPD, whiteListPD])
    badPD =pd.DataFrame(blackListPD)
    goodPD['class'] = 1
    # badPD = runOnListOfPlaylists(badPL)
    # badPD = pd.concat([badPD, blackListPD])
    badPD['class'] = 0
    resultPD = pd.concat([goodPD, badPD])
    resultPD.to_csv('ourResult.csv')
    # resultPD = makeDataAsLabels(resultPD)
    # X = resultPD.drop('class',axis =1)
    # Y = resultPD['class']
    # X.fillna(0, inplace=True)
    # Y.fillna(0, inplace=True)
    # X_train, X_test, y_train, y_test = train_test_split(X,Y)
    # pipe = make_pipeline(StandardScaler(), LogisticRegression())
    # pipe.fit(X_train, y_train)
    # score = pipe.score(X_test, y_test)
    # print(score)