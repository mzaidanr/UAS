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

produksi_total = dfC[:1].iloc[0]['Production']
country_codes = dfC[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ("")

for x in range(len(dfJ)):
    if list(dfJ['alpha-3'])[x] == country_codes:
        negara = list(dfJ['name'])[x]
        region = list(dfJ['region'])[x]
        subregion = list(dfJ['sub-region'])[x]
print("")
st.markdown("Negara dengan total jumlah produksi terbesar pada tahun", T, "adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.textv(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

produksi_total = dk[:1].iloc[0]['jumlah']
country_codes = dk[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ("")

for x in range(len(dk)):
    if list(dk['alpha-3'])[x] == country_codes:
        negara = list(dk['name'])[x]
        region = list(dk['region'])[x]
        subregion = list(dk['sub-region'])[x]
print("")
st.markdown("Negara dengan jumlah produksi minyak terbesar secara keseluruhan adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.text(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

#Terkecil
dfkecil=dfC[dfC.Production !=0]
dfkecil=dfkecil.sort_values(by=['Production'], ascending= True)

produksi_total=dfkecil[:1].iloc[0]['Production']
country_codes =dfkecil[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ('')

for x in range(len(dfJ)):
    if list(dfJ['alpha-3'])[x] == country_codes:
        negara = list(dfJ['name'])[x]
        region = list(dfJ['region'])[x]
        subregion = list(dfJ['sub-region'])[x]

print("")
st.markdown("Negara dengan total jumlah produksi terkecil pada tahun", T, "adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.text(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

dfjumlahkecil=dk[dk.jumlah !=0]
dfjumlahkecil=dfjumlahkecil.sort_values(by=['jumlah'], ascending= True)

produksi_total=dfjumlahkecil[:1].iloc[0]['jumlah']
country_codes =dfjumlahkecil[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ('')

for x in range(len(dfJ)):
    if list(dfJ['alpha-3'])[x] == country_codes:
        negara = list(dfJ['name'])[x]
        region = list(dfJ['region'])[x]
        subregion = list(dfJ['sub-region'])[x]

print("")
st.markdown("Negara dengan jumlah produksi minyak terkecil secara keseluruhan adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.text(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

#terakhiran
negaranol =[]
regionol = []
subregionol =[]
dfnol= dfC[dfC.Production ==0]
for x in range (len(dfnol)):
    for y in range(len(dfJ)):
        if list(dfnol['country_code'])[x] == list(dfjumlahkecil['alpha-3'])[y] :
            negaranol.append(list(dfJ['name'])[y])
            regionol.append(list(dfJ['region'])[y])
            subregionol.append(list(dfJ['sub-region'])[y])
dfnol['country'] = negaranol
dfnol['region'] = regionol
dfnol['sub-region'] = subregionol
dftotalnol= dk[dk.jumlah ==0]
totalnegaranol =[]
totalregionol = []
totalsubregionol =[]
for x in range (len(dftotalnol)):
    for y in range(len(dfJ)):
        if list(dftotalnol['country_code'])[x] == list(dfJ['alpha-3'])[y] :
            totalnegaranol.append(list(dfJ['name'])[y])
            totalregionol.append(list(dfJ['region'])[y])
            totalsubregionol.append(list(dfJ['sub-region'])[y])
print("")
st.dataframe(dfnol)
st.table(dftotalnol)

st.set_option('deprecation.showPyplotGlobalUse', False)
