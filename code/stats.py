#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from http://www.fec.gov/disclosurep/PDownload.do"""

import fileinput
import csv

total = 0
minimum = 0
maximum = 0
counter = 0
sum_squares = 0
candidates = {}
contributions = []

for row in csv.reader(fileinput.input()):
    if not fileinput.isfirstline():
        ## initialize minmium value
        if total == 0: minimum = float(row[9])

        total += float(row[9])
        ###
        # TODO: calculate other statistics here
        # You may need to store numbers in an array to access them together
        ##/

        ## keep a counter to find mean
	counter += 1

        ## Find Min and Max values
        if float(row[9]) < minimum:
            minimum = float(row[9])
        if float(row[9]) > maximum:
            maximum = float(row[9])

        ## Create list of contributions to get median later
        contributions.append(float(row[9]))

        ## Sum of x^2 to be used calculating standard deviation
        sum_squares += (float(row[9])*float(row[9]))

        ## Track Candidate Values
        if row[2] not in candidates:
            candidates[row[2]] = { 'total': float(row[9]), 'counter': 1, 'min': float(row[9]), \
                 'max': float(row[9]), 'contributions': [float(row[9])], 'sum_squares': (float(row[9])*float(row[9])) }
        else:
            candidates[row[2]]['total'] += float(row[9])
            candidates[row[2]]['counter'] += 1
            candidates[row[2]]['sum_squares'] += (float(row[9])*float(row[9]))
            if candidates[row[2]]['min'] > float(row[9]):
                candidates[row[2]]['min'] = float(row[9])
            if candidates[row[2]]['max'] < float(row[9]):
                candidates[row[2]]['max'] = float(row[9])
            candidates[row[2]]['contributions'].append(float(row[9]))
###
# TODO: aggregate any stored numbers here
#
##/

## calculate mean
mean = total/counter

## calculate median
def median(median_list):
    median_list.sort()
    if len(median_list) % 2 == 1:
        median = median_list[int(len(median_list)/2)-1]
    else:
        median = (median_list[len(median_list)/2] + median_list[(len(median_list)/2)-1])/2

    return median

contributions_median = median(contributions)

## Standard deviation
def standard_deviation(sum_squares,mean,n):
    return ((sum_squares/n)-mean**2)**0.5 

contributions_sd = standard_deviation(sum_squares,mean,counter)

## Candidates median and sd
for candidate,values in candidates.items():
    values['mean'] = values['total']/values['counter']
    values['median'] = median(values['contributions'])
    values['standard_deviation'] = standard_deviation(values['sum_squares'],values['mean'],values['counter'])

##### Print out the stats
print "Total: %s" % total
print "Minimum: %s" % minimum
print "Maximum: %s" % maximum
print "Mean: %s" % mean
print "Median: %s" % contributions_median
# square root can be calculated with N**0.5
print "Standard Deviation: %s" % contributions_sd

##### Comma separated list of unique candidate names
print "Candidates: %s" % candidates.keys()

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    norm = ((value-minimum)/(maximum-minimum))*(1-0)+0
    ###/
    
    return norm

def z_score(value):
    '''Takes a donation amount and returns the z-score normalized value'''

    z_score = (value - mean) / contributions_sd

    return z_score

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
print "z-score normalized values: %r" % map(z_score, [2500, 50, 250, 35, 8, 100, 19])

## print Candidate Stats
for candidate,values in candidates.items():
    print "Candidate: %s" % candidate
    print "Total: %s" % values['total']
    print "Minimum: %s" % values['min']
    print "Maximum: %s" % values['max']
    print "Mean: %s" % values['mean']
    print "Median: %s" % values['median']
    print "Standard Deviation: %s" % values['standard_deviation']
    print "mean normalized: %s" % minmax_normalize(values['mean'])
    print "mean as normalized z_score: %s" % z_score(values['mean']) 
    print

