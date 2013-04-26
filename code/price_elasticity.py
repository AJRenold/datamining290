from math import log, exp
from scipy.stats import linregress
import re

f = open("price-elasticity.csv",'r')
rows = [ line.strip().split(',') for line in f ]
header = rows[0]
data = rows[1:]

weekday_ids = ['1','2','3','4','5']
weekend_ids = ['6','7']

x = 'demand quantity'
y = 'room price'

weekday_data = [[],[]]
weekend_data = [[],[]]

for row in data:
        if row[0] in weekday_ids:
                weekday_data[0].append(log(float(row[1])))
                weekday_data[1].append(log(float(re.sub(r'\$','',row[2]))))
          
        if row[0] in weekend_ids:
                weekend_data[0].append(log(float(row[1])))
                weekend_data[1].append(log(float(re.sub(r'\$','',row[2]))))
             
# weekday
wd_slope, wd_intercept, wd_r_value, p_value, std_err = linregress(weekday_data[1],weekday_data[0])
print "weekday price elasticity =", wd_slope

# weekend
we_slope, we_intercept, we_r_value, p_value, std_err = linregress(weekend_data[1],weekend_data[0])
print "weekend price elasticity =", we_slope

## forecast based on a given price elasticity (the slope of the linear regression)
## and based on a forecast price, number of rooms demanded and capacity
## this uses the slope for calculating the price elasticity
## increments from %200 to -%200 price change to find the max of P*Q

def forecast(slope,capacity,start_price,start_quantity):
        change_price = 2
        increment = 0.0005
        max_rev = [0,0,0]
        while change_price > -2:
                price = start_price*(1 + change_price)
                quantity = (1+(slope*change_price))*start_quantity
                rev = price*quantity
                if quantity <= capacity:
                        #print rev, price, quantity
                        if rev > max_rev[0]:
                                max_rev = [ rev, price, quantity ]
                change_price -= increment

        return max_rev[1]

## forecast based on the intercept and slope from the linear regression
## uses the function Q = exp(intercept+slope*log(P)) to maximize Q*P incrementing
## from P = 1000 downwards until Q exceeds capacity

def forecast2(intercept, slope, capacity):
    rooms = 0
    max_rev = [0,0,0]
    price = 1000
    while rooms <= capacity:
        rooms = exp(intercept+slope*log(price))
        rev = price * rooms
        if rev > max_rev[0] and rooms <= 1100:
            max_rev = [rev, price, rooms]
        price -= 1
    return max_rev[1]

## weekday price
print "weekday forecast method 1:",forecast(wd_slope,1100,200,1000)
print "weekday forecast method 2:",forecast2(wd_intercept,wd_slope,1100)

## weekend price
print "weekend forecast method 1:",forecast(we_slope,1100,200,1000)
print "weekend forecast method 2:",forecast2(we_intercept,we_slope,1100)
