Name : Muhammmad Akmal Haqqani

NPM : 2506548295

Class : PBP D

# Personal Portfolio Akmal

Website portofolio pribadi saya yang dibuat pakai HTML5 dan CSS3 untuk Tugas Individu 1 mata kuliah Pemrograman Berbasis Platform, Fakultas Ilmu Komputerm Universitas Indonesia.
Isinya informasi pribadi, kemampuan teknis, pengalaman, proyek, dan kontak, semua dalam satu halaman yang responsif.

## Deskripsi

Saya bikin project ini untuk latihan HTML5 dan CSS3 dalam membangun static website. lalu di Tugas 2 saya kembangkan lagi jadi aplikasi Django supaya data project-nya tidak lagi hardcoded di HTML, 
disini saya fokus ngembangin di struktur halaman yang rapi dan layout yang tetap enak dilihat baik di desktop maupun di HP.
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
## TUGAS 1

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

# Pertanyaan Reflektif
## TUGAS 2

## 1. Alur dari Request sampai Data Tampil di Browser

Ketika saya buka halaman Projects, browser saya mengirim HTTP request ke URL `/projects/`. Request ini pertama diproses lewat `portofolio/urls.py`, URL dispatcher utama project yang mencocokkan URL request dengan pattern yang tersedia. Untuk URL yang jadi tanggung jawab app `main`, routing-nya saya teruskan lewat `include()` ke `main/urls.py`.
 
Di `main/urls.py`, Django mencocokkan lagi URL `/projects/` ke pattern yang saya definisikan, lalu diarahkan ke view `show_projects` di `main/views.py`. Saya kasih nama route ini `show_projects` juga, jadi di template saya bisa panggil pakai `{% url 'main:show_projects' %}` tanpa hardcode URL.
 
Di dalam `show_projects`, saya ambil data project lewat `Project.objects.all()`. `Project` adalah model yang saya definisikan di `main/models.py`, dan `objects` adalah manager bawaan Django untuk berinteraksi dengan model lewat Django ORM. Query ini menghasilkan QuerySet yang merepresentasikan data project dari database.
 
Data itu saya masukkan ke context dengan nama `project_list`, lalu saya kirim ke template `projects.html` pakai `render()`. Django Template Engine yang memproses template ini bersama context-nya. Saya loop pakai `{% for project in project_list %}` supaya tiap object `Project` ditampilkan pakai struktur HTML yang sama, judul, kategori, deskripsi, tech stack, achievement, tahun, dan link, semua saya ambil dari atribut object-nya langsung. Saya juga tambahkan `{% empty %}` untuk kondisi kalau belum ada project di database, jadi halaman tetap kasih informasi ke pengguna.
 
Setelah template selesai diproses, Django menghasilkan HTML yang sudah dirender dan mengembalikannya sebagai HTTP response ke browser. Browser yang mengurus render HTML itu bersama CSS dan aset lain yang dibutuhkan, sampai halaman Projects tampil ke pengguna.
 
Kalau saya ringkas prosesnya akan dimulai dari `urls.py` menangani routing request, view menangani proses request dan menyiapkan data, model merepresentasikan struktur data yang berinteraksi dengan database lewat ORM, template mengatur cara data itu dipresentasikan ke pengguna.

## 2. Kenapa Data Project Disimpan di Model, Bukan Ditulis Langsung di Template

kenapa kita simpan data project di model itu karena model dan template punya responsibility yang berbeda. Model dipakai untuk mendefinisikan struktur data aplikasi dan template dipakai untuk menentukan cara data itu ditampilkan ke pengguna.
 
Di Tugas 2 ini, saya definisikan model `Project` di `main/models.py` dengan field `title`, `category`, `description`, `tech_stack`, `achievement`, `github_url`, `external_url`, `year`, dan `image`. Data dari model ini disimpan di database. Template `projects.html` sendiri tidak menyimpan informasi tiap project secara langsung, dia hanya menerima data dari view lewat context dan menampilkannya pakai template syntax(ini contoh sedikit saja untuk gambaran yaa):
 
```django
{% for project in project_list %}
    {{ project.title }}
    {{ project.description }}
{% endfor %}
```
 
Dengan struktur seperti ini, jumlah project yang ditampilkan bisa bertambah tanpa saya perlu bikin elemen HTML baru satu-satu. Kalau saya tambah project baru lewat database atau Django Admin, data itu langsung terpakai struktur template yang sama.
 
