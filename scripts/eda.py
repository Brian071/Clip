import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from PIL import Image

def main():
    data_path = 'data/shoes_dataset.csv'
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)

    if not os.path.exists(data_path):
        print("Dataset not found. Run preprocess.py first.")
        return

    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records.")

    # 1. Analisis Teks (Panjang Teks)
    df['text_length'] = df['text'].apply(lambda x: len(str(x).split()))

    plt.figure(figsize=(10, 6))
    sns.histplot(df['text_length'], bins=30, kde=True, color='skyblue')
    plt.title('Distribusi Panjang Teks Deskripsi Sepatu')
    plt.xlabel('Jumlah Kata')
    plt.ylabel('Frekuensi')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'text_length_distribution.png'))
    plt.close()

    # Analisis kata dominan
    all_words = ' '.join(df['text'].astype(str).tolist()).lower().split()
    # Filter stopwords sederhana
    stopwords = set(['for', 'and', 'with', 'women', 'men', 'shoes', 'the', 'in', 'of', 'to', 'a', '-', 'shoe'])
    words_filtered = [w for w in all_words if w not in stopwords and len(w) > 2]
    word_freq = Counter(words_filtered).most_common(20)

    words, counts = zip(*word_freq)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(counts), y=list(words), palette='viridis')
    plt.title('Top 20 Kata Dominan pada Deskripsi Sepatu')
    plt.xlabel('Frekuensi')
    plt.ylabel('Kata')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'top_words.png'))
    plt.close()

    # 2. Analisis Citra (Sederhana) - Ukuran Gambar
    image_sizes = []
    valid_images = []

    for idx, row in df.iterrows():
        img_path = row['local_image_path']
        try:
            with Image.open(img_path) as img:
                image_sizes.append(img.size) # (width, height)
                valid_images.append(row)
        except Exception as e:
            print(f"Error reading {img_path}: {e}")

    # Histogram Width x Height
    widths = [s[0] for s in image_sizes]
    heights = [s[1] for s in image_sizes]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(widths, bins=20, ax=axes[0], color='salmon')
    axes[0].set_title('Distribusi Lebar Gambar')
    axes[0].set_xlabel('Width (pixels)')

    sns.histplot(heights, bins=20, ax=axes[1], color='lightgreen')
    axes[1].set_title('Distribusi Tinggi Gambar')
    axes[1].set_xlabel('Height (pixels)')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'image_sizes.png'))
    plt.close()

    # 3. Analisis Hubungan Teks-Citra (Plot 10 contoh)
    valid_df = pd.DataFrame(valid_images)
    sample_df = valid_df.sample(10, random_state=42).reset_index(drop=True)

    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    for i, ax in enumerate(axes.flatten()):
        row = sample_df.iloc[i]
        img_path = row['local_image_path']
        text = row['text']

        # Truncate text for title
        short_text = text[:40] + "..." if len(text) > 40 else text

        try:
            img = Image.open(img_path)
            ax.imshow(img)
            ax.set_title(short_text, fontsize=10, wrap=True)
            ax.axis('off')
        except:
            ax.set_title("Image Error")
            ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'text_image_samples.png'))
    plt.close()

    # Simpan sampel text vs image mismatch / match analysis ke file teks
    with open(os.path.join(results_dir, 'eda_insights.txt'), 'w', encoding='utf-8') as f:
        f.write("=== Insight EDA Dataset ABO (Kategori: SHOES) ===\n")
        f.write(f"Total Data: {len(df)}\n")
        f.write(f"Rata-rata panjang teks deskripsi: {df['text_length'].mean():.2f} kata\n")
        f.write("Top 5 kata dominan: " + ", ".join([w[0] for w in word_freq[:5]]) + "\n")

        # Beberapa analisis observasional
        f.write("\nInsight Tambahan:\n")
        f.write("1. Teks Terlalu Umum: Banyak deskripsi yang hanya mencantumkan brand atau nama tipe secara general tanpa mendeskripsikan ciri visual sepatu (misal: warna, bentuk).\n")
        f.write("2. Banyak Mismatch: Teks memiliki istilah kompleks ('breathable', 'lightweight') yang tidak selalu bisa ditangkap secara visual oleh citra produk yang beresolusi kecil.\n")
        f.write("3. Variasi Citra: Beberapa gambar memiliki background putih (katalog murni) sementara beberapa lainnya memperlihatkan produk dari sudut (angle) yang tidak biasa.\n")

    print("EDA completed. Outputs saved to 'results/' folder.")

if __name__ == "__main__":
    main()