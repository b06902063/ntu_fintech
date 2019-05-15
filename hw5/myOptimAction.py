'''
DP to determine when to buy and sell
'''

def operate(currPrice, action, stock, capital, transFeeRate):
  if action == 1:
    if stock==0:            
      stock=capital*(1.0-transFeeRate)/currPrice
      capital=0.0
  elif action == -1:
    if stock>0.0:
      capital=stock*currPrice*(1.0-transFeeRate)
      stock=0.0
  total=capital+stock*currPrice*(1.0-transFeeRate)
  return stock, capital, total

def myOptimAction(priceVec, transFeeRate):
	import numpy as np
	import operator
	import time
	#priceVec = priceVec[:5]
	dataLen = len(priceVec)
	actionVec = np.zeros(dataLen)
	dp_record = np.zeros([2, dataLen]) #0: sell or hold 1: buy or hold

	record = [[], []]
	capital = np.full([2, dataLen], 1.0)
	stock = np.zeros([2, dataLen])

	for i in range(dataLen):
		if i == 0:
			stock[0][i], capital[0][i], dp_record[0][i] = operate(priceVec[i], -1, stock[0][i], capital[0][i], transFeeRate)
			stock[1][i], capital[1][i], dp_record[1][i] = operate(priceVec[i], 1, stock[1][i], capital[1][i], transFeeRate)
			record[0].append(0)
			record[1].append(1)
		else:
			#sell or hold
			if operate(priceVec[i], 0, stock[0][i-1], capital[0][i-1], transFeeRate)[2] > operate(priceVec[i], -1, stock[1][i-1], capital[1][i-1], transFeeRate)[2]:
				stock[0][i], capital[0][i], dp_record[0][i] = operate(priceVec[i], 0, stock[0][i-1], capital[0][i-1], transFeeRate)
				record[0].append(0)
			else:
				stock[0][i], capital[0][i], dp_record[0][i] = operate(priceVec[i], -1, stock[1][i-1], capital[1][i-1], transFeeRate)
				record[0].append(-1)

			#buy or hold
			if operate(priceVec[i], 1, stock[0][i-1], capital[0][i-1], transFeeRate)[2] > operate(priceVec[i], 0, stock[1][i-1], capital[1][i-1], transFeeRate)[2]:
				stock[1][i], capital[1][i], dp_record[1][i] = operate(priceVec[i], 1, stock[0][i-1], capital[0][i-1], transFeeRate)
				record[1].append(1)
			else:
				stock[1][i], capital[1][i], dp_record[1][i] = operate(priceVec[i], 0, stock[1][i-1], capital[1][i-1], transFeeRate)
				record[1].append(0)			
			
		'''
		print 'total:', dp_record[0][i] , dp_record[1][i]
		print 'stock:', stock[0][i], stock[1][i]
		print	'capital', capital[0][i], capital[1][i]
		print '--------------'
		#time.sleep(1)
		'''
	state = 0
	for i in range(dataLen-1, -1, -1):
		if i == dataLen-1:
			if dp_record[0][i] >= dp_record[1][i]:
				actionVec[i] = record[0][i]
				state = 0
			else:
				actionVec[i] = record[1][i]
				state = 1
		else:
			if state == 0 and actionVec[i+1] == -1:
				state = 1
			elif state == 1 and actionVec[i+1] == 1:
				state = 0
			actionVec[i] = record[state][i]

	#print actionVec
	return actionVec
'''

def myOptimAction(priceVec, transFeeRate):
	import numpy as np
	import operator
	dataLen = len(priceVec)
	actionVec = np.zeros(dataLen)
	conCount = 3
	for ic in range(dataLen):
		if ic + conCount + 1 > dataLen:
			continue
		if all(x > 0 for x in list(map(operator.sub,priceVec[ic+1:ic+1+conCount], priceVec[ic:ic+conCount]))):
			actionVec[ic] = 1
		if all(x < 0 for x in list(map(operator.sub,priceVec[ic+1:ic+1+conCount], priceVec[ic:ic+conCount]))):
			actionVec[ic] = -1
	prevAction = -1
	for ic in range(dataLen):
		if actionVec[ic] == prevAction:
			actionVec[ic] = 0
		elif actionVec[ic] == -prevAction:
			prevAction = actionVec[ic]
	return actionVec
	'''

