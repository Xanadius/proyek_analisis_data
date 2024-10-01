# Dashboard Proyek Analisis Data Kualitas Udara
Proyek ini berisi dashboard interaktif yang menganalisis kualitas udara menggunakan dataset yang mencakup berbagai polutan dan variabel lainnya. Dashboard ini dibuat menggunakan **Streamlit** dan dapat dijalankan secara lokal atau di-deploy ke Streamlit Cloud.

## Prasyarat

Pastikan Anda telah menginstal prasyarat berikut sebelum menjalankan dashboard:

1. **Python 3.x**: Dashboard ini dikembangkan menggunakan Python, jadi Anda perlu Python versi 3.x.
2. **Streamlit**: Pastikan Anda sudah menginstal Streamlit. Jika belum, instal dengan perintah berikut:
    ```bash
    pip install streamlit
    ```

3. **Library Pendukung**: Selain Streamlit, Anda juga perlu menginstal beberapa library lainnya:
    ```bash
    pip install pandas matplotlib seaborn
    ```

## Menjalankan Dashboard Secara Lokal

1. **Clone Repository**:
    Clone repository proyek ini atau unduh seluruh berkas proyek ke direktori lokal Anda:
    ```bash
    git clone https://github.com/username/project-name.git
    cd project-name
    ```

2. **Jalankan Streamlit**:
    Buka terminal Anda dan arahkan ke folder tempat file *Streamlit* berada. Gunakan perintah berikut untuk menjalankan dashboard:
    ```bash
    streamlit run dashboard.py
    ```

3. **Akses Dashboard**:
    Setelah perintah di atas dijalankan, Streamlit akan memberikan URL (biasanya `http://localhost:8501/`). Anda dapat membuka URL tersebut di browser untuk melihat dashboard.

## Penjelasan File

- **dashboard.py**: Script utama yang memuat dashboard Streamlit.
- **data/PRSA_Data_Aotizhongxin_20130301-20170228.csv**: File CSV yang berisi dataset kualitas udara di stasiun Aotizhongxin.
- **requirements.txt**: File teks ini berisi library yang digunakan dalam proyek ini.
- **README.md**: Dokumentasi ini yang menjelaskan cara menjalankan proyek.
- **url.txt**: File teks ini berisi url/link menuju dashboard.

## Deployment ke Streamlit Cloud

Jika Anda ingin meng-deploy dashboard ini ke **Streamlit Cloud**, ikuti langkah-langkah berikut:

1. Masuk ke [Streamlit Cloud](https://streamlit.io/cloud).
2. Buat aplikasi baru dengan menghubungkan repository GitHub Anda.
3. Pilih file `dashboard.py` sebagai file utama untuk dijalankan.
4. Klik tombol **Deploy** dan Streamlit akan membuatkan URL yang dapat diakses publik untuk dashboard Anda.

## Catatan

- Pastikan dataset terletak di direktori yang sama dengan `dashboard.py` atau sesuaikan path di dalam kode jika dataset berada di lokasi lain.
- Anda bisa menyesuaikan visualisasi, analisis, dan elemen lain dari dashboard dengan mudah melalui script `dashboard.py`.