Sebaliknya, kalau semua informasi project saya tulis langsung di template, tiap kali menambah atau mengubah project saya harus ubah HTML secara manual. Data dan presentation-nya jadi tercampur, dan makin susah dikelola begitu jumlah project bertambah.
 
Pemisahan ini juga bikin data `Project` bisa saya pakai lagi untuk fitur lain nanti, misalnya halaman detail project, pencarian, filter kategori, urut berdasarkan tahun, atau saya kelola lewat Django Admin, tanpa perlu ubah struktur dasar template tiap kali datanya berubah.
 
jadi kita menyimpan data di model itu untuk memisahkan tanggung jawab data dan tampilan, sementara template-nya sendiri jadi reusable karena satu struktur HTML bisa dipakai untuk banyak object `Project`.

## 3. Beda `makemigrations` dan `migrate`

`makemigrations` dan `migrate` adalah dua perintah Django yang berkaitan dengan perubahan struktur database, dan ada perbedaan dalam fungsinya.
 
`makemigrations` saya pakai untuk membuat migration file berdasarkan perubahan yang saya lakukan di `models.py`. Django mendeteksi perubahan itu dan menghasilkan instruksi perubahan schema database dalam bentuk migration. Di tahap ini, struktur database saya belum berubah.
 
Setelah migration dibuat, saya jalankan `migrate`. Perintah ini yang menerapkan migration yang tersedia ke database, jadi perubahan struktur yang didefinisikan di migration benar-benar dieksekusi ke database.
 
Contoh nya jika kitalihat di Tugas 2 ketika waktu saya bikin model `Project`, saya jalankan `python manage.py makemigrations`. Django membuat migration yang berisi operasi untuk membangun struktur yang dibutuhkan model `Project`. Setelah itu saya jalankan `python manage.py migrate`, baru perubahan itu diterapkan ke database dan tabel untuk model `Project` bisa dipakai aplikasi.
 
Hal yang sama berlaku waktu saya menambahkan field `image` ke model `Project`. Perubahan di `models.py` itu harus saya buat jadi migration dulu lewat `makemigrations`, baru saya terapkan ke database lewat `migrate`.
 
Pemisahan dua proses ini membuat perubahan schema database tercatat sebagai migration yang terstruktur dan bisa diterapkan secara konsisten, jadi perubahan model di aplikasi saya tetap terkontrol.


# Pertanyaan Reflektif
## TUGAS 3

## 1. Kenapa Pakai 'ModelForm', bukan Form HTML Manual

`ModelForm` saya pakai karena form-nya bisa langsung dibuat berdasarkan model Django yang sudah saya definisikan, jadi saya tidak perlu menulis tiap field secara manual pakai HTML. `ModelForm` juga otomatis menangani validasi data sesuai tipe field di model, dan langsung bisa dipakai untuk menyimpan data ke database lewat method `save()`. Ini bikin kode saya lebih ringkas dan mengurangi risiko field di form nggak sinkron dengan field di model, karena keduanya sumbernya sama.

Soal `{% csrf_token %}`, ini wajib saya tambahkan di form saya karena fungsinya melindungi dari serangan Cross-Site Request Forgery (CSRF). Django mengecek token ini setiap ada request POST masuk, untuk memastikan request itu benar-benar berasal dari form di website saya sendiri, bukan dari website lain yang mencoba mengirim request atas nama saya menggunakan session yang sedang aktif di browser saya.

## 2. Kenapa JSON Lebih Disukai Dibanding XML

JSON lebih sering dipakai dibanding XML karena formatnya jauh lebih ringkas. JSON cukup pakai pasangan key-value dan array, tanpa tag pembuka-penutup seperti XML, jadi ukuran data yang dikirim lebih kecil dan lebih cepat diproses.

Struktur JSON juga mirip banget sama object literal di JavaScript, jadi frontend (terutama yang berbasis JavaScript) bisa langsung parsing JSON ini jadi object tanpa parsing tambahan yang ribet seperti di XML. Kombinasi ukuran yang lebih kecil dan kemudahan parsing ini yang bikin JSON jadi pilihan default untuk pertukaran data lewat API di web modern, termasuk di endpoint JSON yang saya buat di portofolio saya.

## 3. Alur View yang Mengembalikan Data dalam Bentuk JSON(saya menggunakan case projects)

