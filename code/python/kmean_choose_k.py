
from process_puz import *

import numpy as np

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

def kmeans_AIC(mod):
    log_L = mod.inertia_
    k = mod.cluster_centers_.shape[0]
    d = mod.cluster_centers_.shape[1]
    return(2*d*k+log_L)

if __name__ == '__main__':
    try:
        with open(os.path.join(PICKLE_DIR,'word_clue_factors.p'),'rb') as f:
            Q,P = pickle.load(f)

    except:
        exec(open(os.path.join(CODE_DIR,'clue_wmf.py')).read())


    aics = []
    k_vals = range(1,20)
    for k in kvals:
        print(k)
        km = KMeans(n_clusters=k, random_state=0).fit(Q.T)
        aics.append(kmeans_AIC(km))

plt.plot(k_vals,aics)
plt.xlabel('Number of Clusters (k)',size=16)
plt.ylabel('Akaike Information Criterion',size=16)
plt.savefig('aic.png')
plt.close()
