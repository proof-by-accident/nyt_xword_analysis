from process_puz import *

if __name__=='__main__':
    rows = []

    try:
        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'rb') as f:
            clues_df = pickle.load(f)

        with open(os.path.join(PICKLE_DIR,'grids_df.p'),'rb') as f:
            grids_df = pickle.load(f)
    except:
        exec(open(os.path.join(CODE_DIR,'process_puz.py').read()))


    pun_clues = clues_df.loc[clues_df.is_pun_clue]
