import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from PIL import Image
import sqlite3
import warnings
warnings.filterwarnings('ignore')


bpk_icon = Image.open("asset/BPK.ico")
LOGO_IMAGE = "asset/BPK.png"
st.set_page_config(
    layout="centered", page_icon=bpk_icon, page_title="Arsip Digital Kertas Kerja Pemeriksa", initial_sidebar_state="auto"
) #layout use wide instead of centered


with st.sidebar:
    col1, col2 = st.columns([2, 5])
    with col1:
        st.image(bpk_icon, width=150, use_column_width=True)
    #st.sidebar.image(bpk_icon, width=50)
    with col2:
        st.write("Arsip Digital \n Kertas Kerja Pemeriksa")

    option = st.selectbox(
        'Data subbag apa yang ingin anda cari?',
        ('Kertas Kerja Pemeriksa', 'Aset TI', 'Data Kesekretariatan'))

    values = st.slider(
        "Data Arsip tahun berapa yang anda cari?",
        2015, 2022, (2018, 2019))
    if 'year' not in st.session_state: #experimental using st.session_state, if not wowrking just delete
        st.session_state['key'] = values
    #st.write(st.session_state['key'])

    #values dtypes is tuple

#sementara sebelum merubah nama tabel agar hemat line code
if option == "Kertas Kerja Pemeriksa":
    choice = "tabel_kkp"
elif option == "Aset TI":
    choice = "aset_ti"
if option == "Data Kesekretariatan":
    choice = "tabel_kkp"
#bagian ini masih harus di perbaiki, tiap pilihan menampilkan sheet berbeda

col1, col2 = st.columns([2,5])

with col1:
    st.image(bpk_icon, width =150, use_column_width=True)

with col2:
    st.title("Arsip Digital \n Kertas Kerja Pemeriksa")
    #st.header("Kertas Kerja Pemeriksa")

st.write(
    """ \n Selamat datang di webapp arsip digital Kertas Kerja Pemeriksa.\n
    Webapp ini dibuat menggunakan bahasa pemrograman Python 3.10 dengan streamlit library.\n
    Database index tabel disimpan menggunakan google spreadsheets"""
)
st.write("Silahkan klik pada row tabel yang mana anda ingin lihat arsip digitalnya.")

def tabel_arsip(df: pd.DataFrame):
    #tabel interaktif berisi index arsip digital KKP
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

#menggunakan live google spreadsheet
#@st.cache(ttl=600)
sheet_url = "https://docs.google.com/spreadsheets/d/1pW0_JJ3NuXDcuIFlQ88v8qPa-YtD1B9dOu-J-JDAyX4/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=') #to get the csv version
tabel_index_arsip = pd.read_csv(url_1) #to read the csv as pandas dataframe

tabel_index_arsip = tabel_index_arsip[tabel_index_arsip['Year'].isin(st.session_state['key'])] #delete session state to only values
                                       #== values[0]) & (tabel_index_arsip['Year'] == values[1])]
#in here you can put pandas table operation such as only display certain years
#before you feed it as an argumen to our aggregat table below

pilihan_row = tabel_arsip(df=tabel_index_arsip)  #call our interactive table aggrid

#st.write(pilihan_row['selected_rows'][0]['City'])
#pilihan_row adalah object berbentuk nested dictionaries
#jika ingin memilih value gunakan syntax ini pilihan_row['selected_rows'][0]['nama kolom yang mau didisplay valuenya']

if pilihan_row:
    st.write("Anda memilih:")
    #st.json(pilihan_row["selected_rows"])
    pilihanmu = pilihan_row["selected_rows"] #for reproducibility, jika ingin memilih value tinggal pilihanmu['nama kolom']
    if pilihanmu:
        st.write("Kota yang anda pilih: ", pilihanmu[0]['City'])
        st.write("Link untuk mendownload pdf kote ", pilihanmu[0]['City'] , ": " )
        st.write("[View PDF arsip](" + pilihanmu[0]['Link'] + ")")
        #to write hyperlink with shorter clickable use syntax to create a variable link = '[GitHub](http://github.com)'
        #or you can put it inside st.write statement directly as above
    else:
        st.write("Anda belum memilih arsip")