Ketika saya mengakses endpoint JSON portofolio saya, yaitu `/api/projects/`, request ini diproses lewat `urls.py` yang mengarahkannya ke view `get_projects_json` di `main/views.py`. View ini berbeda dengan `show_projects` yang saya gunakan untuk menampilkan halaman Projects dalam bentuk HTML. Di dalam `get_projects_json`, saya mengambil data `Project` dari database lewat `Project.objects.all()`.

Object `Project` hasil query ini masih berupa Python object Django, bukan format yang bisa langsung saya kirim lewat HTTP sebagai JSON. Di sinilah proses serialization saya perlukan. Saya menggunakan `django.core.serializers.serialize("json", projects)` untuk mengubah QuerySet tersebut menjadi string JSON. Serialization ini menerjemahkan data dari model Django beserta field-nya menjadi representasi data yang mengikuti format JSON.

Setelah datanya diserialize, saya mengembalikannya lewat `HttpResponse` dengan `content_type="application/json"`, supaya browser atau client yang mengakses endpoint tersebut tahu bahwa response yang dikirim berupa JSON, bukan HTML biasa.

Serialization ini diperlukan karena object hasil query Django belum berbentuk data JSON yang bisa langsung dikirim sebagai response. Object Django perlu diterjemahkan terlebih dahulu menjadi representasi data yang terdiri dari struktur JSON seperti object, array, string, dan number. Setelah proses tersebut selesai, hasilnya dapat dikirim melalui HTTP sebagai JSON dan digunakan oleh client yang membutuhkannya.

# AI Disclosure

## TUGAS 1
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

## Tugas 2
## Penggunaan AI

Untuk Tugas 2, saya pakai ChatGPT di dua konteks berbeda. Pertama waktu saya bingung soal positioning CSS untuk bagian Projects, foto-nya kelihatan terlalu maju padahal urutan elemennya sudah benar. Kedua waktu saya mengerjakan bagian Django-nya sendiri: bikin model `Project`, view, test, sampai brainstorming fitur tambahan supaya bisa naik ke nilai 4.0.

Beberapa hal yang dibantu ChatGPT:
 
- Menjelaskan konsep `z-index`, `position: relative` vs `position: absolute`, dan CSS Grid dengan analogi sederhana, karena sebelumnya saya cuma ikut-ikutan video YouTube tanpa benar-benar paham logikanya.
- Membaca model `Project` yang sudah saya buat dan membantu saya memahami struktur kode saya sendiri.
- Membimbing saya menulis unit test untuk `Project`, dengan cara membandingkan ke test `Experience` yang sudah saya buat duluan.
- Brainstorming fitur tambahan yang bisa membuat submission ini "melampaui ekspektasi" sesuai rubrik nilai 4.0.
- Menjelaskan cara setup Django admin dan superuser supaya TA bisa login dan mencoba fitur tambah data.
- Menjelaskan ulang alur request Django dari `urls.py` sampai halaman tampil, dengan gaya cerita supaya saya lebih gampang inget.

## Pendekatan Penggunaan AI

Saya pakai pendekatan yang sama seperti Tugas 1, iterative prompting, tapi kali ini saya eksplisit minta di awal supaya ChatGPT tidak langsung kasih kode jadi. jadi saya minta dia analisis file yang sudah saya kembangkan, pahami strukturnya dulu, terus bantu saya "develop".
 
Untuk bagian CSS, saya jelaskan gejala yang saya lihat (foto kedepan padahal indexing oke), lalu saya tanya konsep di baliknya satu-satu sampai saya paham analoginya.
 
Untuk bagian testing, saya awalnya agak bingung, jadi saya kasih tahu ChatGPT saya sudah punya test untuk `Experience` dari tugas 1 dan saya mau bikin yang mirip tapi disesuaikan ke field model `Project`. Setelah saya coba sendiri dan selesai, saya baru tanya cara menjalankannya.
 
## Keterbatasan AI yang Ditemukan

Penjelasan pertama ChatGPT soal z-index dan positioning masih terlalu teknis buat saya, saya sampai minta diulang pakai bahasa yang lebih sederhana. Ini nunjukin AI tidak otomatis tahu level pemahaman saya di awal, saya yang harus aktif bilang kalau penjelasannya belum cukup jelas.
 
Untuk bagian nilai 4.0, saran pertama ChatGPT (fitur tambah project) menurut saya sendiri masih terasa seperti fitur dasar yang seharusnya memang ada, bukan sesuatu yang kreatif. Saya yang mempertanyakan itu balik ke ChatGPT sebelum akhirnya kami sama-sama sampai ke ide Django Admin sebagai fitur ekstra yang lebih pantas disebut "melampaui ekspektasi".
 
