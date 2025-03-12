import pandas as pd
import numpy as np
import scipy.stats as stats
from joblib import Parallel, delayed
from statsmodels.stats.multitest import multipletests

class FeaturesSelection:
    
    def __init__(self, data:pd.DataFrame, metadata:pd.DataFrame):
        
        self.data = data
        self.metadata = metadata
        self.stats = None

        
    def row_statistics(self, df):
        
        pct_occurrence = (df.gt(0).sum(axis=1) / df.shape[1])
        mean_values = df.mean(axis=1)
        variance_values = df.var(axis=1)
        
        result_df = pd.DataFrame({
            'pct_occurrence': pct_occurrence,
            'mean': mean_values,
            'variance': variance_values
        }, index=df.index)
        
        return result_df
    
    
    
    def compute_p_value(self, inx, df, df2):
        if np.sum(df.loc[inx, :]) == np.sum(df2.loc[inx, :]):
            return inx, 1.0  
        else:
            _, p = stats.mannwhitneyu(df.loc[inx, :], df2.loc[inx, :])
            return inx, p  
        
    
    def fs(self, pct_set = .95, low_exp = .5, var_perc = .99, min_log = 1.5, min_p_val = 0.01):
        
        
        fdf = self.data.copy()
        
        fdf.columns = self.metadata['names']

        full_stats = pd.DataFrame()
        
        for se in set(fdf.columns):
            df = fdf.loc[:,se]
            dt1 = self.row_statistics(df)
            dt1 = dt1[dt1['pct_occurrence'] >= pct_set]
            dt1 = dt1[dt1['mean'] > np.quantile(dt1['mean'], low_exp)]
            dt1 = dt1[dt1['variance'] <= np.quantile(dt1['variance'], var_perc)]
            df = df.loc[dt1.index,:]
            df2 = fdf.loc[dt1.index, fdf.columns != se]
            
            dt1['p-val'] = None
            
            results = Parallel(n_jobs=-1)(delayed(self.compute_p_value)(inx, df, df2) for inx in dt1.index)
            
            for inx, p in results:
                dt1.at[inx, 'p-val'] = p
                
            dt1['adj_pval'] = multipletests(dt1['p-val'], method='fdr_bh')[1] 
            
            s1 = np.array(dt1['mean'])
            s1_min = np.min(s1[s1 > 0])
            s2 = np.array(df2.mean(axis=1))
            s2_min = np.min(s2[s2 > 0])
            
            s1[s1 == 0] = s1_min / 2
            s2[s2 == 0] = s2_min / 2
            
            dt1['FC'] = s1 / s2
            
            dt1['log(FC)'] = np.log2(dt1['FC'])
            
            dt1 = dt1[dt1['log(FC)'] > min_log]
            
            dt1 = dt1[dt1['adj_pval'] <= min_p_val]

            dt1['set'] = se
            
            dt1['feature'] = dt1.index
                        
            full_stats = pd.concat([full_stats, dt1])
            
        self.stats = full_stats
        return full_stats
    
    
    def select_top(self, top_n = 50, values_q = {'pct_occurrence':False,
                                                           'variance':True,
                                                           'mean':False,
                                                           'FC':False}):
        
        stats_df = self.stats
        
        sets = set(stats_df['set'])
        
        res_df = pd.DataFrame()
        
        for s in sets:
        
            stats_df_tmp = stats_df[stats_df['set'] == s].sort_values(
                by=list(values_q.keys()),  
                ascending=list(values_q.values())  
            ).reset_index(drop = True)
            
            
            
            stats_df_tmp = stats_df_tmp.iloc[list(range(0,top_n)),:]
            
            res_df = pd.concat([res_df, stats_df_tmp])
        
        
        return res_df
               
        
        
            
            
            
            
            

            
   