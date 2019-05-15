# myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic])
import numpy as np
import operator
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
'''
import warnings
warnings.filterwarnings("ignore")
'''
def RSI(priceVec, n):
    U=[]
    D=[]
    for i in range(n-1,-1,-1):
        if priceVec[-1-i] > priceVec[-1-i-1]:
            U.append(priceVec[-1-i]-priceVec[-1-i-1])
            D.append(0)
        elif priceVec[-1-i] < priceVec[-1-i-1]:
            U.append(0)
            D.append(priceVec[-1-i-1]-priceVec[-1-i])
        else:
            U.append(0)
            D.append(0)
    RS=np.mean(U)/np.mean(D)
    RSIValue = (1.0-1.0/(1.0+RS))
    return RSIValue  


def myStrategy(pastDailyData, pastMinuteData, currPrice):
    a,b,c,d,e,f,g = 0, 19, 64, 3, 20, 0.6, 0.7
    #a,b,c,d,e,f,g = parameter[0], parameter[1], parameter[2], parameter[3], parameter[4], parameter[5], parameter[6]
    pastData=(pastMinuteData['open'].values + pastMinuteData['close'].values)/2.0
    pastDataDaily = pastDailyData['close'].values
    param=[a, b] # 0 19
    windowSize=c # 296
    alpha=param[0]
    beta=param[1]
    action=0
    dataLen = len(pastDataDaily)
    if dataLen<windowSize:
        ma=np.mean(pastDataDaily)
        return 0
    windowedData=pastDataDaily[-windowSize:]
    weight = [i for i in range(1, len(windowedData)+1)]
    #ma=np.mean(windowedData)
    ma = np.dot(weight, windowedData)/sum(weight)
    #print 'ma:', np.mean(windowedData)
    #print 'currPrice:', currPrice
    flag = 0 # 3
    if pastDataDaily[-1-d+1] - pastDataDaily[-1-d] > 0 and pastDataDaily[-1-d+2] - pastDataDaily[-1-d+1] > 0 and pastDataDaily[-1-d+3] - pastDataDaily[-1-d+2] > 0:
        flag = -1
    elif pastDataDaily[-1-d+1] - pastDataDaily[-1-d] < 0 and pastDataDaily[-1-d+2] - pastDataDaily[-1-d+1] < 0 and pastDataDaily[-1-d+3] - pastDataDaily[-1-d+2] < 0:
        flag = 1
    else:
        flag = 0
    #print 'flag', flag

    RSIValue = RSI(pastDailyData['close'].values, e) # 14
    #print 'RSI' , RSIValue

    threshold = 30

    X_trainData1 = np.asarray((pastDailyData['open'].values)[windowSize-2:-1])
    X_trainData2 = np.asarray((pastDailyData['close'].values)[windowSize-2:-1])
    X_train = np.array([np.array(i) for i in zip(X_trainData1,X_trainData2)])
    #X_train = X_train.reshape((-1,1))
    #print 'X train:' , X_train
    y_train = np.array([np.mean(pastDataDaily[i:i+windowSize]) for i in range(-windowSize+len(pastDataDaily)+1)])
    #y_train = y_train.reshape(-1,1)
    #print 'Y train:', y_train

    lin_regressor = LinearRegression()
    
    poly = PolynomialFeatures(2)
    X_transform = poly.fit_transform(X_train)
    #print X_transform
    lin_regressor.fit(X_transform,y_train) 
    x_test = np.array([(pastDailyData['open'].values)[-1], (pastDailyData['close'].values)[-1]])
    x_test = x_test.reshape(1,-1)
    x_test_transform = poly.fit_transform(x_test)
    y_preds = lin_regressor.predict(x_test_transform)
    #print 'predict:', y_preds
    #print 'error:', y_preds-np.mean(windowedData)


    if ((currPrice-alpha)>ma or flag or (currPrice-ma)<-threshold or (currPrice-y_preds) < -50.0) and RSIValue <= f: # 0.30
        action=1
    elif ((currPrice+beta)<ma or -flag or (currPrice-ma)>threshold or (currPrice-y_preds) > 50.0) and RSIValue >= g: # 0.70
        action=-1
    else:
        action=0
    #print 'action:', action
    return action
