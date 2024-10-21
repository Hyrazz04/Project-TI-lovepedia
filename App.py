import streamlit as st
import random
import json
import os

def apply_custom_css():
    st.markdown(
        """
        <style>
        .block-container {
            padding: 2rem 5rem;
        }
        h1 {
            color: #ffffff; /* Heading warna gelap yang mudah dibaca */
            text-align: center;
            font-size: 3rem;
        }
        h2, h3, h4 {
            color: #ffffff; /* Subheading */
        }
        /* Gaya tombol dan interaksi */
        .stButton button {
            background-color: #1ABC9C; /* Tombol  */
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #16A085; /* Warna hover  */
            color: white;
        }
        .stTextInput>div>div>input {
            color: #2C3E50; /* Warna teks di dalam input */
            background-color: #FDFEFE; /* Latar belakang input  */
            border: 1px solid #D5D8DC; /* Garis abu-abu tipis */
            padding: 10px;
        }
        /* Pemisah untuk daftar pengguna */
        hr {
            border: none;
            height: 1px;
            background-color:#ffffff; /* Garis pemisah abu-abu halus */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Fungsi untuk menyimpan data ke file JSON
def simpan_data():
    with open("data_pengguna.json", "w") as f:
        json.dump(st.session_state.daftar_pengguna, f)

# Fungsi untuk memuat data dari file JSON
def muat_data():
    if os.path.exists("data_pengguna.json"):
        with open("data_pengguna.json", "r") as f:
            st.session_state.daftar_pengguna = json.load(f)
    else:
        st.session_state.daftar_pengguna = []



# Inisialisasi daftar pengguna di session_state
if "daftar_pengguna" not in st.session_state:
    muat_data()

# Fungsi untuk menampilkan pengguna
def tampilkan_pengguna():
    if not st.session_state.daftar_pengguna:
        st.write("### Tidak ada pengguna saat ini.")
    else:
        st.write("## Daftar pengguna terdaftar:")
        for i, pengguna in enumerate(st.session_state.daftar_pengguna, start=1):
            st.write(f"**{i}. Nama**: {pengguna['nama']}  \n**Umur**: {pengguna['umur']}  \n**Jenis Kelamin**: {pengguna['jenis_kelamin']}  \n**Preferensi**: {pengguna['preferensi']}  \n**Hobi**: {pengguna['hobi']}  \n**Love Language**: {pengguna['love_language']}  \n**Preferensi Love Language**: {pengguna['preferensi_love_language']}  \n**Agama**: {pengguna['agama']}  \n**Nomor WA**: {pengguna['nomor_wa']}")
            st.markdown("<hr/>", unsafe_allow_html=True) # separator antar pengguna

# Fungsi untuk menambahkan pengguna
def tambah_pengguna():
    st.write("## Tambahkan Pengguna Baru")
    nama = st.text_input("Masukkan nama:")
    umur = st.number_input("Masukkan umur:", min_value=1, step=1)
    jenis_kelamin = st.selectbox("Masukkan jenis kelamin:", ["L", "P"])
    preferensi = st.selectbox("Masukkan preferensi jenis kelamin jodoh:", ["L", "P"])
    hobi = st.text_input("Masukkan hobi Anda (pisahkan dengan koma jika lebih dari satu):")
    love_language = st.selectbox("Masukkan love language Anda:", ["Acts of service", "Words of affirmation", "Quality time", "Physical touch", "Receiving gifts"])
    preferensi_love_language = st.selectbox("Masukkan preferensi love language jodoh:", ["Acts of service", "Words of affirmation", "Quality time", "Physical touch", "Receiving gifts"])
    agama = st.text_input("Masukkan agama Anda:")
    nomor_wa = st.text_input("Masukkan nomor WA: ")

    if st.button("Tambahkan Pengguna"):
        pengguna = {
            "nama": nama,
            "umur": umur,
            "jenis_kelamin": jenis_kelamin,
            "preferensi": preferensi,
            "hobi": hobi,
            "love_language": love_language,
            "preferensi_love_language": preferensi_love_language,
            "agama": agama,
            "nomor_wa": nomor_wa
        }
        # Tambahkan pengguna ke session_state
        st.session_state.daftar_pengguna.append(pengguna)
        simpan_data()
        st.success(f"{nama} telah ditambahkan ke dalam daftar pengguna.")

# Fungsi untuk mencari jodoh
def cari_jodoh():
    if len(st.session_state.daftar_pengguna) < 2:
        st.write("### Belum cukup pengguna untuk mencocokkan.")
        return

    nama = st.text_input("Masukkan nama Anda untuk mencari jodoh:")

    if st.button("## Cari Jodoh"):
        pengguna_dicari = next((pengguna for pengguna in st.session_state.daftar_pengguna if pengguna["nama"] == nama), None)

        if pengguna_dicari is None:
            st.write("Nama Anda tidak ditemukan dalam daftar pengguna.")
            return

        pasangan_cocok = []
        for pengguna in st.session_state.daftar_pengguna:
            if pengguna != pengguna_dicari:
                if pengguna["jenis_kelamin"] != pengguna_dicari["jenis_kelamin"]:
                    if pengguna["jenis_kelamin"] == pengguna_dicari["preferensi"] and pengguna_dicari["jenis_kelamin"] == pengguna["preferensi"]:
                        if abs(pengguna["umur"] - pengguna_dicari["umur"]) <= 5:
                            if pengguna["agama"] == pengguna_dicari["agama"]:
                                if pengguna_dicari["preferensi_love_language"] == pengguna["love_language"]:
                                    pasangan_cocok.append(pengguna)

        if pasangan_cocok:
            random.seed()
            pasangan_dipilih = random.choice(pasangan_cocok)
            st.write("Pasangan yang cocok untuk Anda adalah:")
            st.write(f"Nama: {pasangan_dipilih['nama']}, Umur: {pasangan_dipilih['umur']}, Jenis Kelamin: {pasangan_dipilih['jenis_kelamin']}, Hobi: {pasangan_dipilih['hobi']}, Love Language: {pasangan_dipilih['love_language']}, Agama: {pasangan_dipilih['agama']}, Nomor WA: {pasangan_dipilih['nomor_wa']}")
        else:
            st.write("Tidak ada pasangan yang cocok ditemukan.")

# Fungsi menu utama
def menu():
    apply_custom_css() # terapkan CSS di awal
    st.title("Lovepedia")
    st.write("### Masa depan mu ditentukan dengan satu klik!")
    

    menu_options = ["Lihat daftar pengguna", "Tambah pengguna baru", "Cari jodoh"]
    pilihan = st.selectbox("Pilih menu:", menu_options)

    if pilihan == "Lihat daftar pengguna":
        tampilkan_pengguna()
    elif pilihan == "Tambah pengguna baru":
        tambah_pengguna()
    elif pilihan == "Cari jodoh":
        cari_jodoh()

# Jalankan menu
menu()
