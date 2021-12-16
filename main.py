import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import csv
import json

st.sidebar.title('Pilih Fitur yang akan digunakan')
option=st.sidebar.selectbox('pilih salah satu',('Jumlah Pertahun','Produksi Terbesar', 'Produksi Kumulatif', 'Data Pertahun'))

# inisiasi fungsi
def csvFileToList():
     csvreader = csv.reader(open("produksi_minyak_mentah.csv"))
     header = next(csvreader)
     file = []
     # looping append ke list
     for item in csvreader:
          file.append(item)
     return file

def getDataMinyakByKode(kodeNegara, angka):
     file = csvFileToList()
     data = []
     
     # looping mencari data sesuai kode negara
     # angka dalam fungsi ini sesuai dengan entry array / record
     # 0 = kode negara, 1 = tahun, 2 = jumlah produksi
     # 4 untuk retrieve seluruh data
     if angka == 4:
          for item in file:
               if item[0] == kodeNegara:
                    data.append(item)
     
     for item in file:
          if item[0] == kodeNegara:
               data.append(item[angka])
     return data

def getDataMinyakByTahun(tahun):
     file = csvFileToList()
     data = []

     # looping mencari data sesuai tahun produksi
     for item in file:
          if item[1] == tahun and isNegaraIndividu(item[0]):# isNegaraIndividu() untuk memfilter negara kelompok
               data.append(item) 
     return data
     
def getDataNegara(kodeNegara):
     file = open("kode_negara_lengkap.json")
     data = json.load(file)
     for item in data:
          if item['alpha-3'] == kodeNegara:
               return item

def getDataKumulatif(kodeNegara):
     file = csvFileToList()
     data = []
     i = 0
     sum = 0
     for item in file:
          if item[0] == kodeNegara:
               tempArray = []
               sum += float(item[2])
               tempArray.insert(i,item[2])
               tempArray.insert(i,sum)
               data.append(tempArray)
          i += 1
     return data


def getKodeNegara(namaNegara):
     file = open("kode_negara_lengkap.json")
     data = json.load(file)
     for item in data:
          if item['name'] == namaNegara:
               return item['alpha-3']

def getAllKodeNegara():
     file = open("kode_negara_lengkap.json")
     data = json.load(file)
     tempArray = []
     for item in data:
          tempArray.append(item['alpha-3'])
     return tempArray

def getAllTahun():
     file = csvFileToList()
     data = []

     # looping mencari data sesuai tahun produksi
     for item in file:
          if item[0] == 'AUS':
               data.append(item[1])
     return data

def getByValue(tahun, case):
     data = getDataMinyakByTahun(tahun)
     negara = getAllKodeNegara()
     tempArray = []
     if case == 'zero':
          for item in data:
               for any in negara:
                    if any == item[0] and float(item[2]) == 0.0:
                         tempArray = item
     if case == 'max':
          nilai = 0.0
          for item in data:
               for any in negara:
                    if any == item[0] and float(item[2]) > nilai:
                         nilai = float(item[2])
                         tempArray = item
     if case == 'min':
          nilai = 1000000.0
          for item in data:
               for any in negara:
                    if any == item[0] and float(item[2]) < nilai and float(item[2]) != 0.0:
                         nilai = float(item[2])
                         tempArray = item
     # if case =='total':

     return tempArray

def getTotalProduksi(kodeNegara):
     produksi = getDataMinyakByKode(kodeNegara, 2)
     total = 0.0
     for item in produksi:
          total += float(item)
     return total

def getAllNamaNegara():
    file = open("kode_negara_lengkap.json")
    data = json.load(file)
    negara = []
    
    for item in data:
         negara.append(item['name'])
    return negara

def countAmountNegara():
     return len(getAllNamaNegara())

#kunci dari jumlah produksi
def keyJumlahProduksi(e):
     return np.double(e[2])

def getDataMinyakByTahunAndJumlah(tahun,jumlah):
     dataMinyak = getDataMinyakByTahun(tahun)
     #sorting dataMinyak
     dataMinyak.sort(key=keyJumlahProduksi,reverse=True)
     mostData = []
     i = 1
     #mengambil data sejumlah {jumlah} untuk mostData
     for temp in dataMinyak:
          mostData.append(temp)
          if i ==jumlah : break
          i +=1
     return mostData

# convert List to set
def listtoSetWithKey(data):
     baru =[]
     for A in data:
          temp = {}
          temp['Kode Negara'] = A[0]
          temp['Tahun'] = A[1]
          temp['Jumlah'] = A[2]
          baru.append(temp)
     return baru

def isNegaraIndividu(kodeNegara):
     file = open("kode_negara_lengkap.json")
     data = json.load(file)

     # validasi kodeNegara adalah negara individu atau kelompok
     for temp in data:
          if temp['alpha-3'] == kodeNegara:
               return temp['name']
     return False

def getNamaNegara(kodeNegara):
     file = open("kode_negara_lengkap.json")
     data = json.load(file)
     for item in data:
          if item['alpha-3'] == kodeNegara:
               return item['name']

def getAllTotalProduksi():
     # mengambil total dari tahun 1971 sampai 2015 negara individu
     file = open("kode_negara_lengkap.json")
     data = json.load(file)
     file = csvFileToList()
     arr = []

     # membuat record
     for temp in data:
          A={}
          A['Nama Negara'] = temp['name']
          A['Kode Negara'] = temp['alpha-3']
          A['Total'] = getTotalProduksi(temp['alpha-3'])
          arr.append(A)
     return arr

