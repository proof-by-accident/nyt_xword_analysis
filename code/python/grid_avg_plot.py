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

    day_grids = []
    day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for day in day_names:
        grids = grids_df.loc[(grids_df.day_name==day) & (grids_df.year>2015)].grid
        grids = np.array(list(grids))
        day_grids.append(grids)

    fig,ax = plt.subplots(nrows=2,ncols=3)
    ax = ax.flatten()
    for a,g,n in zip(ax,day_grids,day_names):
        a.imshow(g[:,:15,:15].mean(0))
        a.set_title(n)
        a.axis('off')

    plt.show()
