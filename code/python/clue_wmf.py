from process_puz import *

import spacy

import numpy as np

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def cos_dot(x,y):
    if np.linalg.norm(x) == 0:
        return(0.)

    elif np.linalg.norm(y) == 0:
        return(0.)

    else:
        return(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)))

if __name__ == '__main__':
    try:
        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'rb') as f:
            clues = pickle.load(f)
    except:
        exec(open('./process_puz.py').read())

    try:
       with open(os.path.join(PICKLE_DIR,'word_clue_matrix.p'),'rb') as f:
            data = pickle.load(f)

    except:
        count_vectorizer = CountVectorizer(stop_words='english')
        data = count_vectorizer.fit_transform(clues.clue_text_clean)

        with open(os.path.join(PICKLE_DIR,'word_clue_matrix.p'),'wb') as f:
            pickle.dump(data,f)

    nmf = NMF(n_components=10)
    Q = nmf.fit_transform(data).T # columns of Q are latent representations of clues
    P = nmf.components_ # columns of P are latent representations of words

    kmeans = KMeans(n_clusters=20, random_state=0).fit(Q.T)
    clues.insert(clues.shape[-1],'cluster',kmeans.labels_)

    with open(os.path.join(PICKLE_DIR,'clues_df_clusts.p'),'wb') as f:
        pickle.dump(clues,f)

    clues.to_csv(os.path.join(DATA_DIR,'clues_df_clusts.csv'))

