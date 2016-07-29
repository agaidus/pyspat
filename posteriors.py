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
            z=coda.loc[var['start']:var['end']].set_index('iteration')['value']
            z.name=i
            single_chain=single_chain.join(z)
        if thin_factor:
            single_chain=single_chain.iloc[::thin_factor, :]
        single_chain['chain']=num
        single_chain.set_index('chain',append=True,inplace=True)
        posteriors=posteriors.append(single_chain)
    posteriors=posteriors.sortlevel(level=['iteration','chain'])
    return posteriors
    
