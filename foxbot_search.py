#!/usr/bin/env python3

import csv

sdq_file = 'sdq.csv'

def filter_candidates_zh(query, db):
    with open(db, newline='') as f:
        reader = csv.reader(f)
        candidates = [row for row in reader if query in row[1]]
    perfect_matches = [c for c in candidates if c[1] == query]
    if perfect_matches:
        return perfect_matches
    elif candidates:
        return candidates

def filter_candidates_word(query, db):
    case_sensitive = not query.islower()
    with open(db, newline='') as f:
        reader = csv.reader(f)
        if case_sensitive:
            candidates = [row for row in reader if query in row[0]]
        else:
            candidates = [row for row in reader if query in row[0].lower()]
    return candidates

def is_word_in_row(row, wordlist):
    words = [w.strip(",.;:()'") for w in row[1].split()]
    return any(w in words for w in wordlist)

def filter_candidates_wordlist(query, db):
    wordlist = query.split()
    with open(db, newline='') as f:
        reader = csv.reader(f)
        candidates = [row for row in reader
                      if is_word_in_row(row, wordlist)]
    return candidates

def display_candidates(cs, lang):
    if lang == 'sdq':
        langstr = 'Seediq'
    # else:
    #     langstr = 'PMP'
	#
    return [f'{langstr} **\{c[0]}** "{c[1]}"'
            for c in cs]

def select_candidates(query, lang):
    if lang == 'sdq':
        db = sdq_file
    # else:
    #     db = pmp_file

    if query.startswith('^[a-z0-9^éṟɨʉ’]+$/i') and query.endswith('^[a-z0-9^éṟɨʉ’]+$/i'):
        candidates = filter_candidates_zh(query.strip('"'), db)
    else:
        candidates = filter_candidates_wordlist(query, db)

    if candidates:
        return display_candidates(candidates, lang)
    else:
        return ["No matches found!"]
