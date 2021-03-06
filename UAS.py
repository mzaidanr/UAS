#Import Module
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import cm 
import streamlit as st
from fileHandler import csvHandler,jsonHandler
from PIL import Image

#Additional Info
st.sidebar.write('Creator Info : Muhammad Zaidan R / 12220011') 
image = Image.open('logoitb.png')
st.sidebar.image(image)
st.sidebar.title("Menu Pilihan")
st.sidebar.header('Pengaturan Jumlah Produksi tiap Tahun')

#Read json
with open("kode_negara_lengkap.json", "r") as rfile:
    data = json.load(rfile)
# for i in data:
#     print(type(i))
print(data[0])
dfJ = pd.DataFrame(data)

#Read csv
csv = pd.read_csv("produksi_minyak_mentah.csv")
df = pd.DataFrame(csv)
print(df)

#Mengubah mjd Data Frame 
st.title('Analisis Data Produksi Minyak Mentah Dunia')
ch_ = csvHandler('produksi_minyak_mentah.csv')
jh_ = jsonHandler('kode_negara_lengkap.json')
dfC = ch_.dataFrame
dfJ = jh_.dataFrame
nama_ngr = dfJ['name'].tolist()

kode_kumpulanngr = []
for i in list(dfC['kode_negara']) :
    if i not in list(dfJ['alpha-3']) :
        kode_kumpulanngr.append(i)

for i in kode_kumpulanngr :
    dfC = dfC[dfC.kode_negara != i]
print(dfC)


#Bagian A

st.header("Data Produksi suatu Negara ")
left_col, right_col = st.columns(2)
negara = st.sidebar.selectbox('Pilih negara : ',nama_ngr) 

kode = dfJ[dfJ['name']==negara]['alpha-3'].tolist()[0]

st.sidebar.write('Kode Negara : ', kode)

df['produksi'] = df['produksi'].astype(str).str.replace(".", "", regex=True).astype(float)
df['produksi'] =df['produksi'].astype(str).str.replace(",", "", regex=True).astype(float)
df['produksi'] = pd.to_numeric(df['produksi'], errors='coerce')

df2 = pd.DataFrame(df,columns= ['kode_negara','tahun','produksi'])
df2=df2.loc[df2['kode_negara']==kode]
df2['produksi'] = pd.to_numeric(df2['produksi'], errors='coerce')

left_col.write(df2)

fig, ax = plt.subplots()
ax.plot(df2['tahun'], df2['produksi'], label = df2['tahun'], color='blue')
ax.set_title("Jumlah Produksi per Tahun di Negara {A} ".format(A=negara))
ax.set_xlabel("Tahun", fontsize = 11)
ax.set_ylabel("Jumlah Produksi", fontsize = 11)
ax.legend(fontsize = 2)
plt.show()
right_col.pyplot(fig)

#Bagian B
st.header('Negara dengan Produksi Terbesar pada 1 Tahun')
st.sidebar.header('Pengaturan Data Produksi Terbesar dan Kumulatif suatu Negara')
tahun = st.sidebar.number_input("Pilih Tahun produksi", min_value=1971, max_value=2015)
n = st.sidebar.slider("Pilih Banyak Negara", min_value=1, max_value=None)

dfb = dfC.loc[dfC['tahun'] == tahun]
dfb = dfb.sort_values(by='produksi', ascending = False)
dfbaru = dfb[:n]

dfbaru.plot.bar(x='kode_negara', y='produksi', color='cyan')
plt.title('{B} Negara dengan Produksi Terbesar pada Tahun {T}'.format(B=n,T=tahun))
plt.xlabel('Kode Negara')
plt.ylabel('Jumlah Produksi')
plt.show()
st.pyplot(plt)

#Bagian C
st.header('Negara dengan Produksi Kumulatif Terbesar')
kode_kmltf = []
kumulatif = []

for i in list (dfC['kode_negara']) :
    if i not in kode_kmltf:
        kode_kmltf.append(i)
        
for i in kode_kmltf :
    a=dfC.loc[dfC['kode_negara'] ==i,'produksi'].sum()
    kumulatif.append(a)
    
dk = pd.DataFrame(list(zip(kode_kmltf,kumulatif)), columns = ['kode_negara','kumulatif'])
dk = dk.sort_values(by=['kumulatif'], ascending = False)
dk2 = dk.sort_values(by=['kumulatif'], ascending = True)
dk1 = dk[:n]

dk1.plot.bar(x='kode_negara', y='kumulatif', color='cyan')
plt.title('{B} Negara dengan Produksi Kumulatif Terbesar pada Tahun {T}'.format(B=n,T=tahun))
plt.xlabel('Kode Negara')
plt.ylabel('Produksi Kumulatif')
plt.show()
st.pyplot(plt)

