from process_puz import *

import spacy
NLP = spacy.load('en_core_web_lg')

import numpy as np

from sklearn.decomposition import PCA

def doc_avg_proj(doc,proj):
    tok = 1

if __name__ == '__main__':
    try:
        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'rb') as f:
            clues = pickle.load(f)
    except:
        exec(open('./process_puz.py').read())

    try:
        with open(os.path.join(PICKLE_DIR,'pca_fit.p'),'rb') as f:
            pickle.load(f)

    except:
        try:
            with open(os.path.join(PICKLE_DIR,'clue_word_embeddings.p'),'rb'):
                pickle.load(f)

        except:
            words = []
            done = 0
            tot = len(clues.clue_text)
            out = str(done) + '/' + str(tot)
            sys.stdout.write(out)
            sys.stdout.flush
            sys.stdout.write('\b'*len(out))
            for t in clues.clue_text:
                tok = NLP(t)
                new_words = [_ for _ in tok if not(_.is_stop) and not (_.is_punct)]
                words += new_words

                out = str(done) + '/' + str(tot)

                if (done%500) == 0:
                    sys.stdout.write(out)
                    sys.stdout.flush()
                    sys.stdout.write('\b'*len(out))
                done += 1

            dims = 300
            #nrows = len(words)
            nrows = 100000
            clue_word_embeddings = np.zeros((nrows,dims))
            word_samps = np.random.choice(range(len(words)),nrows)

            j = 0
            for i in word_samps:
                clue_word_embeddings[j,:] = words[i].vector
                j += 1

            with open(os.path.join(PICKLE_DIR,'clue_word_embeddings.p'),'wb'):
                pickle.dump(clue_word_embeddings,f)

    pca = PCA(n_components=20)
    pca.fit(clue_word_embeddings)

    pc1 = pca.components_[0,:]
    pc2 = pca.components_[1,:]

    word_projections = pd.DataFrame.from_dict(
        {'proj1': list(np.dot(clue_word_embeddings,pc1)),
         'proj2': list(np.dot(clue_word_embeddings,pc2)),
         'word': [words[i] for i in word_samps]}
    )
