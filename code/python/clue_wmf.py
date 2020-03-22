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
       with open(os.path.join(PICKLE_DIR,'token_counts.p'),'rb') as f:
            data = pickle.load(f)

    except:
        count_vectorizer = CountVectorizer(stop_words='english')
        data = count_vectorizer.fit_transform(clues.clue_text)

        with open(os.path.join(PICKLE_DIR,'token_counts.p'),'wb') as f:
            pickle.dump(data,f)

    nmf = NMF(n_components=10)
    Q = nmf.fit_transform(data).T # columns of Q are latent representations of clues
    P = nmf.components_ # columns of P are latent representations of words

    Q_cov = np.dot(Q.T,Q)
    clue_pca = np.linalg.svd(Q_cov)
    cutoff = [sum(clue_pca[1][:i])/sum(clue_pca[1]) for i in range(20)]
    cutoff = np.min(np.where(np.array(cutoff)>.99))
    pcs = clue_pca[0][:,:cutoff]

    proj1 = np.dot(pcs[:,0],Q_samp.T)
    proj2 = np.dot(pcs[:,1],Q_samp.T)
    proj3 = np.dot(pcs[:,2],Q_samp.T)

    kmeans = KMeans(n_clusters=6, random_state=0).fit(np.array([proj1,proj2]).T)
    clues.insert(clues.shape[-1],'cluster',kmeans.labels_)

    cluster0 = clues.clue_text[clues.cluster==0]
    data = CountVectorizer(stop_words='english').fit_transform(cluster0)
    nmf = NMF(n_components=30)
    Q0 = nmf.fit_transform(data)

    Q0_cov = np.dot(Q0.T,Q0)
    clue_pca0 = np.linalg.svd(Q0_cov)
    cutoff0 = [sum(clue_pca0[1][:i])/sum(clue_pca0[1]) for i in range(30)]
    cutoff0 = np.min(np.where(np.array(cutoff0)>.95))
    pcs0 = clue_pca0[0][:,:cutoff]

    proj1 = np.dot(pcs0[:,0],Q0.T)
    proj2 = np.dot(pcs0[:,1],Q0.T)
    proj3 = np.dot(pcs0[:,2],Q0.T)

    kmeans0 = KMeans(n_clusters=3, random_state=0).fit(np.array([proj1,proj2]).T)

    clues0 = clues.loc[clues.cluster==0]
    clues0.insert(clues0.shape[-1],'cluster0',kmeans0.labels_)