#Bagian D
c1, c2, c3, c4 = st.columns(4)
col1, col2, col3, col4 = st.columns(4)
lft, rght = st.columns(2)

#Maksimum
jumlah_produksi = dfb[:1].iloc[0]['produksi']
kode_ngr = dfb[:1].iloc[0]['kode_negara']
nama_ngr = ""
region = ""
subregion = ""

for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_ngr:
        nama_ngr = list(dfJ['name'])[i]
        region = list(dfJ['region'])[i]
        subregion = list(dfJ['sub-region'])[i]
        
c1.write('Negara dengan Produksi Terbesar')
col1.write(jumlah_produksi)
col1.write(kode_ngr)
col1.write(nama_ngr)
col1.write(region)
col1.write(subregion)

jumlah_produksi = dk[:1].iloc[0]['kumulatif']
kode_ngr = dk[:1].iloc[0]['kode_negara']
nama_ngr = ""
region = ""
subregion = ""

for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_ngr:
        nama_ngr = list(dfJ['name'])[i]
        region = list(dfJ['region'])[i]
        subregion = list(dfJ['sub-region'])[i]
        
c2.write('Negara dengan Produksi Terbesar pada Keseluruhan Tahun')
col2.write(jumlah_produksi)
col2.write(kode_ngr)
col2.write(nama_ngr)
col2.write(region)
col2.write(subregion)


#Minimum tak 0
def_terkecil = dfb[dfb.produksi !=0]
def_terkecil = def_terkecil.sort_values(by=['produksi'],ascending=True)
jumlah_produksi = def_terkecil[:1].iloc[0]['produksi']
kode_ngr = def_terkecil[:1].iloc[0]['kode_negara']
nama_ngr = ""
region = ""
subregion = ""
                                    
for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_ngr:
        nama_ngr = list(dfJ['name'])[i]
        region = list(dfJ['region'])[i]
        subregion = list(dfJ['sub-region'])[i]
                                    
c3.write('Negara dengan Produksi Terkecil')
col3.write(jumlah_produksi)
col3.write(kode_ngr)
col3.write(nama_ngr)
col3.write(region)
col3.write(subregion)

df_kmltfmin=dk2[dk2.kumulatif !=0]
df_kmltfmin = df_kmltfmin[:1].sort_values(by=['kumulatif'], ascending = True)
jumlah_produksi = df_kmltfmin[:1].iloc[0]['kumulatif']
kode_ngr = df_kmltfmin[:1].iloc[0]['kode_negara']
nama_ngr = ""
region = ""
subregion = ""
                                                
for i in range(len(dfJ)):
    if list(dfJ['alpha-3'])[i]==kode_ngr:
        nama_ngr = list(dfJ['name'])[i]
        region = list(dfJ['region'])[i]
        subregion = list(dfJ['sub-region'])[i]


c4.write('Negara dengan Produksi Terkecil Pada Keseluruhan Tahun')
col4.write(jumlah_produksi)
col4.write(kode_ngr)
col4.write(nama_ngr)
col4.write(region)
col4.write(subregion)
 

#Data Nol
df_produksi0 = dfb[dfb.produksi == 0]
listnegaranol = []
listregionol = []
listsubregionol = []

for i in range(len(df_produksi0)):
    for j in range(len(dfJ)):
        if list (df_produksi0['kode_negara'])[i] == list(dfJ['alpha-3'])[j]:
            listnegaranol.append(list(dfJ['name'])[j])
            listregionol.append(list(dfJ['region'])[j])
            listsubregionol.append(list(dfJ['sub-region'])[j])

df_produksi0['negara'] = listnegaranol
df_produksi0['region'] = listregionol
df_produksi0['sub-region'] = listsubregionol
 
                                                        
df_produksikmltf = dfb[dfb.produksi == 0]
listnegarakumulatifnol = []
listregionkumulatifnol = []
listsubregionkumulatifnol = []

for i in range(len(df_produksikmltf)):
    for j in range(len(dfJ)):
        if list (df_produksikmltf['kode_negara'])[i] == list(dfJ['alpha-3'])[j]:
            listnegarakumulatifnol.append(list(dfJ['name'])[j])
            listregionkumulatifnol.append(list(dfJ['region'])[j])
            listsubregionkumulatifnol.append(list(dfJ['sub-region'])[j])

df_produksikmltf['negara'] = listnegarakumulatifnol
df_produksikmltf['region'] = listregionkumulatifnol
df_produksikmltf['sub-region'] = listsubregionkumulatifnol   

lft.write('Data Negara dengan Produksi Nol')                                                     
lft.write(df_produksi0)
rght.write('Data Negara dengan Produksi Kumulatif Nol')       
rght.write(df_produksikmltf)

gif = Image.open('34f1d8973dfbbe0d4442102053c2317a.gif')
st.image(gif)
