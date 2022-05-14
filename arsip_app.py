import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from PIL import Image
import sqlite3
from gsheetsdb import connect
import warnings
warnings.filterwarnings('ignore')


bpk_icon = Image.open("asset/BPK.ico")
LOGO_IMAGE = "asset/BPK.png"
st.set_page_config(
    layout="centered", page_icon=bpk_icon, page_title="Arsip Digital Kertas Kerja Pemeriksa", initial_sidebar_state="auto"
) #layout use wide instead of centered

#from here
# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
#rows = run_query(f'SELECT * FROM "{sheet_url}"')
st.write(sheet_url)
# Print results.
#for row in rows:
    #st.write(f"{row.City} has a :{row.Rating}:")

#to here


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

#sementara sebelum merubah nama tabel agar hemat line code
if option == "Kertas Kerja Pemeriksa":
    choice = "tabel_kkp"
elif option == "Aset TI":
    choice = "aset_ti"
if option == "Data Kesekretariatan":
    choice = "tabel_kkp"


col1, col2 = st.columns([2,5])

with col1:
    st.image(bpk_icon, width =150, use_column_width=True)

with col2:
    st.title("Arsip Digital \n Kertas Kerja Pemeriksa")
    #st.header("Kertas Kerja Pemeriksa")

st.write(
    """Selamat datang di webapp arsip digital Kertas Kerja Pemeriksa.
    Webapp ini dibuat menggunakan bahasa pemrograman Python 3.10 dengan streamlit library.
    Untuk index tabel disimpan menggunakan database sqlite3"""
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

#menggunakan sqlite database
con = sqlite3.connect("asset/arsip.db") #koneksi ke sqlite database
tabel_index_arsip = pd.read_sql_query("SELECT * from " + choice, con)

#jika menggunakan csv
#tabel_index_arsip = pd.read_csv(
    #"asset/tabel_kkp.csv"
#) #ini bisa berupa csv sementara, atau connect ke sqlite tabel
con.close() #close connection, jika ingin mengedit database, posisi con.close bisa dipaling bawah

pilihan_row = tabel_arsip(df=tabel_index_arsip)
#st.write(pilihan_row['selected_rows'][0]['City'])
#pilihan_row adalah object berbentuk nested dictionaries
#jika ingin memilih value gunakan syntax ini pilihan_row['selected_rows'][0]['nama kolom yang mau didisplay valuenya']

if pilihan_row:
    st.write("Anda memilih:")
    #st.json(pilihan_row["selected_rows"])
    pilihanmu = pilihan_row["selected_rows"] #for reproducibility, jika ingin memilih value tinggal pilihanmu['nama kolom']
    if pilihanmu:
        st.write("Kota yang anda pilih: ", pilihanmu[0]['City'])
        st.write("Pendapatan kotor rata-rata di kota " , pilihanmu[0]['City'] , ": " , str(pilihanmu[0]['grossincome']))
    else:
        st.write("Anda belum memilih arsip")