Sama seperti Tugas 1, ChatGPT juga tidak bisa memastikan hasil test saya benar-benar cover semua kondisi yang dibutuhkan rubrik. Saya tetap yang menjalankan `python manage.py test` sendiri dan memastikan semuanya lulus, mungkin jika dalam penggunaaan agentic AI itu akan bisa run sedniri, namun dalam LLM nampaknhya belum punya kapabilitas untuk eksekusi langsung.

## Perbaikan Manual

Setelah diskusi dengan ChatGPT, saya sendiri yang:
 
- Menulis model `Project` dengan field dan tipe data sesuai kebutuhan saya (termasuk `UUIDField` sebagai primary key dan method `tech_list()` untuk parsing `tech_stack`).
- Menulis dan menyesuaikan unit test untuk `Project` berdasarkan pola test `Experience`, disesuaikan ke tiga kasus wajib: URL bisa diakses dengan template yang benar, data project muncul saat ada data, dan pesan kondisi kosong muncul saat belum ada data.
- Menjalankan `makemigrations` dan `migrate` sendiri, lalu mengecek hasilnya di database.
- Setup Django Admin dan superuser secara manual, lalu mengetes sendiri alur login dan tambah data lewat admin sebelum menganggap fitur ini selesai.
- Memutuskan sendiri untuk tidak memakai saran pertama ChatGPT (form tambah project di halaman publik) karena saya menilai itu belum cukup "di luar ekspektasi" untuk standar nilai 4.0.

## Evaluasi Penggunaan AI

Untuk Tugas 2, ChatGPT paling membantu di menjelaskan konsep CSS yang selama ini saya pakai tanpa saya pahami betul, dan jadi lawan diskusi waktu saya mikirin fitur tambahan yang benar-benar bernilai lebih, bukan sekadar checklist.
 
Yang saya pelajari, AI bisa kasih ide awal, tapi keputusan mana ide yang layak tetap ada di saya. Waktu saya merasa saran pertamanya masih terlalu basic, saya tidak langsung terima, saya tanya balik dan diskusikan lagi sampai ketemu solusi yang saya rasa memang pantas.

## Log Prompting

Log percakapan lengkap dengan ChatGPT untuk Tugas 2 (CSS positioning, pengembangan model `Project`, unit test, hingga diskusi fitur Django Admin) saya lampirkan di link ini.
Link Chat GPT: https://chatgpt.com/share/6aa6ae4d-2a44-83ec-881f-c6a06e21935a

## Kesimpulan
 
Tugas 1 kita fokus pada HTML5 dan CSS3, dengan membangun struktur dan membangun layout pakai Grid dan Flexbox, sampai menerapkan responsive design dan animasi lewat CSS. Tugas 2 melanjutkannya dengan mengubah bagian Projects dari data statis di HTML jadi data dinamis lewat model, view, dan template Django, lengkap dengan unit test dan Django Admin.


# AI Disclosure
## Tugas 3
## Penggunaan AI

Untuk Tugas 3, saya pakai ChatGPT terutama untuk memahami alur kerja Django secara menyeluruh (yang tadinya masih saya "kureng paham" dari awal) dan brainstorming fitur tambahan supaya bisa mengejar nilai 4.0.

Beberapa hal yang dibantu ChatGPT:

- Menjelaskan requirement lengkap Tugas 3 berdasarkan dua PDF tutorial yang saya berikan.
- Menjelaskan ulang logika kerja Tutorial 3 dari awal, dari request masuk sampai objeknya muncul di halaman.
- Menjelaskan alur Django secara menyeluruh, dari cara kode sampai tampil di web, alur request, sampai urls path, karena saya masih bingung integrasinya untuk lab yang harus dibangun ulang dari Tutorial 1 sampai 3.
- Membantu saya menentukan Experience sebagai bagian yang saya pakai untuk requirement Tugas 3.
- Brainstorming fitur tambahan yang bisa mendorong nilai ke 4.0, yang saya lanjutkan dengan implementasi create, update, delete untuk Experience.
- Menjelaskan cara kerja pengiriman data JSON dan cara implementasinya di code.
- Menjelaskan konsep search, sorting, dan template inheritance.
- Membantu saya evaluasi mana fitur tambahan yang worth diimplementasikan dan mana yang tidak.

## Pendekatan Penggunaan AI

