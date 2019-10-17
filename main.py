# -*- coding: utf-8 -*-

"""  
    reportlab API Package Test
"""

# import reportlabAPI as repf

from reportlabAPI import (build_doc, build_cover, addPageBreak,
                          new_chapter, addSubtitle, build_credits,
                          save_doc, sumarryTable, detailed_Table_df,
                          MSG_COMPLY, MSG_NOT_COMPLY)

import numpy as np
import pandas as pd

title = 'My Title'
desc = 'My Description'

build_doc(title, desc)
print('Building Cover')
build_cover()

new_chapter('Subtitle Tests')

addSubtitle('Subltile 1')

addSubtitle('Subltile 2')

new_chapter('Teste sumarryTable')
    
df1 = pd.DataFrame({4:{1:5, 2:6, 3:7},
                   5:{1:6, 2:'B=Vey', 3:8},
                   6:{1:7, 2:8, 3:9},
                   12:{1:'B=Vey', 2:MSG_NOT_COMPLY, 3:9}})

df2 = pd.DataFrame({9:{1:3, 2:2, 3:MSG_COMPLY},
                    99:{1:4, 2:3, 3:MSG_NOT_COMPLY},
                    999:{1:5, 2:4, 3:MSG_COMPLY},
                   9999:{1:MSG_NOT_COMPLY, 2:MSG_COMPLY, 3:MSG_COMPLY},
                   99989:{1:'vEY', 2:MSG_COMPLY, 3:MSG_COMPLY},
                   15:{1:'vEY', 2:MSG_COMPLY, 3:MSG_COMPLY}})

sumarryTable(df1, df2, master_rows_name=('AAA', 'BBB'))

#%%

def soma2(a,b):
    return a + b

def subt2(a,b):
    return a - b

#%%
    
columns = np.linspace(0,1, 8)
lines = np.linspace(0,.3, 5)

somaTable = []
subtTable = []

for j in lines:
    
    each_line_soma = {}
    each_line_subt = {}
    
    for i in columns:
        res_soma = soma2(i, j)
        res_subt = subt2(i, j)
        
        each_line_soma[i] = res_soma
        each_line_subt[i] = res_subt
    somaTable.append(each_line_soma)
    subtTable.append(each_line_subt)
        
df_soma = pd.DataFrame(somaTable, index=lines)
df_subt = pd.DataFrame(subtTable, index=lines)

max1 = df_soma.max().max() / 2
max2 = df_subt.max().max() / 2

new_chapter('Teste detailed_Table_df')

detailed_Table_df(df_soma, maxValue=max1)
detailed_Table_df(df_subt, maxValue=max2)

#%%
new_chapter('detailed_Table_nocolor')

detailed_Table_df(df_soma, maxValue=max1, mode='no_color')
detailed_Table_df(df_subt, maxValue=max2, mode='no_color')

#%%

new_chapter('detailed_Table_red_limit')

detailed_Table_df(df_soma, maxValue=max1*1.5, minValue=0, mode='red_limit')
detailed_Table_df(df_subt, maxValue=max2*1.5, minValue=0, mode='red_limit')

#%%

new_chapter('detailed_Table_colorful_by_column')

max_thdh = {3: 4, 5: 4, 7: 4, 9: 4, 11: 2, 13: 2, 15: 2, 17: 1.5, 19: 1.5,
            21: 1.5, 23: 0.6, 25: 0.6, 27: 0.6, 29: 0.6, 31: 0.6}

columns = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
indexes = ['0, 0°', '0, 45°', '5, 0°', '5, 45°', '10, 0°', '10, 45°',
           '15, 0°', '15, 45°']
values = [[0.01,  0.2, 0.15, 0.01, 0.09, 0.08, 0.01, 0.06, 0.05, 0.01, 0.04, 0.04],
          [ 0.0,  0.2, 0.15, 0.01, 0.09, 0.08, 0.01, 0.06, 0.05, 0.01, 0.05, 0.04],
          [ 0.0, 1.05, 1.39, 0.0, 1.8, 1.5, 0.0, 0.07, 0.05, 0.01, 0.05, 0.05],
          [0.01,  0.9, 1.48, 0.0, 1.85, 1.47, 0.01, 0.06, 0.05, 0.02, 0.04, 0.04],
          [0.01, 2.09, 2.73, 0.0, 3.56, 3.05, 0.01, 0.07, 0.04, 0.0, 0.04, 0.05],
          [0.01, 1.95, 2.83, 0.0, 3.61, 3.02, 0.0, 0.07, 0.05, 0.02, 0.06, 0.07],
          [0.01, 3.15, 4.09, 0.01, 5.32, 4.61, 0.01, 0.07, 0.06, 0.02, 0.06, 0.05],
          [ 0.0,  3.0, 4.18,  0.0, 5.37, 4.57, 0.01, 0.06, 0.05, 0.01, 0.05, 0.03]
        ] 

df = pd.DataFrame(values, index=indexes, columns=columns)

detailed_Table_df(df, mode='colorful_by_columns', maxValueColumns=max_thdh,
                  corner='        ')    

#%%

members = ['Member 1', 'Member 2', 'Member 3']

acknow = 'This project is the result of an agreement between member 1 and ' + \
    'member 2.'

print('Building Credits')
build_credits(acknow, members)

print('Building All Report')

from webbrowser import open as openf

openf(save_doc('Test_', withDate=True))

#%%


