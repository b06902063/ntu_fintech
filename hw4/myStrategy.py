'''
 How my strategy is designed: 
 Our technical indicator: 
 Moving average (MA) 
 How the indicator is used: 
 "buy" if currentPrice-alpha>MA % "Sell" if currentPrice+beta<MA 
 How many modifiable parameters and what are they % 3, including window size, alpha, and beta 
 How the system is optimized 
 Window size is fixed at 296, which is obtaind via exhaustive search when [alpha, beta]=[0, 0] 
 Start fminsearch from [alpha, beta]=[10, 10] ==> 153.493% at [8.5 11.25] 
 Use exhaustive search over the range alpha=-5:25 and beta=-5:20 ==> 205.889% at [0, 19]
 '''

def myStrategy(pastData, currPrice):
    import numpy as np
    param=[0, 19]
    windowSize=296
    alpha=param[0]
    beta=param[1]
    action=0
    dataLen = len(pastData)
    if dataLen<windowSize:
        ma=np.mean(pastData)
        return 0
    windowedData=pastData[-windowSize:]
    ma=np.mean(windowedData)
    if (currPrice-alpha)>ma:
        action=1
    elif (currPrice+beta)<ma:
        action=-1
    else:
        action=0
    return action
