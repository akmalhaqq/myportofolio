Name : Muhammmad Akmal Haqqani

NPM : 2506548295

Class : PBP D

# Personal Portfolio Akmal

Website portofolio pribadi saya yang dibuat pakai HTML5 dan CSS3 untuk Tugas Individu 1 mata kuliah Pemrograman Berbasis Platform, Fakultas Ilmu Komputerm Universitas Indonesia.
Isinya informasi pribadi, kemampuan teknis, pengalaman, proyek (menyusul), dan kontak, semua dalam satu halaman yang responsif.

## Deskripsi

Saya bikin project ini untuk latihan HTML5 dan CSS3 dalam membangun static website. Fokus saya ada di dua hal, yaitu struktur halaman yang rapi dan layout yang tetap enak dilihat baik di desktop maupun di HP.
Tidak pakai frontend framework. Struktur halaman full HTML5, layout dan responsivitasnya diatur lewat CSS3.

## Fitur

### Responsive Layout

Tampilan menyesuaikan ukuran viewport. Di layar besar, beberapa bagian pakai layout multi-kolom. Begitu layar mengecil, layout berubah jadi satu kolom, dan ukuran teks serta spacing ikut menyesuaikan.
Breakpoint-nya di `768px` dan `600px`.

### Semantic HTML5

Saya pakai beberapa elemen semantik HTML5:

- `<header>`
- `<nav>`
- `<main>`
- `<section>`
- `<article>`
- `<footer>`

### Mobile Navigation

Navigasi di HP jalan pakai kombinasi HTML dan CSS saja, checkbox sebagai pengontrol state menu, CSS yang mengatur posisi dan transisinya.

### Active Navigation Indicator

Navbar punya indikator visual untuk menunjukkan section yang sedang dituju, pakai selector CSS `:target` untuk menghubungkan link navigasi ke section terkait.

### Smooth Scrolling

Perpindahan antar section pakai smooth scrolling, jadi navigasinya terasa lebih halus.

### Scroll Reveal Animation

Beberapa elemen punya animasi saat masuk viewport, dibuat pakai CSS `view-timeline` saja, tanpa library animasi tambahan.

## Teknologi

| Teknologi           | Penggunaan                                      |
| ------------------- | ----------------------------------------------- |
| HTML5               | Struktur dan konten halaman                     |
| CSS3                | Styling, layout, responsive design, dan animasi |
| CSS Grid            | Layout utama beberapa section                   |
| Flexbox             | Alignment dan pengaturan komponen               |
| Media Query         | Responsive design                               |
| CSS `:target`       | Active navigation indicator                     |
| CSS `view-timeline` | Scroll reveal animation                         |
| Remix Icon          | Icon pada website                               |
| Google Fonts        | Typography                                      |

## Struktur Project

```text
.
├── main/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── css/
│       │   └── style.css
│       └─── img/
│
├── manage.py
└── README.md
```

## Instalasi dan Menjalankan Project

### Prasyarat

Python dan Django sudah harus terpasang.

### Menjalankan Project

Clone repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

Kalau project pakai `requirements.txt`, install dependency-nya:

```bash
pip install -r requirements.txt
```

Lalu jalankan development server:

```bash
python manage.py runserver
```

Buka:

```text
http://127.0.0.1:8000/
```

## Proses Pengembangan

Saya kerjakan project ini selama satu minggu, lewat beberapa tahap.

### Perancangan Struktur

Tahap awal saya habiskan untuk menentukan informasi apa saja yang mau ditampilkan dan bagaimana membaginya jadi beberapa bagian.
Struktur utamanya pakai semantic HTML5: Hero, About, Skills, Experience, Projects (menyusul), dan Contact.

### Implementasi Layout

Setelah struktur HTML jadi, saya bangun layout pakai CSS Grid dan Flexbox. Beberapa bagian saya buat multi-kolom untuk desktop, lalu saya sesuaikan ke layar kecil lewat media query.

### Implementasi Responsive Design

Saya uji responsive behavior-nya di beberapa ukuran viewport, cek apakah konten masih enak dibaca dan tidak overflow.
Di layar kecil, beberapa layout multi-kolom saya ubah jadi satu kolom, dan beberapa komponen saya sesuaikan lagi supaya tetap enak dipandang.

# Pertanyaan Reflektif

## 1. Penggunaan Semantic HTML5