Saya mulai dengan kasih ChatGPT dua PDF tutorial sebagai konteks, lalu minta dia jelaskan detail requirement Tugas 3 supaya saya paham target nilai 4.0-nya dari awal, bukan baru cari tahu di tengah jalan.

Karena saya masih belum paham alur Django secara keseluruhan, dari request sampai tampil di web, urls path, sampai integrasi antar tutorial, saya minta dijelaskan dari nol dulu sebelum masuk ke implementasi. Setelah itu, saya juga sempat minta ChatGPT menyimpan requirement tugas dalam format JSON sebagai konteks percakapan yang lebih ringkas, dan minta dia sebutkan file mana saja yang perlu saya kasih supaya dia tahu kondisi kode saya saat itu, karena state project saya sedikit beda dari Tutorial 3 murni.

Untuk tiap fitur, CRUD, JSON delivery, search, sorting, template inheritance, saya kerjakan satu-satu, saya implementasikan sendiri, lapor progress ke ChatGPT, baru tanya konsep atau langkah berikutnya. Misalnya soal sorting, saya sempat tanya balik apakah itu butuh input data baru atau tidak, supaya saya tidak salah asumsi sebelum implementasi.

Untuk fitur tambahan yang diusulkan ChatGPT, termasuk drag & drop, saya tidak langsung terima. Saya pertimbangkan dulu apakah fitur itu cocok dan sepadan dengan effort-nya, sampai akhirnya saya putuskan sendiri fitur mana yang saya pakai.

## Keterbatasan AI yang Ditemukan

Waktu ChatGPT usul fitur drag & drop untuk reorder data, saya mempertanyakan balik dampaknya ke performa, karena tiap drag pasti akan update database terus-menerus. ChatGPT sendiri tidak otomatis mempertimbangkan trade-off ini di awal, saya yang harus tanya dan menilai sendiri apakah fitur itu sepadan dengan risikonya.

Sama seperti Tugas 1 dan 2, ChatGPT juga tidak bisa langsung menjamin implementasi saya benar, dia cuma bisa menjelaskan konsep dan kasih arahan. Saya tetap yang harus coding, commit, dan cek sendiri apakah fitur-fitur itu benar-benar jalan sesuai checklist.

## Perbaikan Manual

Setelah diskusi dengan ChatGPT, saya dipandu gpt untuk code melakukan:

- Implementasi create, update, delete untuk Experience berdasarkan pemahaman alur Django yang saya dapat.
- Membuat endpoint dan logic untuk JSON delivery (`get_json_experience`), termasuk serialize dan loop datanya.
- Implementasi fitur filter kategori lewat button pemisah untuk Experience.
- Implementasi dropdown sorting untuk data Experience.
- Refactor seluruh file HTML supaya extend dari root template, sesuai konsep template inheritance yang saya pelajari(ini dari tutorial 3).
- Memutuskan sendiri untuk tidak memakai fitur drag & drop yang diusulkan ChatGPT, setelah saya pertimbangkan dampaknya ke beban database.

## Evaluasi Penggunaan AI

Untuk Tugas 3, ChatGPT paling membantu di bagian yang paling saya bingungkan dari awal, yaitu memahami alur Django.

Yang saya pelajari lagi, sama seperti tugas sebelumnya, AI bisa kasih banyak ide fitur tambahan, tapi saya yang harus filter mana yang benar-benar relevan dan mana yang cuma menambah kompleksitas tanpa manfaat sebanding, seperti kasus drag & drop itu.

## Log Prompting

Log percakapan lengkap dengan ChatGPT untuk Tugas 3 (pemahaman requirement, alur Django, implementasi CRUD, JSON delivery, search, sorting, sampai evaluasi fitur tambahan) saya lampirkan di link ini.
Link Chat GPT: https://chatgpt.com/share/6aac2250-7ac0-83ec-a4d2-f4f56bb106df

## Kesimpulan
 
Tugas 1 kita fokus pada HTML5 dan CSS3, dengan membangun struktur dan membangun layout pakai Grid dan Flexbox, sampai menerapkan responsive design dan animasi lewat CSS. Tugas 2 melanjutkannya dengan mengubah bagian Projects dari data statis di HTML jadi data dinamis lewat model, view, dan template Django, lengkap dengan unit test dan Django Admin. Tugas 3 saya lanjutkan lagi dengan menambahkan CRUD penuh (create, update, delete) untuk Experience, endpoint JSON, fitur filter kategori dan sorting, serta refactor template supaya seluruh halaman extend dari satu root template lewat template inheritance.