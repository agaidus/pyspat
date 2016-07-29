import pandas as pd

def read_coda(index, chain_1, chain_2, thin_factor=None, use_vars=None):
    index_df=pd.read_csv(index,sep='\t',header=None,names=['var','start','end']).set_index('var')
    if use_vars:
        index_df=index_df.loc[use_vars]
    posteriors=pd.DataFrame()
    for num,codafile in enumerate([chain_1,chain_2],1):
        coda=pd.read_csv(codafile,sep='\t',header=None,names=['iteration','value'])
        single_chain=pd.DataFrame(index=coda.iteration.unique())
        single_chain.index.name='iteration'
        for i,var in index_df.iterrows():
            z=coda.loc[var['start']-1:var['end']-1].set_index('iteration')['value']
            z.name=i
            single_chain=single_chain.join(z)
        if thin_factor:
            single_chain=single_chain.iloc[::thin_factor, :]
        single_chain['chain']=num
        single_chain.set_index('chain',append=True,inplace=True)
        posteriors=posteriors.append(single_chain)
    posteriors=posteriors.sortlevel(level=['iteration','chain'])
    return posteriors






    
import pysal as ps
import os

def calc_shp_adjacencies(shp, sort_id=None):

    if sort_id:
        adj=ps.queen_from_shapefile(shp,sort_id)
    else:
        adj=ps.queen_from_shapefile(shp)
    sort_order=sorted(adj.id_order)
    
    neigh_dict=adj.neighbors
    
    neigh_list_nest=[neigh_dict[i] for i in sort_order]
    neigh_list_flat=[k for sub in neigh_list_nest for k in sorted(sub)]
    
    neigh_id_list=[sort_order.index(X)+1 for X in neigh_list_flat]

    num_neigh_list=[len(x) for x in neigh_list_nest]
    
    return {'num_neigh':num_neigh_list, 'neigh_id':neigh_id_list,'shp':shp}

def write_adjacencies(adj,outfolder=None):
    if not outfolder:
        outfolder=os.path.dirname(adj['shp'])
    f=open(outfolder+'/num.txt', 'w')
    f.write(str(adj['num_neigh'])[1:-1])
    f.close()

    f=open(outfolder+'/adj.txt', 'w')
    f.write(str(adj['neigh_id'])[1:-1])
    f.close()
