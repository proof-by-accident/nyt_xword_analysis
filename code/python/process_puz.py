import os
import sys
import pickle
import re
import datetime

import pandas as pd
import matplotlib.pyplot as plt

import puz

import spacy
from spacy import tokenizer

NLP = spacy.load('en_core_web_lg')

BASE_DIR = os.path.abspath('../../')
CODE_DIR = os.path.join(BASE_DIR,'code/python')
PICKLE_DIR = os.path.join(CODE_DIR,'pickles')
DATA_DIR = os.path.join(BASE_DIR,'data')
PUZ_DIR = os.path.join(DATA_DIR,'puz')
PUZ_FILES = [os.path.join(PUZ_DIR,_) for _ in os.listdir(PUZ_DIR)]

def title2date(title):
    pattern = re.compile("[a-z]{,9}\s[0-9]{,2},\s[0-9]{4}")
    title = title.strip().lower()

    try:
        date = pattern.search(title).group(0)
    except:
        return(None)

    try:
        dt = datetime.datetime.strptime(date,'%B %d, %Y')

    except ValueError:
        dt = datetime.datetime.strptime(date,'%b %d, %Y')

    return(dt.strftime('%Y-%m-%d-%a'))


def clues2pandas(fname):
    p = puz.read(fname)
    puzNumber = os.path.splitext(os.path.basename(fname))[0]

    across = p.clue_numbering().across
    down = p.clue_numbering().down

    ret = []

    date = title2date(p.title)

    try:
        date_split= date.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])
        day_name = date_split[3]
    except:
        year = month = day = day_name = 0

    for clue in across:
        row = {'puzzle_number': puzNumber,
               'puzzle_date': date,
               'puzzle_year': year,
               'puzzle_month': month,
               'puzzle_day': day,
               'puzzle_day_name': day_name,
               'clue_number': clue['num'],
               'clue_is_across': True,
               'is_culture_clue': is_culture_clue(clue['clue']),
               'is_pun_clue': is_pun_clue(clue['clue']),
               'clue_text': clue['clue'],
               'answer_length': clue['len'],
               }
        ret.append(row)

    for clue in down:
        row = {'puzzle_number': puzNumber,
               'puzzle_date': date,
               'puzzle_year': year,
               'puzzle_month': month,
               'puzzle_day': day,
               'puzzle_day_name': day_name,
               'clue_number': clue['num'],
               'clue_is_across': False,
               'is_culture_clue': is_culture_clue(clue['clue']),
               'is_pun_clue': is_pun_clue(clue['clue']),
               'clue_text': clue['clue'],
               'answer_length': clue['len'],
               }
        ret.append(row)

    return(pd.DataFrame.from_dict(ret))


def get_scrabble_dict():
    try:
        with open(os.path.join(DATA_DIR,'scrabble/scrabble_dict.p'),'rb') as f:
            scrabble_dict = pickle.load(f)

        return(scrabble_dict)

    except FileNotFoundError:
        print('scrabble_dict file not found, making scrabble_dict. This may take a little while...')
        with open(os.path.join(DATA_DIR,'scrabble/scrabble.txt'),'r') as f:
            scrabble_text = f.read().split('\n')

        scrabble_text.pop(0)
        scrabble_text.pop(0)
        scrabble_text.pop(0)

        scrabble_dict = {}
        for word in scrabble_text:
            first_letter = word[0]

            if first_letter in scrabble_dict:
                scrabble_dict[first_letter].append(word)

            else:
                scrabble_dict[first_letter] = [word]

        with open(os.path.join(DATA_DIR,'scrabble/scrabble_dict.p'),'wb') as f:
            pickle.dump(scrabble_dict,f)

        return(scrabble_dict)


def is_culture_clue(clue):
    clue_toks = NLP(clue)
    for tok in clue_toks:
        if tok.pos_ == 'PROPN':
            return True

        else:
            pass

    return False

def is_pun_clue(clue):
    try:
        return(clue[-1]=='?')
    except:
        return(False)


if __name__=='__main__':
    try:
        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'rb') as f:
            clues = pickle.load(f)
    except:
        dfs = []
        barMax = len(PUZ_FILES)
        barWidth=0.
        progbar = str(round(100*barWidth/barMax)) + '%'
        sys.stdout.write(progbar)
        sys.stdout.flush()
        sys.stdout.write("\b"*len(progbar))
        for fn in PUZ_FILES:
            try:
                dfs.append(clues2pandas(fn))
            except Exception as e:
                print(e)
                print(fn)
                assert False

            barWidth += 1
            progbar = str(round(100*barWidth/barMax)) + '%'
            sys.stdout.write(progbar)
            sys.stdout.flush()
            sys.stdout.write("\b"*len(progbar))

        clues = pd.concat(dfs)

        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'wb') as f:
            pickle.dump(clues,f)

        clues.to_csv(os.path.join(DATA_DIR,'clues.csv'))


