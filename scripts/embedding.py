import os
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from PIL import Image
from tqdm import tqdm
import pickle

def main():
    data_path = 'data/shoes_dataset.csv'
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)

    if not os.path.exists(data_path):
        print("Dataset not found. Run preprocess.py first.")
        return

    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records for embedding generation.")

    # Inisialisasi model CLIP
    print("Loading CLIP model (clip-ViT-B-32)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer('clip-ViT-B-32').to(device)

    # 1. Ekstrak Image Embeddings
    print("Extracting Image Embeddings...")
    image_embeddings = []
    valid_indices = []

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        img_path = row['local_image_path']
        try:
            with Image.open(img_path) as img:
                # Convert to RGB just in case
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                emb = model.encode(img, convert_to_tensor=True, show_progress_bar=False)
                image_embeddings.append(emb.cpu())
                valid_indices.append(idx)
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")

    # Filter df untuk yang berhasil
    df_valid = df.loc[valid_indices].reset_index(drop=True)

    # Stack image embeddings menjadi tensor matrix
    if len(image_embeddings) > 0:
        image_embeddings_tensor = torch.stack(image_embeddings)
    else:
        print("No valid images processed.")
        return

    # 2. Ekstrak Text Embeddings (sebagai tambahan informasi)
    print("Extracting Text Embeddings...")
    text_embeddings = model.encode(df_valid['text'].tolist(), convert_to_tensor=True, show_progress_bar=True)
    text_embeddings_tensor = text_embeddings.cpu()

    # Simpan hasil embedding dan dataset yang valid
    df_valid.to_csv(os.path.join(results_dir, 'shoes_dataset_valid.csv'), index=False)

    with open(os.path.join(results_dir, 'image_embeddings.pkl'), 'wb') as f:
        pickle.dump(image_embeddings_tensor, f)

    with open(os.path.join(results_dir, 'text_embeddings.pkl'), 'wb') as f:
        pickle.dump(text_embeddings_tensor, f)

    print("Embeddings saved to 'results/' folder.")

if __name__ == "__main__":
    main()
