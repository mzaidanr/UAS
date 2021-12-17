import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


#COBA DISPLAY DATA NEGARA DULU YG BISA DI INPUT SEBELOM INPUT NAMA NEGARANYA

f = open("kode_negara_lengkap.json")
file_json = json.load(f)
df_xsl = pd.read_excel(
    "produksiminyakmentah.xlsx")
df_csv = pd.read_csv(
    "produksi_minyak_mentah.csv")
df_json = pd.DataFrame.from_dict(file_json, orient='columns')
df_xsl['country_code'] = df_csv['kode_negara']
df_xsl['Year'] = df_csv['tahun']
df_xsl['Production'] = df_csv['produksi']
df_csv['country_code'] = df_xsl['country_code']
df_csv['Year'] = df_xsl['Year']
df_csv['Production'] = df_xsl['Production']

listnih= []
listbaru = []
listnih2 = []
change_country = []
for x in list(df_csv['country_code']):
    if x not in list(df_json['alpha-3']):
        listbaru.append(x)
print("")
nama = input("Tulis Nama Kamu = ")
print("")
print("Welcome ", nama, " !!!")
print("")
print("INFORMASI DULU AJA NI YAA", nama.upper())
print("")
print("Di bawah ini merupakan kode negara yang dihapus karena tidak masuk kalkulasi")
print(listbaru)
#jumlah kode negara yg gadiperluin
print("jumlah alpha-3 awal = ", len(df_csv))
for x in listbaru:
    df_csv = df_csv[df_csv.country_code != x]
print("jumlah alpha-3 sesudah dihilangkan = ", len(df_csv))
print("jumlah alpha-3 yang dihilangkan = ", len(listbaru))
print("")
print("")

inputan = st.text_input("Silahkan masukkan nama Negara yang ingin dicari = ")
dfbaru=df_csv.loc[df_csv['country_code'] == inputan]

#Pemunculan Grafik
grafik = plt.show()
dfbaru.plot(x='Year',y='Production', color='red')
st.pyplot(grafik)
# UNTUK NAMA NEGARA PAKE TOLERANSI HURUF BESAR HURUF KECIL SEMENTARA

#B
print("")
st.text("Untuk Tahun mohon masukkan tahun yang ada pada data untuk menghindari error")
T = int(st.text_input("Masukkan tahun produksi = ", key="T"))
B = int(st.text_input("Masukkan banyak negara untuk ditampilkan = ", key="B"))

df1 = df_csv.loc[df_csv['Year'] == T]
df1 = df1.sort_values(by=['Production'], ascending=False)
dfm = df1[:B]

i = 0
i = i+2
dfm.plot.barh(x='country_code', y='Production', color='mediumorchid', rot=23)
plt.xticks(size=12)
plt.yticks(size=13.5)
grafik1 = plt.show()
st_pyplot(grafik1)

#3
jumlah = []

B2 = int(st.text_input("Masukkan banyak negara untuk ditampilkan jumlah kumulatifnya = ", key="B2"))
for x in list(df_csv['country_code']):
    if x in listnih2:
        continue
    if x not in listnih2:
        listnih2.append(x)

for x in listnih2 :
    i = df_csv.loc[df_csv['country_code'] == x , 'Production'].sum()
    jumlah.append(i)

df2 =pd.DataFrame(list(zip(listnih2,jumlah)), columns=['country_code','jumlah'])
df2 = df2.sort_values(by=['jumlah'], ascending =False)
dft = df2[:B2]
dft.plot.barh(x='country_code', y='jumlah', color='indigo')
grafik2=plt.show()
st.pyplot(grafik2)

#4
produksi_total = df1[:1].iloc[0]['Production']
country_codes = df1[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ("")

for x in range(len(df_json)):
    if list(df_json['alpha-3'])[x] == country_codes:
        negara = list(df_json['name'])[x]
        region = list(df_json['region'])[x]
        subregion = list(df_json['sub-region'])[x]
print("")
st.markdown("Negara dengan total jumlah produksi terbesar pada tahun", T, "adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.textv(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

produksi_total = df2[:1].iloc[0]['jumlah']
country_codes = df2[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ("")

for x in range(len(df_json)):
    if list(df_json['alpha-3'])[x] == country_codes:
        negara = list(df_json['name'])[x]
        region = list(df_json['region'])[x]
        subregion = list(df_json['sub-region'])[x]
print("")
st.markdown("Negara dengan jumlah produksi minyak terbesar secara keseluruhan adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.text(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

#Terkecil
dfkecil=df1[df1.Production !=0]
dfkecil=dfkecil.sort_values(by=['Production'], ascending= True)

produksi_total=dfkecil[:1].iloc[0]['Production']
country_codes =dfkecil[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ('')

for x in range(len(df_json)):
    if list(df_json['alpha-3'])[x] == country_codes:
        negara = list(df_json['name'])[x]
        region = list(df_json['region'])[x]
        subregion = list(df_json['sub-region'])[x]

print("")
st.markdown("Negara dengan total jumlah produksi terkecil pada tahun", T, "adalah dibawah ini ")
st.text(negara)
st.text(country_codes)
st.text(region)
st.text(subregion)
st.text("dengan produksi sebanyak ",produksi_total)

dfjumlahkecil=df2[df2.jumlah !=0]
dfjumlahkecil=dfjumlahkecil.sort_values(by=['jumlah'], ascending= True)

produksi_total=dfjumlahkecil[:1].iloc[0]['jumlah']
country_codes =dfjumlahkecil[:1].iloc[0]['country_code']
negara = ("")
region = ("")
subregion = ('')

for x in range(len(df_json)):
    if list(df_json['alpha-3'])[x] == country_codes:
        negara = list(df_json['name'])[x]
        region = list(df_json['region'])[x]
        subregion = list(df_json['sub-region'])[x]

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
dfnol= df1[df1.Production ==0]
for x in range (len(dfnol)):
    for y in range(len(df_json)):
        if list(dfnol['country_code'])[x] == list(df_json['alpha-3'])[y] :
            negaranol.append(list(df_json['name'])[y])
            regionol.append(list(df_json['region'])[y])
            subregionol.append(list(df_json['sub-region'])[y])
dfnol['country'] = negaranol
dfnol['region'] = regionol
dfnol['sub-region'] = subregionol
dftotalnol= df2[df2.jumlah ==0]
totalnegaranol =[]
totalregionol = []
totalsubregionol =[]
for x in range (len(dftotalnol)):
    for y in range(len(df_json)):
        if list(dftotalnol['country_code'])[x] == list(df_json['alpha-3'])[y] :
            totalnegaranol.append(list(df_json['name'])[y])
            totalregionol.append(list(df_json['region'])[y])
            totalsubregionol.append(list(df_json['sub-region'])[y])
print("")
st.dataframe(dfnol)
st.table(dftotalnol)

st.set_option('deprecation.showPyplotGlobalUse', False)