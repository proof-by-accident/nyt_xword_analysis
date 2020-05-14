from process_puz import *

from sklearn.decomposition import FactorAnalysis
from sklearn.cluster import KMeans

def kmeans_AIC(mod):
    log_L = mod.inertia_
    k = mod.cluster_centers_.shape[0]
    d = mod.cluster_centers_.shape[1]
    return(2*d*k+log_L)

if __name__=='__main__':
    rows = []

    try:
        with open(os.path.join(PICKLE_DIR,'clues_df.p'),'rb') as f:
            clues_df = pickle.load(f)

        with open(os.path.join(PICKLE_DIR,'grids_df.p'),'rb') as f:
            grids_df = pickle.load(f)
    except:
        exec(open(os.path.join(CODE_DIR,'process_puz.py').read()))

    day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']#,'Sunday']
    grids = grids_df.grid.loc[[_ in day_names for _ in grids_df.day_name]]
    grids = np.array(list(grids))[:,:15,:15]
    grids = np.array([_.flatten() for _ in grids])

    fa = FactorAnalysis(n_components=3).fit_transform(grids)
    km = KMeans(n_clusters=6).fit(fa)

    lab_grids = []
    for l in np.unique(km.labels_):
        lgs = grids[km.labels_==l,:]
        n = lgs.shape[0]
        lab_grids.append(lgs.reshape(n,15,15))

    fig,ax = plt.subplots(nrows=2,ncols=3)
    ax = ax.flatten()
    for a,g,n in zip(ax,lab_grids,km.labels_):
        a.imshow(g[:,:15,:15].mean(0))
        a.set_title(n)
        a.axis('off')

    plt.show()
