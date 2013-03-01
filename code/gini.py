#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
from itertools import islice
from collections import defaultdict, Counter

(cmte_id, cand_id, cand_nm, contbr_nm, contbr_city, contbr_st, contbr_zip,
contbr_employer, contbr_occupation, contb_receipt_amt, contb_receipt_dt,
receipt_desc, memo_cd, memo_text, form_tp, file_num, tran_id, election_tp) = range(18)


############### Set up variables
# TODO: declare datastructures

############### Read through files

candidates = Counter(defaultdict(int))
candidates_by_zip = defaultdict(Counter)
contributions = []

for row in islice(csv.reader(fileinput.input()),None):
    if not fileinput.isfirstline():
        ###
        # TODO: replace line below with steps to save information to calculate
        # Gini Index
        candidates[row[cand_nm]] += 1
        candidates['total'] += 1
        candidates_by_zip[str(row[contbr_zip])[:5]][row[cand_nm]] += 1
        candidates_by_zip[str(row[contbr_zip])[:5]]['total'] += 1
        contributions.append((float(row[contb_receipt_amt]),row[cand_nm]))

        ##/

###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class
split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code
##/

def calc_weighted_gini(dict_of_counter_dict,total):
    """accepts a dict with any key and values as Counter objects
    with key['total'] as sum of all values in Counter. Arguement total is
    the length of the entire dataset"""
    weighted_gini = 0
    for item in dict_of_counter_dict.values():
        gini = calc_gini(item)
        weighted_gini += gini*(float(item['total'])/float(total))

    return weighted_gini

def calc_gini(counter_dict,total=None):
    """accepts a dict with values as count of each key
    and with 'total' as sum of all values"""

    sum_freq_sq = 0
    for item, freq in counter_dict.iteritems():
        if item != 'total':
            sum_freq_sq += (float(freq)/float(counter_dict['total']))**2
    return 1 - sum_freq_sq


def best_split_cont(cont_field_list):
    """
    accepts a list of tuples (continuous_field, candidate_name)
    and returns best split on the continuous field
    Uses a binary search like methodology for efficiency
    """
    cont_field_list.sort()
    best_gini = [1,0]
    tot_len = float(len(cont_field_list))
    pointer = int(tot_len/2)
    half = int(tot_len/2)

    while half > 1:
        bottom_len = float(len(cont_field_list[:pointer]))
        top_len = float(len(cont_field_list[pointer+1:]))

        cand_bottom = Counter([ i[1] for i in cont_field_list[:pointer] ])
        cand_bottom['total'] = bottom_len

        cand_top = Counter([ i[1] for i in cont_field_list[pointer+1:]])
        cand_top['total'] = top_len

        gini_bottom = calc_gini(cand_bottom,bottom_len)
        gini_top = calc_gini(cand_top,top_len)

        gini = calc_weighted_gini({ 'bottom': cand_bottom, 'top': cand_top }, tot_len )

        if gini > best_gini[0]:
            #print pointer, gini, best_gini, "moving down"
            pointer -= half
        if gini < best_gini[0]:
            #print pointer, gini, best_gini, "moving up"
            best_gini = [gini,pointer]
            pointer += half

        half = int(half/2)

    return best_gini 

gini = calc_gini(candidates)
split_gini = calc_weighted_gini(candidates_by_zip,candidates['total'])
split_cont = best_split_cont(contributions)

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
print "Best split on contributions attribute: ${0} at  location: {1}".format(\
    contributions[split_cont[1]][0], split_cont[1])
print "Gini after best split: {0}".format(split_cont[0])