Saya pakai elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`.

`<section>` saya pakai untuk membagi halaman berdasarkan bagian utama, misalnya About, Skills, dan Experience. `<article>` saya pakai untuk konten yang punya konteks sendiri, seperti tiap kategori di Skills dan tiap pengalaman di Experience.

Buat saya, semantic HTML bikin struktur website lebih gampang dipahami karena elemen HTML-nya sendiri sudah menjelaskan peran konten di dalamnya. Kode juga jadi lebih gampang dirawat karena struktur dokumen dan tampilan visual jadi lebih terpisah jelas.

## 2. Tantangan dalam Membuat Responsive Design

Tantangan terbesarnya bagi saya adalah menyesuaikan layout desktop ke ruang yang jauh lebih sempit di HP.

Beberapa bagian website saya buat multi-kolom di desktop. Kalau layout itu dipertahankan di layar kecil, konten jadi terlalu sempit dan susah dibaca. Makanya di breakpoint `768px` dan `600px`, saya ubah beberapa layout jadi satu kolom dan saya sesuaikan ukuran elemennya.

Dalam menentukan perubahan itu, saya pertimbangkan hierarki informasi dan keterbacaan, supaya mata yang baca tidak lelah dan bingung. Informasi tetap saya pertahankan semua, cuma ukuran dan posisinya yang saya ubah.

Saya juga cek di beberapa ukuran layar berbeda, cari tahu apakah ada elemen yang terlalu rapat atau teks yang susah dibaca.

Dari proses gonta-ganti ukuran layar ini saya jadi paham: responsive design itu soal mempertimbangkan struktur dan prioritas informasi saat ukuran layar berubah, bukan sekadar mengecilkan semuanya.

## 3. Keterbatasan Static Web

Yang paling saya rasakan adalah konten masih ditulis langsung di source code HTML.
Untuk portofolio dengan informasi yang masih terbatas, ini masih oke. Tapi begitu jumlah project atau pengalaman bertambah, update konten jadi tidak praktis karena tiap perubahan harus langsung ke source code.

Ke depannya saya ingin menambahkan bagian backend dan database (setidaknya itu pemahaman saya sekarang), supaya informasi seperti project dan experience bisa disimpan sebagai data dan ditampilkan secara dinamis.

Saya juga ingin menambahkan bagian project dan contact form yang bisa menerima pesan dari pengunjung (harapannya sih tawaran internship, hehehe), lalu diproses lewat backend. Dengan begitu website-nya bisa lebih interaktif dan datanya bisa diolah.

# AI Disclosure

## Penggunaan AI

Saya pakai ChatGPT sebagai AI assistant selama pengerjaan project ini, terutama untuk brainstorming, debugging, dan mengevaluasi implementasi HTML dan CSS dari video YouTube yang jadi inspirasi website ini.
AI saya jadikan alat bantu untuk eksplorasi solusi dan memahami baris kode yang belum saya pahami.

Beberapa hal yang dibantu AI:

- Eksplorasi CSS Grid dan Flexbox.
- Diskusi pendekatan responsive design.
- Eksplorasi implementasi mobile navigation pakai HTML dan CSS.
- Analisis masalah pada navigation indicator.
- Debugging behavior CSS.
- Masukan soal spacing, positioning, typography, dan user experience.
- Membantu memahami video YouTube referensi coding saya.
- Membantu implementasi beberapa bagian CSS yang belum saya kuasai, seperti navigation indicator di navbar.

## Pendekatan Penggunaan AI

Saya pakai pendekatan iterative prompting. Kalau ketemu masalah atau kebutuhan tertentu, saya kasih konteks struktur code saya saat itu dan behavior yang saya mau. AI saya minta bantu menganalisis kemungkinan penyebab masalah atau kasih alternatif pendekatan.

Setelah dapat saran, saya terapkan ke project dan langsung saya uji. Kalau hasilnya tidak sesuai, saya analisis ulang dan modifikasi lagi.
AI di sini jadi partner eksplorasi saya untuk debugging dan memahami kode dari tutorial YouTube yang belum saya mengerti.

## Keterbatasan AI yang Ditemukan

Saran AI tidak selalu bisa langsung dipakai di project saya. AI belum tentu bisa membuat solusi yang cocok dengan struktur HTML dan CSS yang sudah saya kerjakan sebelumnya. Ubah satu selector atau property CSS saja bisa berdampak ke elemen lain yang sebelumnya sudah jalan baik.

AI juga tidak selalu bisa menilai apakah hasil visualnya sudah sesuai desain yang saya mau. Jadi testing langsung di browser tetap perlu, untuk menemukan masalah yang cuma kelihatan setelah kode dijalankan.

## Perbaikan Manual

Setelah dapat saran dari AI, saya lakukan beberapa penyesuaian manual:

- Menyesuaikan selector dengan struktur HTML yang sebenarnya.
- Mengubah positioning dan spacing beberapa elemen.
- Menyesuaikan ukuran typography dan komponen.
- Memperbaiki behavior layout di tiap breakpoint.
- Menguji mobile navigation langsung.
- Mengecek behavior navigation indicator.
- Mengganti implementasi yang hasilnya tidak sesuai kebutuhan.
- Visual testing untuk memastikan hasil akhir sesuai desain yang saya mau.

## Evaluasi Penggunaan AI

AI membantu mempercepat proses eksplorasi saya. Terakhir kali saya pegang HTML dan CSS itu waktu SMP, jadi AI membantu saya refresh lebih cepat sambil menjelaskan video YouTube yang sedang saya tonton.

Tapi pakai AI juga bikin saya harus lebih teliti waktu verifikasi. Saya tidak bisa asal percaya jawaban AI dan berasumsi kodenya pasti cocok dengan project saya.

Dari project ini saya belajar soal tanggung jawab dalam pakai AI. AI paling efektif jadi development assistant dan learning partner, bisa menjelaskan konsep dan membantu cari kemungkinan penyebab masalah, dan sejujurnya sekarang AI hampir bisa mengerjakan apapun di webdev. Tapi developer tetap harus paham kodenya sendiri, menguji hasilnya, dan menentukan sendiri apakah solusi itu benar-benar cocok untuk kebutuhan project.

## Kesimpulan

Project ini mengajarkan saya membangun static website dengan HTML5 dan CSS3, mulai dari menyusun struktur HTML, membangun layout pakai Grid dan Flexbox, sampai menerapkan responsive design dan animasi lewat CSS.

Di luar sisi teknis, project ini juga jadi pengalaman saya memakai AI secara kritis. Terjun langsung membuat saya sadar: output AI perlu saya pahami, uji, dan sesuaikan dulu sebelum dipakai. Keputusan akhir soal cara mengintegrasikan kode itu tetap ada di tangan developer, supaya hasilnya konsisten dan tidak terasa seperti web yang "slop".
