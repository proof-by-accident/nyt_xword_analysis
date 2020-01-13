import os
import sys
import pickle
import re
import datetime

import pandas as pd
import matplotlib.pyplot as plt

import puz

import spacy

BASE_DIR = os.path.abspath('../../')
CODE_DIR = os.path.join(BASE_DIR,'code/python')
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
        year = month = day = day_name = None

    for clue in across:
        row = {'puzzle_number': puzNumber,
               'puzzle_date': date,
               'puzzle_year': year,
               'puzzle_month': month,
               'puzzle_day': day,
               'puzzle_day_name': day_name,
               'clue_number': clue['num'],
               'clue_is_across': True,
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
               'clue_text': clue['clue'],
               'answer_length': clue['len'],
               }
        ret.append(row)

    return(pd.DataFrame.from_dict(ret))

if __name__=='__main__':
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
    with open(os.path.join(CODE_DIR,'clues_df.p'),'wb') as f:
        pickle.dump(clues,f)


