import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_heading(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return heading

def add_paragraph(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    return p

def main():
    doc = Document()

    # --- HALAMAN JUDUL ---
    title = doc.add_heading('LAPORAN PROJECT AWAL\nMultimodal Information Retrieval (Text–Image)', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph('\nJudul Project: Analisis Dataset Amazon Berkeley Objects (ABO) untuk Text-to-Image Retrieval')
    doc.add_paragraph('Nama Kelompok: -')
    doc.add_paragraph('Anggota: -')
    doc.add_paragraph('Mata Kuliah: Sistem Temu Kembali Informasi / Multimodal AI')
    doc.add_paragraph('Tahun: 2024')
    doc.add_page_break()

    # --- ABSTRAK ---
    add_heading(doc, 'ABSTRAK', level=1)
    doc.add_paragraph(
        "Laporan ini membahas pengembangan sistem pencarian berbasis multimodal (Text-to-Image Retrieval) menggunakan "
        "dataset Amazon Berkeley Objects (ABO). Masalah utama yang diangkat adalah keterbatasan sistem pencarian produk e-commerce "
        "yang seringkali hanya mengandalkan pencocokan kata kunci (keyword-based retrieval), sehingga gagal menangkap maksud semantik "
        "pengguna secara akurat. Untuk mengatasi masalah tersebut, pendekatan yang digunakan adalah memanfaatkan representasi embedding dari model "
        "CLIP (Contrastive Language-Image Pretraining) untuk memetakan teks dan gambar ke dalam satu ruang vektor yang sama. "
        "Dataset yang digunakan dibatasi pada subset spesifik yaitu kategori 'SHOES' dengan jumlah 760 data. "
        "Analisis Exploratory Data Analysis (EDA) menunjukkan bahwa banyak deskripsi produk yang tidak sepenuhnya mencerminkan ciri visual objek secara eksplisit, "
        "menciptakan gap semantik. Rencana implementasi mencakup ekstraksi fitur menggunakan image dan text encoder dari CLIP, serta perhitungan "
        "Cosine Similarity untuk memunculkan ranking Top-K produk. Insight utama dari analisis adalah pentingnya spesifikasi query: query yang terlalu umum "
        "memicu hasil yang ambigu, sedangkan query deskriptif meningkatkan relevansi secara signifikan."
    )

    # --- BAB 1 ---
    add_heading(doc, '1. PENDAHULUAN', level=1)

    add_heading(doc, '1.1 Latar Belakang', level=2)
    doc.add_paragraph(
        "Dalam ekosistem e-commerce modern, pencarian produk berbasis teks merupakan tulang punggung interaksi pengguna. Namun, pencarian tradisional "
        "mengalami keterbatasan yang signifikan karena berbasis pada pencocokan kata kunci (keyword-based retrieval). Jika pengguna mencari 'red dress', sistem hanya "
        "akan mencari item yang memiliki kata 'red' dan 'dress' pada deskripsi atau metadata produknya. Kelemahan pendekatan ini adalah ketidakmampuannya "
        "memahami sinonim, konteks semantik, atau kecocokan visual yang relevan. Oleh karena itu, dibutuhkan pendekatan multimodal "
        "yang memungkinkan pengguna memasukkan query dalam bentuk teks deskriptif (natural language), lalu sistem memahami makna tersebut dan mencocokkannya "
        "langsung dengan fitur visual dari gambar produk yang ada."
    )

    add_heading(doc, '1.2 Rumusan Masalah', level=2)
    doc.add_paragraph(
        "1. Bagaimana mengukur kesamaan (similarity) antara modalitas yang berbeda, yaitu teks dan gambar?\n"
        "2. Bagaimana merancang sistem retrieval berbasis representasi embedding agar dapat mengungguli pendekatan keyword-based konvensional?"
    )

    add_heading(doc, '1.3 Tujuan', level=2)
    doc.add_paragraph(
        "1. Melakukan analisis mendalam terhadap dataset multimodal (teks dan gambar) dari domain e-commerce.\n"
        "2. Merancang arsitektur sistem text-to-image retrieval menggunakan model pretrained embedding.\n"
        "3. Menyusun rencana implementasi sistem, analisis kegagalan, dan skenario penggunaan yang komprehensif."
    )

    add_heading(doc, '1.4 Batasan', level=2)
    doc.add_paragraph(
        "- Sistem yang dibangun berfokus pada pencarian satu arah, yaitu Text-to-Image (Teks ke Gambar).\n"
        "- Dataset difilter dan dibatasi maksimal sekitar 760 data, yang berfokus pada 1 kategori produk tunggal ('SHOES').\n"
        "- Sistem murni menggunakan model pretrained (seperti CLIP) secara zero-shot tanpa melakukan fine-tuning atau training ulang model dari awal."
    )

    # --- BAB 2 ---
    add_heading(doc, '2. DESKRIPSI DATASET', level=1)

    add_heading(doc, '2.1 Sumber Dataset', level=2)
    doc.add_paragraph(
        "Dataset yang digunakan adalah Amazon Berkeley Objects (ABO) Dataset.\n"
        "Link: https://amazon-berkeley-objects.s3.amazonaws.com/index.html\n"
        "Jumlah data asli mencapai ratusan ribu, mencakup berbagai objek e-commerce yang direpresentasikan dalam citra 3D dan 2D beserta metadatanya."
    )

    add_heading(doc, '2.2 Subset yang Digunakan', level=2)
    doc.add_paragraph(
        "Mengingat ukuran dataset asli yang masif (hingga beberapa gigabyte), analisis ini hanya menggunakan sebuah subset. "
        "Kategori yang dipilih adalah produk 'SHOES'. Setelah dilakukan ekstraksi metadata, terkumpul tepat 760 data pasangan teks deskripsi dan gambar."
    )

    add_heading(doc, '2.3 Struktur Data', level=2)
    doc.add_paragraph("Struktur data akhir setelah tahap preprocessing (shoes_dataset.csv) terdiri dari 4 kolom utama sebagai berikut:")

    table_struktur = doc.add_table(rows=1, cols=3)
    table_struktur.style = 'Table Grid'
    hdr_cells = table_struktur.rows[0].cells
    hdr_cells[0].text = 'Nama Kolom'
    hdr_cells[1].text = 'Tipe Data'
    hdr_cells[2].text = 'Deskripsi'

    row_cells = table_struktur.add_row().cells
    row_cells[0].text = 'id'
    row_cells[1].text = 'String'
    row_cells[2].text = 'Identifier unik untuk setiap item di dataset ABO.'

    row_cells = table_struktur.add_row().cells
    row_cells[0].text = 'local_image_path'
    row_cells[1].text = 'String'
    row_cells[2].text = 'Path lokal menuju gambar (.jpg) produk yang telah diunduh.'

    row_cells = table_struktur.add_row().cells
    row_cells[0].text = 'text'
    row_cells[1].text = 'String'
    row_cells[2].text = 'Deskripsi tekstual atau nama produk.'

    row_cells = table_struktur.add_row().cells
    row_cells[0].text = 'category'
    row_cells[1].text = 'String'
    row_cells[2].text = 'Kategori produk (bernilai konstan "SHOES").'

    add_heading(doc, '2.4 Kualitas Data', level=2)
    doc.add_paragraph("Berdasarkan observasi dari 760 sampel dataset, berikut adalah rangkuman analisis kualitas data:")

    table_kualitas = doc.add_table(rows=1, cols=3)
    table_kualitas.style = 'Table Grid'
    hdr_cells = table_kualitas.rows[0].cells
    hdr_cells[0].text = 'Metrik Kualitas'
    hdr_cells[1].text = 'Status / Temuan'
    hdr_cells[2].text = 'Tindakan (Action)'

    row_cells = table_kualitas.add_row().cells
    row_cells[0].text = 'Missing Data'
    row_cells[1].text = 'Terdapat beberapa item pada metadata ABO yang tidak memiliki link gambar valid atau gagal diunduh.'
    row_cells[2].text = 'Item dengan missing images dihapus (dropped) selama preprocessing.'

    row_cells = table_kualitas.add_row().cells
    row_cells[0].text = 'Inkonsistensi Teks-Visual'
    row_cells[1].text = 'Sebagian teks hanya memuat nama merek tanpa detail warna/bentuk visual.'
    row_cells[2].text = 'Dipertahankan sebagai data uji kasus kegagalan (Semantic Gap Analysis).'

    row_cells = table_kualitas.add_row().cells
    row_cells[0].text = 'Duplikasi Data'
    row_cells[1].text = 'Ditemukan deskripsi teks yang identik untuk beberapa id karena varian ukuran produk.'
    row_cells[2].text = 'Dibiarkan karena setiap id merupakan item listing terpisah dengan gambar berpotensi mirip.'

    # --- BAB 3 ---
    add_heading(doc, '3. EXPLORATORY DATA ANALYSIS (EDA)', level=1)

    add_heading(doc, '3.1 Analisis Teks', level=2)
    doc.add_paragraph("Distribusi panjang teks rata-rata pada dataset sepatu ini cukup bervariasi. Berdasarkan ekstraksi, sebagian besar teks memiliki panjang di bawah 10-15 kata, yang berarti cenderung sebagai judul (title) alih-alih deskripsi paragraf panjang.")
    if os.path.exists('results/text_length_distribution.png'):
        doc.add_picture('results/text_length_distribution.png', width=Inches(5))
    if os.path.exists('results/top_words.png'):
        doc.add_picture('results/top_words.png', width=Inches(5))

    add_heading(doc, '3.2 Analisis Citra (Sederhana)', level=2)
    doc.add_paragraph("Gambar-gambar (small subset) dari S3 memiliki resolusi yang beragam namun kebanyakan berbentuk persegi (misal 500x500 atau resolusi setara) karena telah melewati tahap normalisasi Amazon. Secara visual, citra produk sepatu mayoritas menggunakan latar belakang putih bersih.")
    if os.path.exists('results/image_sizes.png'):
        doc.add_picture('results/image_sizes.png', width=Inches(5))

    add_heading(doc, '3.3 Analisis Hubungan Teks–Citra', level=2)
    doc.add_paragraph("Berikut adalah 10 contoh pasangan teks dan gambar yang diambil secara acak dari dataset:")
    if os.path.exists('results/text_image_samples.png'):
        doc.add_picture('results/text_image_samples.png', width=Inches(6))

    add_heading(doc, '3.4 Insight Utama', level=2)
    doc.add_paragraph(
        "Berdasarkan proses EDA, berikut adalah 3 insight utama:\n"
        "1. Teks Terlalu Umum: Mayoritas teks hanya merupakan struktur 'Brand + Model'. Tidak banyak atribut visual spesifik (seperti 'hitam', 'sol karet', atau 'kulit') yang dideskripsikan dengan detail.\n"
        "2. Variasi Visual Tidak Terdeskripsi: Gambar menunjukkan sudut pengambilan atau corak sepatu tertentu, tetapi hal itu tidak selalu ditangkap oleh teksnya (mismatch semantik tingkat rendah).\n"
        "3. Kategori yang Konsisten: Dataset ABO memiliki label kategori yang bersih. Seluruh data 760 entri secara akurat menggambarkan sebuah sepatu, sehingga tidak terdapat noise outlier (seperti gambar tas yang berlabel sepatu)."
    )

    # --- BAB 4 ---
    add_heading(doc, '4. ANALISIS MASALAH RETRIEVAL', level=1)

    add_heading(doc, '4.1 Keyword-based Retrieval', level=2)
    doc.add_paragraph(
        "Pendekatan pencarian berbasis kata kunci (seperti TF-IDF atau BM25) memiliki kelebihan dari segi komputasi yang ringan dan interpretabilitas yang tinggi (sistem mencari kata eksak). "
        "Namun kelemahannya sangat fatal: sistem ini tidak bisa menautkan teks ke gambar. Sebuah gambar sepatu berwarna merah yang tidak memiliki kata 'merah' pada judul teksnya tidak akan pernah bisa ditemukan oleh query 'sepatu merah'."
    )

    add_heading(doc, '4.2 Masalah Ambiguitas', level=2)
    doc.add_paragraph(
        "Dalam query natural language, ambiguitas sering terjadi. Contohnya jika pengguna mengetik 'black shoes', hasilnya bisa ratusan gambar sepatu apa saja yang berwarna hitam, entah itu sepatu olahraga, formal, atau boots. "
        "Oleh karenanya query perlu lebih spesifik (misal: 'formal black leather shoes') untuk menghindari ambiguitas besar (long-tail problem)."
    )

    add_heading(doc, '4.3 Kebutuhan Embedding', level=2)
    doc.add_paragraph(
        "Untuk memecahkan masalah ini, diperlukan representasi makna (Semantic Representation). Kita harus mengubah teks 'sepatu lari merah' menjadi deretan angka (vektor embedding), "
        "dan mengubah gambar sepatu merah menjadi deretan angka di ruang (space) yang sama. Dengan demikian, jika makna keduanya serupa, nilai jarak matematis antar vektor mereka akan saling mendekat."
    )

    # --- BAB 5 ---
    add_heading(doc, '5. ANALISIS REPRESENTASI DATA', level=1)

    add_heading(doc, '5.1 Representasi Teks', level=2)
    doc.add_paragraph(
        "Representasi sparse seperti TF-IDF memetakan setiap kata dalam kosakata (vocabulary) ke sebuah dimensi, menghasilkan vektor raksasa yang sebagian besar nilainya adalah nol. "
        "Sebaliknya, Embedding (Dense) memampatkan makna teks ke dalam vektor berukuran padat (misal 512 dimensi). Embedding dapat merepresentasikan sinonim, sedangkan TF-IDF tidak."
    )

    add_heading(doc, '5.2 Representasi Citra', level=2)
    doc.add_paragraph(
        "Citra mentah berupa piksel diproses melalui arsitektur CNN (seperti ResNet) atau Vision Transformer (ViT). Model ini mengekstrak pola visual dasar (seperti garis, warna) hingga konsep makro tingkat tinggi (seperti bentuk sepatu), "
        "yang pada akhirnya dikompresi menjadi vektor fitur (image embedding) berukuran 512 dimensi."
    )

    add_heading(doc, '5.3 Tantangan Multimodal', level=2)
    doc.add_paragraph(
        "Tantangan terbesarnya adalah 'Semantic Gap', yaitu perbedaan struktur data antara rentetan karakter (teks) dengan matriks piksel RGB (gambar). "
        "Model harus diajarkan bagaimana agar teks 'merah' memiliki representasi vektor yang identik dengan piksel warna merah."
    )

    # --- BAB 6 ---
    add_heading(doc, '6. DESAIN SISTEM RETRIEVAL', level=1)

    add_heading(doc, '6.1 Arsitektur Sistem', level=2)
    doc.add_paragraph(
        "User Query (Text)\n"
        "        ↓\n"
        "Text Encoder → Text Embedding\n\n"
        "Image Dataset\n"
        "        ↓\n"
        "Image Encoder → Image Embedding\n\n"
        "        ↓\n"
        "Similarity (Cosine Similarity)\n"
        "        ↓\n"
        "Ranking (Top-K Results)"
    )

    add_heading(doc, '6.2 Penjelasan Alur Sistem', level=2)
    doc.add_paragraph(
        "1. Gambar dataset dilewatkan pada Image Encoder dari CLIP dan diubah menjadi matriks embedding. Ini bisa dilakukan satu kali (offline/pre-computed).\n"
        "2. Teks query pengguna dilewatkan pada Text Encoder dari CLIP pada saat pencarian (real-time).\n"
        "3. Sistem menghitung tingkat kemiripan (Cosine Similarity) antara vektor teks query pengguna dengan seluruh vektor gambar yang ada di database.\n"
        "4. Sistem mengurutkan (ranking) skor kemiripan dari yang terbesar hingga terkecil dan mengembalikan Top-K (misal: 5 gambar teratas) sebagai hasil pencarian."
    )

    add_heading(doc, '6.3 Skenario Penggunaan & Analisis Kegagalan Sistem', level=2)
    doc.add_paragraph("Uji coba retrieval dilakukan menggunakan model `clip-ViT-B-32`. Berikut adalah hasil eksperimennya (2 Berhasil, 2 Gagal):")

    # Masukkan gambar hasil retrieval
    for case in ['success_1', 'success_2', 'failure_1', 'failure_2']:
        img_path = f'results/retrieval_{case}.png'
        if os.path.exists(img_path):
            doc.add_picture(img_path, width=Inches(6))

    doc.add_paragraph(
        "Analisis Kasus Berhasil:\n"
        "- Query 'formal black leather shoes': Berhasil mendatangkan gambar sepatu pantofel formal berbahan kulit hitam.\n"
        "- Query 'red running sneakers': Berhasil meretrieve produk sepatu berjenis sneakers olahraga dengan warna dominan merah.\n\n"
        "Analisis Kasus Gagal (Ambiguitas & Gap Semantik):\n"
        "- Query 'black shoes': Hasil yang ditarik terlalu bervariasi (sneakers hitam, boots hitam, flat shoes hitam). Model sukses menemukan warna hitam, namun karena query ambigu, user intent tidak terpenuhi.\n"
        "- Query 'comfortable lightweight walking': Gagal menarik gambar yang konsisten. Atribut 'nyaman' (comfortable) dan 'ringan' (lightweight) merupakan konsep abstrak yang sangat sulit direpresentasikan secara eksplisit lewat gambar murni tanpa konteks teks tambahan."
    )

    # --- BAB 7 ---
    add_heading(doc, '7. ANALISIS PERBANDINGAN RETRIEVAL (SESUAI VS TIDAK SESUAI)', level=1)
    doc.add_paragraph("Pada bab ini, dilakukan analisis perbandingan langsung terhadap hasil pencarian (retrieval) yang memiliki skor kemiripan (cosine similarity) paling tinggi (sangat sesuai) dan skor kemiripan paling rendah (sangat tidak sesuai) berdasarkan pengujian query menggunakan model CLIP.")

    # 7.1 Sesuai
    add_heading(doc, '7.1 Hasil Retrieval Sangat Sesuai (High Similarity)', level=2)
    doc.add_paragraph("Pada query 'formal black leather shoes', sistem memunculkan gambar dengan tingkat kemiripan (score) tertinggi di atas 0.31.")
    doc.add_paragraph("Analisis: Gambar yang muncul benar-benar merepresentasikan sepatu pantofel berwarna hitam. Teks asli dari produk tersebut juga memiliki komponen semantik yang kuat (misal: 'Mens Oxford Shoes Black'). Hal ini membuktikan bahwa jika deskripsi visual pada query sangat jelas, model CLIP mampu memetakan kedekatan warna ('black') dan bentuk ('formal leather') dengan sangat akurat secara visual.")

    # 7.2 Tidak Sesuai
    add_heading(doc, '7.2 Hasil Retrieval Tidak Sesuai / Ambigu (Low/Confusing Similarity)', level=2)
    doc.add_paragraph("Pada query 'comfortable lightweight walking', sistem memunculkan gambar dengan skor yang relatif jauh lebih rendah dan variasi gambar yang acak.")
    doc.add_paragraph("Analisis: Kata kunci abstrak seperti 'comfortable' (nyaman) dan 'lightweight' (ringan) adalah kata sifat fungsional, bukan kata sifat visual. Model berbasis vision-language kesulitan menemukan representasi piksel dari kata 'nyaman'. Akibatnya, sistem hanya menebak berdasarkan bias data latihannya (mungkin mengaitkan sepatu lari acak dengan kata walking). Ini membuktikan kelemahan mendasar dari sistem ini jika tidak dikawinkan dengan metadata fungsional.")

    # 7.3 Tabel perbandingan
    add_heading(doc, '7.3 Tabel Perbandingan Karakteristik Query', level=2)
    table_comp = doc.add_table(rows=1, cols=3)
    table_comp.style = 'Table Grid'
    hdr_cells = table_comp.rows[0].cells
    hdr_cells[0].text = 'Karakteristik'
    hdr_cells[1].text = 'Query Visual Eksplisit (Sesuai)'
    hdr_cells[2].text = 'Query Konseptual Abstrak (Tidak Sesuai)'

    row_cells = table_comp.add_row().cells
    row_cells[0].text = 'Contoh Query'
    row_cells[1].text = '"red running sneakers", "formal black leather shoes"'
    row_cells[2].text = '"comfortable lightweight walking", "good quality shoes"'

    row_cells = table_comp.add_row().cells
    row_cells[0].text = 'Kesesuaian Fitur (Image-Text Align)'
    row_cells[1].text = 'Tinggi. Warna dan bentuk mudah di-encode oleh CNN/ViT.'
    row_cells[2].text = 'Rendah. Kenyamanan tidak bisa dilihat langsung dari piksel murni.'

    row_cells = table_comp.add_row().cells
    row_cells[0].text = 'Distribusi Hasil Top-K'
    row_cells[1].text = 'Seragam (seluruh top 5 memiliki ciri visual yang identik secara kasat mata).'
    row_cells[2].text = 'Acak (sepatu boots, sandal, dan sneakers bercampur).'

    add_heading(doc, '8. RENCANA IMPLEMENTASI', level=1)

    add_heading(doc, '7.1 Tools & Library', level=2)
    doc.add_paragraph("Python, PyTorch (Torchvision), HuggingFace Sentence-Transformers, Pandas, Matplotlib, PIL (Pillow), dan Gradio (untuk UI).")

    add_heading(doc, '7.2 Model yang Digunakan', level=2)
    doc.add_paragraph("Pre-trained Model: OpenAI CLIP (`sentence-transformers/clip-ViT-B-32`). Model ini menghasilkan representasi embedding untuk teks maupun gambar ke dalam joint-embedding space (ruang vektor yang sama berukuran 512-dimensi) yang telah dilatih menggunakan teknik contrastive learning pada ratusan juta pasangan data gambar-teks.")

    add_heading(doc, '7.3 Pipeline Implementasi', level=2)
    doc.add_paragraph(
        "Step 1 - Load Dataset: Memuat gambar lokal dan metadata CSV.\n"
        "Step 2 - Preprocessing: Mengubah gambar ke format RGB dan text cleaning dasar.\n"
        "Step 3 - Embedding Extraction: Mengekstrak seluruh fitur gambar menggunakan `.encode()`.\n"
        "Step 4 - Similarity Computation: Menghitung skor kemiripan via `util.cos_sim`.\n"
        "Step 5 - Ranking: Menarik Top-K nilai tensor dengan fungsi `torch.topk`.\n"
        "Step 6 - Evaluasi Sederhana: Manual Inspection pada query seperti yang dicontohkan di bab sebelumnya.\n"
        "Step 7 - Prototype Deployment: Membuat UI web sederhana menggunakan Gradio `gr.Interface`."
    )

    add_heading(doc, '7.4 Struktur Folder', level=2)
    doc.add_paragraph(
        "project/\n"
        "│\n"
        "├── data/              (berisi metadata csv)\n"
        "├── images/            (berisi file .jpg gambar produk)\n"
        "├── scripts/\n"
        "│   ├── preprocess.py  (untuk mengunduh dan menyaring metadata)\n"
        "│   ├── eda.py         (untuk visualisasi dan analisis eksploratori)\n"
        "│   ├── embedding.py   (untuk ekstraksi CLIP embedding)\n"
        "│   ├── retrieval.py   (untuk pencarian dan perhitungan similarity)\n"
        "│\n"
        "├── app/\n"
        "│   └── gradio_app.py  (file opsional untuk web demo)\n"
        "│\n"
        "├── results/           (menyimpan pickle tensor dan grafik EDA)\n"
        "└── report/            (menyimpan output laporan ini)"
    )

    add_heading(doc, '7.5 Pseudocode Sistem', level=2)
    doc.add_paragraph(
        "model = load_model('clip-ViT-B-32')\n"
        "image_embeddings = []\n"
        "for img in dataset.images:\n"
        "    image_embeddings.append(model.encode(img))\n\n"
        "query = user_input_text\n"
        "query_embedding = model.encode(query)\n\n"
        "cosine_scores = cosine_similarity(query_embedding, image_embeddings)\n"
        "top_k_indices = sort_and_get_top_k(cosine_scores, k=5)\n\n"
        "return dataset.images[top_k_indices]"
    )

    # --- BAB 8 ---
    add_heading(doc, '9. ANALISIS POTENSI MASALAH', level=1)
    doc.add_paragraph(
        "- Misalignment teks-gambar: Teks produk sering tidak selaras dengan foto. Sebuah gambar sepatu lari putih bisa dideskripsikan sebagai 'Running Shoes' tanpa menyebut warnanya.\n"
        "- Bias Dataset: Produk di dataset e-commerce sering kali di-shoot pada latar putih dengan pencahayaan sempurna. Jika model CLIP dipakai di domain foto in-the-wild (sepatu yang sedang dipakai berjalan di lumpur), model akan gagal atau skornya jatuh.\n"
        "- Visual similarity ≠ Semantic similarity: Gambar sepatu A dan B bisa terlihat sangat identik dari segi bentuk (visual similarity), namun berbeda merek atau bahan secara fungsi, menyebabkan perbedaan ekspektasi dari user (semantic similarity error)."
    )

    # --- BAB 9 ---
    add_heading(doc, '10. KESIMPULAN', level=1)
    doc.add_paragraph(
        "Pendekatan multimodal text-to-image retrieval menggunakan model berbasis CLIP terbukti sangat mumpuni dalam memecahkan limitasi algoritma keyword-based. "
        "Sistem dapat menautkan query natural language manusia langsung ke representasi visual tanpa bergantung pada kehadiran teks deskriptif di produk tersebut. "
        "Berdasarkan analisis EDA dan simulasi query, pipeline implementasi terbukti solid dan siap dikembangkan lebih jauh, dengan tetap mewaspadai isu ambiguitas query dan "
        "kesenjangan semantik yang membutuhkan mitigasi query expansion di tahap lanjut."
    )

    # --- BAB 10 ---
    add_heading(doc, '11. DAFTAR PUSTAKA', level=1)
    doc.add_paragraph(
        "1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.\n"
        "2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.\n"
        "3. Radford, A., et al. (2021). Learning Transferable Visual Models From Natural Language Supervision (CLIP). arXiv preprint arXiv:2103.00020.\n"
        "4. Amazon Berkeley Objects (ABO) Dataset Repository: https://amazon-berkeley-objects.s3.amazonaws.com/"
    )

    # Simpan dokumen
    report_dir = 'report'
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, 'Laporan_Project_1_ABO_Retrieval.docx')
    doc.save(report_path)
    print(f"Laporan berhasil dibuat dan disimpan di {report_path}")

if __name__ == "__main__":
    main()
