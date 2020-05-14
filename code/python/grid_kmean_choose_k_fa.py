from process_puz import *

from sklearn.decomposition import FactorAnalysis
from sklearn.cluster import KMeans

import scipy.signal as spsig

from mpl_toolkits.mplot3d import Axes3D

def kmeans_AIC(mod):
    log_L = mod.inertia_
    k = mod.cluster_centers_.shape[0]
    d = mod.cluster_centers_.shape[1]
    return(2*d*k+log_L)

def grid_sqavg(grid,sqdim):
    avgM = np.ones((sqdim,)*2)/(sqdim**2)
    return(spsig.convolve2d(avgM,grid,mode='valid'))

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
    smooth_grids = np.array([grid_sqavg(_,5).flatten() for _ in grids])
    grids = np.array([_.flatten() for _ in grids])

    fa = FactorAnalysis(n_components=3).fit_transform(grids)

    aics = []
    k_vals = range(1,25)
    for k in k_vals:
        print(k)
        km = KMeans(n_clusters=k).fit(fa)
        aics.append(kmeans_AIC(km))

    plt.plot(k_vals,aics)
    plt.xlabel('Number of Clusters (k)',size=16)
    plt.ylabel('Akaike Information Criterion',size=16)
    plt.savefig('grid_aic_fa.png')
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    k_best = np.where(np.array(aics) == np.min(aics))[0][0]
    km_best = KMeans(n_clusters=k_best).fit(fa)
    ax.scatter(fa[:,0],fa[:,1],fa[:,2],c=km_best.labels_)
    plt.show()

