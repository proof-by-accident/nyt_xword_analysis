from process_puz import *

import spacy
NLP = spacy.load('en_core_web_lg')

import numpy as np

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer

import pyLDAvis
from pyLDAvis import sklearn as sklearn_lda

if __name__ == '__main__':
    try:
        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'rb') as f:
            clues = pickle.load(f)
    except:
        exec(open('./process_puz.py').read())

    try:
       with open(os.path.join(PICKLE_DIR,'lda_fit.p'),'rb') as f:
            pickle.load(f)

    except:
        nclues = clues.shape[0]
        ntext = int(.1*nclues)
        clue_samples = np.random.choice(range(nclues),ntext)

        count_vectorizer = CountVectorizer(stop_words='english')
        data = count_vectorizer.fit_transform(clues.clue_text.iloc[clue_samples])

        number_topics = 4
        lda = LDA(n_components=number_topics, n_jobs=-1)
        lda.fit(data)

        with open(os.path.join(PICKLE_DIR,'lda_fit.p'),'wb') as f:
            pickle.dump(lda,f)

    LDAvis_prepared = sklearn_lda.prepare(lda, data, count_vectorizer)

    with open(os.path.join(PICKLE_DIR,'ldavis.p'), 'wb') as f:
            pickle.dump(LDAvis_prepared, f)

    pyLDAvis.save_html(LDAvis_prepared, './ldavis_prepared_'+ str(number_topics) +'.html')
