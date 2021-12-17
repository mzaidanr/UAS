import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from fileHandler import csvHandler,jsonHandler
from PIL import Image

jh_ = jsonHandler('kode_negara_lengkap.json')
dfJ = jh_.dataFrame
ch_ = csvHandler('produksi_minyak_mentah.csv')
dfC = ch_.dataFrame

#Additional Info
st.title('Analisis Produksi Minyak Mentah Dunia')
st.sidebar.write('Creator Info : Muhammad Zaidan R / 12220011')
image = Image.open('logoitb.png')
st.sidebar.image(image)

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

dfC = dfC[dfC['tahun']==T]
kode_negara = dfC[dfC['tahun']==T]['kode_negara'].tolist()
produksi_1 = dfC[dfC['tahun']==T]['produksi'].tolist()

maks_produksi = []
negara_tiaptahun = []

kode_negara = list(dict.fromkeys(kode_negara))
for kode in kode_negara:
    try:
        produksi_1 = dfC[dfC['kode_negara']==kode]['produksi'].tolist()
        negara = dfJ[dfJ['alpha-3']==kode]['name'].tolist()[0]
        maks_produksi.append(max(produksi_1))
        negara_tiaptahun.append(negara)
    except:
        continue
        
dic = {'negara':negara_tiaptahun,'produksi_maks':maks_produksi}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values('produksi_maks',ascending=False).reset_index()

plt.title('{B} Negara dengan Produksi Terbesar pada Tahun {T}'.format(B=B,T=T))
plt.bar(df__['negara'][:B],df__['produksi_maks'][:B],width=0.5, bottom=None, align="center",
            color="cyan", data=None, zorder=3)
plt.grid(True, color="blue", linewidth="0.7", linestyle="-.", zorder=0)
plt.xlabel('Negara')
plt.ylabel('Banyaknya Produksi')
plt.show()
st.pyplot(plt)

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

c1, c2, c3, c4 = st.columns(4)
col1, col2, col3, col4 = st.columns(4)

dfb = dfC.loc[dfC['tahun'] == tahun]
dfb = dfb.sort_values(by='produksi', ascending = False)

#Maksimum
jumlah_produksi = dfb[:1].iloc[0]['produksi']
kode_negara = dfb[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""

for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_negara:
        nama_negara = list(dfJ['name'])[i]
        region_negara = list(dfJ['region'])[i]
        subregion_negara = list(dfJ['sub-region'])[i]
        
c1.write('Negara dengan Produksi Terbesar')
col1.write(jumlah_produksi)
col1.write(kode_negara)
col1.write(nama_negara)
col1.write(region_negara)
col1.write(subregion_negara)

jumlah_produksi = dk[:1].iloc[0]['kumulatif']
kode_negara = dk[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""

for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_negara:
        nama_negara = list(dfJ['name'])[i]
        region_negara = list(dfJ['region'])[i]
        subregion_negara = list(dfJ['sub-region'])[i]
        
c2.write('Negara dengan Produksi Terbesar pada Keseluruhan Tahun')
col2.write(jumlah_produksi)
col2.write(kode_negara)
col2.write(nama_negara)
col2.write(region_negara)
col2.write(subregion_negara)


#Minimum tak 0
dfterkecil = dfb[dfb.produksi !=0]
dfterkecil = dfterkecil.sort_values(by=['produksi'],ascending=True)
jumlah_produksi = dfterkecil[:1].iloc[0]['produksi']
kode_negara = dfterkecil[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""
                                    
for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_negara:
        nama_negara = list(dfJ['name'])[i]
        region_negara = list(dfJ['region'])[i]
        subregion_negara = list(dfJ['sub-region'])[i]
                                    
c3.write('Negara dengan Produksi Terkecil')
col3.write(jumlah_produksi)
col3.write(kode_negara)
col3.write(nama_negara)
col3.write(region_negara)
col3.write(subregion_negara)

dfakumulatifmin=dk[dk.kumulatif !=0]
dfakumulatifmin = dfakumulatifmin[:1].sort_values(by=['kumulatif'], ascending = True)
jumlah_produksi = dfakumulatifmin[:1].iloc[0]['kumulatif']
kode_negara = dfakumulatifmin[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""
                                                
for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_negara:
        nama_negara = list(dfJ['name'])[i]
        region_negara = list(dfJ['region'])[i]
        subregion_negara = list(dfJ['sub-region'])[i]


c4.write('Negara dengan Produksi Terkecil Pada Keseluruhan Tahun')
col4.write(jumlah_produksi)
col4.write(kode_negara)
col4.write(nama_negara)
col4.write(region_negara)
col4.write(subregion_negara)
 

#Nol
dfproduksinol = dfb[dfb.produksi == 0]
listnegaranol = []
listregionol = []
listsubregionol = []

for i in range(len(dfproduksinol)):
    for j in range(len(dfJ)):
        if list (dfproduksinol['kode_negara'])[i] == list(dfJ['alpha-3'])[j]:
            listnegaranol.append(list(dfJ['name'])[j])
            listregionol.append(list(dfJ['region'])[j])
            listsubregionol.append(list(dfJ['sub-region'])[j])

dfproduksinol['negara'] = listnegaranol
dfproduksinol['region'] = listregionol
dfproduksinol['sub-region'] = listsubregionol
 
                                                        
dfproduksikumulatifnol = dfb[dfb.produksi == 0]
listnegarakumulatifnol = []
listregionkumulatifnol = []
listsubregionkumulatifnol = []

for i in range(len(dfproduksikumulatifnol)):
    for j in range(len(dfJ)):
        if list (dfproduksikumulatifnol['kode_negara'])[i] == list(dfJ['alpha-3'])[j]:
            listnegarakumulatifnol.append(list(dfJ['name'])[j])
            listregionkumulatifnol.append(list(dfJ['region'])[j])
            listsubregionkumulatifnol.append(list(dfJ['sub-region'])[j])

dfproduksikumulatifnol['negara'] = listnegarakumulatifnol
dfproduksikumulatifnol['region'] = listregionkumulatifnol
dfproduksikumulatifnol['sub-region'] = listsubregionkumulatifnol   
                                                      
st.write(dfproduksinol)
st.write(dfproduksikumulatifnol)
