import os
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
import pickle
import matplotlib.pyplot as plt
from PIL import Image

def perform_search(query, model, image_embeddings_tensor, df, top_k=5):
    # Encode query
    query_embedding = model.encode(query, convert_to_tensor=True).cpu()

    # Calculate cosine similarity
    cos_scores = util.cos_sim(query_embedding, image_embeddings_tensor)[0]

    # Sort scores and get top_k
    top_results = torch.topk(cos_scores, k=top_k)

    results = []
    for score, idx in zip(top_results[0], top_results[1]):
        results.append({
            'score': score.item(),
            'id': df.iloc[idx.item()]['id'],
            'text': df.iloc[idx.item()]['text'],
            'local_image_path': df.iloc[idx.item()]['local_image_path']
        })
    return results

def plot_results(query, results, filename):
    fig, axes = plt.subplots(1, len(results), figsize=(15, 4))
    fig.suptitle(f'Query: "{query}"', fontsize=16)

    for i, res in enumerate(results):
        ax = axes[i]
        try:
            img = Image.open(res['local_image_path'])
            ax.imshow(img)
            # Shorten text
            short_text = res['text'][:30] + "..." if len(res['text']) > 30 else res['text']
            ax.set_title(f"Score: {res['score']:.2f}\n{short_text}", fontsize=9, wrap=True)
            ax.axis('off')
        except:
            ax.set_title("Image Error")
            ax.axis('off')

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    results_dir = 'results'
    dataset_path = os.path.join(results_dir, 'shoes_dataset_valid.csv')
    emb_path = os.path.join(results_dir, 'image_embeddings.pkl')

    if not os.path.exists(dataset_path) or not os.path.exists(emb_path):
        print("Embeddings or valid dataset not found. Run embedding.py first.")
        return

    df = pd.read_csv(dataset_path)

    with open(emb_path, 'rb') as f:
        image_embeddings_tensor = pickle.load(f)

    print("Loading CLIP model (clip-ViT-B-32)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer('clip-ViT-B-32').to(device)

    # Uji Coba: 2 Kasus Berhasil, 2 Kasus Gagal/Ambigu
    test_queries = {
        'success_1': "formal black leather shoes",
        'success_2': "red running sneakers",
        'failure_1': "black shoes", # Terlalu umum (Ambiguity)
        'failure_2': "comfortable lightweight walking" # Semantic gap, no explicit visual feature
    }

    analysis_results = []

    print("Performing Retrieval Tests...")
    for key, query in test_queries.items():
        print(f"Testing Query: {query}")
        res = perform_search(query, model, image_embeddings_tensor, df, top_k=5)

        plot_filename = os.path.join(results_dir, f'retrieval_{key}.png')
        plot_results(query, res, plot_filename)

        # Save info for report
        analysis_results.append(f"Query ({key}): {query}")
        for i, r in enumerate(res):
            analysis_results.append(f"  Rank {i+1} [Score: {r['score']:.4f}] - {r['text']}")
        analysis_results.append("")

    with open(os.path.join(results_dir, 'retrieval_analysis.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(analysis_results))

    print("Retrieval analysis completed. Plots and text saved to 'results/' folder.")

if __name__ == "__main__":
    main()
