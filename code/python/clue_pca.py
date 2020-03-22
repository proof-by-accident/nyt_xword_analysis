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
            with open(os.path.join(PICKLE_DIR,'clue_wordrembeddings.p'),'rb'):
                pickle.load(f)

        except:
            nclues = clues.shape[0]
            ntext = int(.01*nclues)

            clue_samps = np.random.choice(range(nclues),ntext)
            clues_text = list(clues.clue_text.iloc[clue_samps])

            words = []

            done = 0
            out = str(done) + '/' + str(ntext)
            sys.stdout.write(out)
            sys.stdout.flush
            sys.stdout.write('\b'*len(out))

            for t in clues_text:
                tok = NLP(t)
                new_words = [_ for _ in tok if not(_.is_stop) and not (_.is_punct)]
                words += new_words

                out = str(done) + '/' + str(ntext)

                if (done%500) == 0:
                    sys.stdout.write(out)
                    sys.stdout.flush()
                    sys.stdout.write('\b'*len(out))
                done += 1

            dims = 300
            nrows = len(words)
            clue_word_embeddings = np.zeros((nrows,dims))

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
