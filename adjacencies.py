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