def keyTotal(e):
     return e.get('Total')

def getDataKumulatifByJumlah(jumlah):
     temp = getAllTotalProduksi()
     temp.sort(key=keyTotal,reverse=True)
     data = []
     for x in range(jumlah):
          data.append(temp[x])
          
     return data
     
# Soal Point A
if option == 'Jumlah Produksi Pertahun':
     st.title("Jumlah Produksi Minyak Pertahun")
     NamaNegara = st.selectbox("Pilih Nama Negara", getAllNamaNegara())
     kodeNegara = getKodeNegara(NamaNegara)
     tahun = getDataMinyakByKode(kodeNegara, 1)
     jumlah = getDataMinyakByKode(kodeNegara, 2)
     if kodeNegara or (tahun and jumlah):
          st.subheader("grafik jumlah produksi minyak pertahun negara ", NamaNegara )
          
          #menampilkan grafik
          if tahun and jumlah:
               df = pd.DataFrame({'Tahun': tahun ,'Jumlah Minyak Mentah': jumlah})
               grafik = alt.Chart(df).mark_line().encode(
                    x = 'Tahun:O',
                    y = 'Jumlah Minyak Mentah:Q'
               ).properties(
                    width= 1000,
                    height= 500
               )
               st.altair_chart(grafik, use_container_width=True)
               st.text("Pada grafik jika kita menambahkan seluruh jumlah produksi.")
               st.text("maka akan diperoleh total %s yang dihasilkan" %getTotalProduksi(kodeNegara))
               st.text("oleh negara %s" %NamaNegara)

# Soal Point B
if option == ' Negara Dengan Produksi Terbesar':
    st.title("Negara dengan Produksi Minyak terbesar")
    jumlahNegara = st.slider('Berapa Negara :',2,countAmountNegara())
    pilihTahun = st.selectbox('Pilih Tahun', getAllTahun())
    dataMinyak = getDataMinyakByTahunAndJumlah(pilihTahun,jumlahNegara)
    dataMinyak = listtoSetWithKey(dataMinyak)
    df = pd.DataFrame(dataMinyak)
    if jumlahNegara !=0:
          grafik = alt.Chart(df).mark_bar().encode(
               x = 'Kode Negara:N',
               y = 'Jumlah:Q',
               color = 'Kode Negara:N'
          ).properties(
               width= 1000,
               height= 500
          )
          st.altair_chart(grafik, use_container_width=True)
          st.text("Tabel dari grafik diatas")
          st.table(df)
          
# Soal Point C
if option =='Produksi Kumulatif':
     st.title("Produksi Kumulatif Dari Beberapa Negara")
     jumlahNegara = st.slider('Berapa Negara :',2,countAmountNegara())
     dataMinyak = getDataKumulatifByJumlah(jumlahNegara)

     df = pd.DataFrame(dataMinyak)
     if jumlahNegara !=0:
          grafik = alt.Chart(df).mark_bar().encode(
               x = 'Kode Negara:N',
               y = 'Total:Q',
               color = 'Kode Negara:N'
          ).properties(
               width= 1000,
               height= 500
          )
          st.altair_chart(grafik, use_container_width=True)
          st.text("Tabel dari grafik diatas")
          st.table(df)

#Soal point D
if option == 'Data Produksi Pertahun':
     st.title("Data Pertahun Pada Seluruh Negara")
     allTahun = getAllTahun()
     pilihan = st.selectbox("Pilih Tahun", allTahun)
     # st.write('You selected:', pilihan)
     if pilihan:
          # Nilai Max
          st.subheader("Negara dengan produksi paling tinggi pada tahun %s" %pilihan)
          max = getByValue(pilihan, 'max')
          negara = getDataNegara(max[0])
          st.text("Nama Negara: %s" %negara['name'])
          st.text("Kode Negara: %s" %negara['alpha-3'])
          st.text("Region     : %s" %negara['region'])
          st.text("Sub Region : %s" %negara['sub-region'])
          st.text("Jumlah Produksi: %s" %max[2])
          st.text("Total Produksi : %s" %getTotalProduksi(max[0]))
          
          # Nilai Min
          st.subheader("Negara dengan produksi paling rendah pada tahun %s" %pilihan)
          min = getByValue(pilihan, 'min')
          negara = getDataNegara(min[0])
          st.text("Nama Negara: %s" %negara['name'])
          st.text("Kode Negara: %s" %negara['alpha-3'])
          st.text("Region     : %s" %negara['region'])
          st.text("Sub Region : %s" %negara['sub-region'])
          st.text("Jumlah Produksi: %s" %min[2])
          st.text("Total Produksi : %s" %getTotalProduksi(min[0]))

          # Salah satu Nilai Zero
          st.subheader("Salah satu negara yang tidak memproduksi pada tahun %s" %pilihan)
          zero = getByValue(pilihan, 'zero')
          negara = getDataNegara(zero[0])
          st.text("Nama Negara: %s" %negara['name'])
          st.text("Kode Negara: %s" %negara['alpha-3'])
          st.text("Region     : %s" %negara['region'])
          st.text("Sub Region : %s" %negara['sub-region'])
          st.text("Jumlah Produksi: %s" %zero[2])
          st.text("Total Produksi : %s" %getTotalProduksi(zero[0]))
