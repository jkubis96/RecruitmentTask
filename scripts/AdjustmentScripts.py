# scripts necessery for data adjustment and normalization in recruitment task
import pandas as pd
import numpy as np

class DataAdj:
    
    def __init__(self, transcripts_meta:pd.DataFrame):
       
        if {'id', 'len'}.issubset(transcripts_meta.columns):
            self.transcripts_meta = transcripts_meta

        else:
            raise ValueError("Invalid 'transcripts_meta' - It must contain 'id' (e.g., gene_name, gene_id) and 'len' (sequence length) columns!")

    
    
    def compare_data(self, set1, set2):
        return set(set1) - set(set2)
        
     
    def reduce_data(self, data):
        missing_ids = self.compare_data(set1=data.index , set2=self.transcripts_meta['id'])
        return data.loc[data.index.difference(missing_ids)] 
        
        
    def normalize_tpm(self, counts_data:pd.DataFrame, log_adj = True):
        
        counts_data_reduced = self.reduce_data(counts_data)
        
                
        # Add transcript len
        merged = counts_data_reduced.merge(self.transcripts_meta[['id', 'len']], left_index=True, right_on='id', how='left').set_index('id')
        
        # Convert base --> kb
        merged['len'] = merged['len'] / 1000
        
        # Normalization RPK (rm len col)
        RPK_matrix = merged.iloc[:, :-1].div(merged['len'], axis=0)
        
        # TPM
        scaling_factor = RPK_matrix.sum(axis=0) / 1e6
        TPM_matrix = RPK_matrix.div(scaling_factor, axis=1)
        
        # log2
        if log_adj:
            TPM_matrix = np.log2(TPM_matrix + 1)
        
      
        
        return TPM_matrix
    
    
    def data_concat(self, data_list:dict):
        
        if len(data_list.keys()) > 1:
            
            
            result = pd.concat(list(data_list.values()), axis=1).fillna(0)
            
            colnames = []
            names = []

            for n, i in enumerate(data_list.values()): 
                colnames += list(i.columns)
                names += [list(data_list.keys())[n]]*len(i.columns)
                
                metadata = pd.DataFrame({'colnames':colnames, 'names':names})
            
            return result, metadata
                
        else:
            
            raise ValueError('Nothing to concatenate!')
            
   
