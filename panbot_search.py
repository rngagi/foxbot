#!/usr/bin/env python3

import csv

pan_file = 'pan.csv'
pmp_file = 'pmp.csv'

def filter_candidates_string(query, db):
    with open(db, newline='') as f:
        reader = csv.reader(f)
        candidates = [row for row in reader if query in row[2]]
    perfect_matches = [c for c in candidates if c[2] == query]
    if perfect_matches:
        return perfect_matches
    elif candidates:
        return candidates

def filter_candidates_proto(query, db):
    case_sensitive = not query.islower()
    with open(db, newline='') as f:
        reader = csv.reader(f)
        if case_sensitive:
            candidates = [row for row in reader if query in row[0]]
        else:
            candidates = [row for row in reader if query in row[0].lower()]
    return candidates

def is_word_in_row(row, wordlist):
    words = [w.strip(",.;:()'") for w in row[2].split()]
    return any(w in words for w in wordlist)

def filter_candidates_wordlist(query, db):
    wordlist = query.split()
    with open(db, newline='') as f:
        reader = csv.reader(f)
        candidates = [row for row in reader
                      if is_word_in_row(row, wordlist)]
    return candidates

def display_candidates(cs, lang):
    if lang == 'pan':
        langstr = 'PAn'
    else:
        langstr = 'PMP'

    return [f'{langstr} **{c[0]}** "{c[2]}" https://www.trussel2.com/acd/{c[1]}'
            for c in cs]

def select_candidates(query, lang):
    if lang == 'pan':
        db = pan_file
    else:
        db = pmp_file

    if query.startswith('"') and query.endswith('"'):
        candidates = filter_candidates_string(query.strip('"'), db)
    elif query.startswith('*'):
        candidates = filter_candidates_proto(query.lstrip('*'), db)
    else:
        candidates = filter_candidates_wordlist(query, db)

    if candidates:
        return display_candidates(candidates, lang)
    else:
        return ["No matches found!"]
