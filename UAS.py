import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from fileHandler import csvHandler,jsonHandler

jh_ = jsonHandler('kode_negara_lengkap.json')
dfJ = jh_.dataFrame
ch_ = csvHandler('produksi_minyak_mentah.csv')
dfC = ch_.dataFrame

#Bagian A
st.sidebar.title('Pilihan Pengaturan')
left_col, mid_col, right_col = st.columns(3)

name_negara = dfJ['name'].tolist()

negara = st.sidebar.selectbox('Pilih Negara : ', name_negara)

kode_negara = dfJ[dfJ['name']==negara]['alpha-3'].tolist()[0] 
N = kode_negara
tahun = dfC[dfC['kode_negara']==N]['tahun'].tolist()
produksi = dfC[dfC['kode_negara']==N]['produksi'].tolist()

dic = {'tahun':tahun,'produksi':produksi}
df_ = pd.DataFrame(dic)
dfJ['alpha-3'][243]

st.write('Grafik Produksi Minyak Negara', negara)

plt.title('Produksi Tahunan Negara {}'.format(negara))
plt.plot(tahun,produksi,label='Nilai Produksi')
plt.xlabel('Tahun')
plt.ylabel('Produksi')
plt.legend()
st.pyplot(plt)

#Bagian B
st.write('Grafik Negara dengan Produksi Terbesar')

st.sidebar.write('Pengaturan Produksi Negara per Tahun')
T = st.sidebar.number_input("Pilih Tahun produksi", min_value=1971, max_value=2015)
B = st.sidebar.number_input("Pilih Banyak Negara", min_value=1, max_value=None, value=3)

lcol, rcol = st.columns(2)
lcol.write('Negara dengan Produksi Terbesar')

dfb = dfC.loc[dfC['tahun'] == tahun]
dfb = dfb.sort_values(by='produksi', ascending = False)
dfbaru = dfb[:B]
lcol.write(dfbaru)

dfbaru.plot.bar(x='kode_negara', y='produksi')
plt.show()
rcol.pyplot(plt)

#Bagian C

st.write('Grafik Negara dengan Produksi Kumulatif Terbesar')
st.sidebar.write('Pengaturan Produksi Negara per Tahun')
B = st.sidebar.number_input("Pilih Banyak Negara", min_value=1, max_value=None)

list_ngr = []
kmltf = []

for i in list (dfC['kode_negara']) :
    if i not in list_ngr:
        list_ngr.append(i)
        
for i in list_ngr :
    a=dfC.loc[dfC['kode_negara'] ==i,'produksi'].sum()
    kmltf.append(a)
    
dk = pd.DataFrame(list(zip(list_ngr,kmltf)), columns = ['kode_negara','kumulatif'])
dk = dk.sort_values(by=['kumulatif'], ascending = False)
dk = dk[:B]

dk.plot.bar(x='kode_negara', y='kumulatif') 
plt.show()
st.pyplot(plt)

#Bagian D
'''
T = st.sidebar.number_input("Pilih Tahun produksi", min_value=1971, max_value=2015)

tahun = list(dict.fromkeys(dfC['tahun'].tolist()))

dic_maks = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_min = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_zero = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}

for t in tahun:
    dfC_per_tahun = dfC[dfC['tahun']==t]
    produksi = np.array(dfC_per_tahun['produksi'].tolist())
    maks_prod = max(produksi)
    min_prod = min([p for p in produksi if p != 0])
    zero_prod = min([p for p in produksi if p == 0])
    # maksimum
    kode_negara = dfC_per_tahun[dfC_per_tahun['produksi']==maks_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_maks['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_maks['kode_negara'].append(kode_negara)
    dic_maks['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_maks['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_maks['produksi'].append(maks_prod)
    # minimum != 0
    kode_negara = dfC_per_tahun[dfC_per_tahun['produksi']==min_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_min['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_min['kode_negara'].append(kode_negara)
    dic_min['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_min['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_min['produksi'].append(min_prod)
    # zero == 0
    kode_negara = dfC_per_tahun[dfC_per_tahun['produksi']==zero_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_zero['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_zero['kode_negara'].append(kode_negara)
    dic_zero['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_zero['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_zero['produksi'].append(zero_prod)

df_maks = pd.DataFrame(dic_maks)
df_min = pd.DataFrame(dic_min)
df_zero = pd.DataFrame(dic_zero)
'''
