#!/usr/bin/env python3

import csv

def filter_candidates_string(query):
    with open('pan.csv', newline='') as f:
        reader = csv.reader(f)
        candidates = [row for row in reader if query in row[2]]
    perfect_matches = [c for c in candidates if c[2] == query]
    if perfect_matches:
        return perfect_matches
    elif candidates:
        return candidates

def filter_candidates_proto(query):
    case_sensitive = not query.islower()
    with open('pan.csv', newline='') as f:
        reader = csv.reader(f)
        if case_sensitive:
            candidates = [row for row in reader if query in row[0]]
        else:
            candidates = [row for row in reader if query in row[0].lower()]
    return candidates

def filter_candidates_wordlist(query):
    wordlist = query.split()
    with open('pan.csv', newline='') as f:
        reader = csv.reader(f)
        candidates = [row for row in reader
                      if any(w in row[2].split()
                             for w in wordlist)]
    return candidates

def display_candidates(cs):
    return [f'PAn **{c[0]}** "{c[2]}" https://www.trussel2.com/acd/{c[1]}'
            for c in cs]

def select_candidates(query):
    if query.startswith('"') and query.endswith('"'):
        candidates = filter_candidates_string(query.strip('"'))
    elif query.startswith('*'):
        candidates = filter_candidates_proto(query.lstrip('*'))
    else:
        candidates = filter_candidates_wordlist(query)

    if candidates:
        return display_candidates(candidates)
    else:
        return ["No matches found!"]
