# coding=Big5
import csv
import sys

def sort_element(elem):
    return elem[0]

def read_data():
  filename = sys.argv[1]
  #data = []
  data_2 = []
  date = 0
  date_2 = 0
  with open(filename , encoding='big5') as csvdata:
    rows = csv.reader(csvdata)
    flag = 0
    flag_start = 0
    for row in rows:
      if flag == 0:
        flag = 1
      else:
        if row[1][0:2] == 'TX':
          if flag_start == 0 and int(row[3]) == 84500:
            flag_start = 1
            date_2 = row[2]
            date = row[0]
          if int(row[3]) >= 84500 and int(row[3]) <= 134500 and row[0] == date and row[2] == date_2:
            data_2.append(float(row[4]))
  #data.sort(key=sort_element)
  return data_2

def main():
  data_2 = read_data()
  open_price = (data_2[0])
  close_price = (data_2[-1])
  high_price = max(data_2)
  low_price = min(data_2)
  print(int(open_price) , int(high_price) , int(low_price) , int(close_price))


main()