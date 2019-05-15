import numpy as np
import pandas as pd
import time

def profitEstimateOpen(capital, stock, price, action):
    flag = 0
    if action == 1:
        if stock == 0:            
            stock = (capital-100)/price
            capital=0
            flag = 1
    elif action == -1:
        if stock > 0:
            capital = stock*price - 100
            stock = 0
            flag = 1
    elif action == 0:
        capital = capital
        stock = stock
    else:
        assert False
    total = capital + stock * price - 100 * flag    

    return capital, stock, total 