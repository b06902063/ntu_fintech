import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy
from profitEstimateOpen import profitEstimateOpen

dailyOhlcv = pd.read_csv(sys.argv[1])
minutelyOhlcv = pd.read_csv(sys.argv[2])
evalDays = 18
action = np.zeros((evalDays,1))
openPricev = dailyOhlcv["open"].tail(evalDays).values
capital = 500000.0
stock = 0.0
maxReturn = 0.0
record = []
total = 500000.0
returnRate = 0.0
'''
for a in range(0, 10):
  for b in range(a, 50):
    for c in range(128, 312):
      for d in range(1,5):
        for e in range(10, 15):
          for f in range(20,50,10):
            for g in range(60, 90, 10):  
              #a,b,c,d,e,f,g = 0,19,296,3,14,60,80
'''
a,b,c,d,e,f,g = 0, 19, 64, 3, 20, 60, 70
for ic in range(evalDays,0,-1):
  dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
  #print dailyOhlcvFile["open"][1]
  dateStr = dailyOhlcvFile.iloc[-1,0]
  minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
  #print minutelyOhlcvFile["open"]
  action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic])
  capital, stock, total = profitEstimateOpen(capital, stock, openPricev[evalDays-ic], action[evalDays-ic])
  returnRate=(total-500000)/500000
print 'return rate:', returnRate , 'total:', total
if returnRate > maxReturn:
  maxReturn = returnRate
  #print 'maxreturn:', maxReturn
  record = [a,b,c,d,e,f,g]
#print 'parameter:', [a,b,c,d,e,f,g]
#print action
