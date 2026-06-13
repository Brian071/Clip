import os
import pandas as pd
import gzip
import json
import urllib.request
import time
from tqdm import tqdm

def download_file(url, filepath):
    if not os.path.exists(filepath):
        print(f"Downloading {url} to {filepath}...")
        try:
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False
    return True

def main():
    data_dir = 'data'
    images_dir = 'images'
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    images_metadata_url = "https://amazon-berkeley-objects.s3.amazonaws.com/images/metadata/images.csv.gz"
    images_csv_path = os.path.join(data_dir, "images.csv.gz")

    download_file(images_metadata_url, images_csv_path)

    print("Reading images metadata...")
    try:
        images_df = pd.read_csv(images_csv_path)
        print(f"Loaded {len(images_df)} image records.")
    except Exception as e:
        print(f"Error reading images.csv.gz: {e}")
        return

    listings_tar_url = "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-listings.tar"
    listings_tar_path = os.path.join(data_dir, "abo-listings.tar")

    if not os.path.exists(listings_tar_path):
        print(f"Downloading {listings_tar_url} to {listings_tar_path}...")
        urllib.request.urlretrieve(listings_tar_url, listings_tar_path)

    print("Extracting listings...")
    os.system(f"tar -xf {listings_tar_path} -C {data_dir}")

    listings_dir = os.path.join(data_dir, "listings", "metadata")
    all_items = []

    print("Parsing listings json.gz files to find SHOES...")
    files = [f for f in os.listdir(listings_dir) if f.endswith('.json.gz')]
    shoes_data = []

    for f in files:
        filepath = os.path.join(listings_dir, f)
        with gzip.open(filepath, 'rt', encoding='utf-8') as f_in:
            for line in f_in:
                item = json.loads(line.strip())
                item_id = item.get('item_id', '')

                node_list = item.get('node', [])
                product_type = ""
                if item.get('product_type'):
                    if isinstance(item['product_type'], list):
                        product_type = item['product_type'][0].get('value', '').upper()

                if 'SHOES' in product_type:
                    title = ""
                    if item.get('item_name'):
                        title = item['item_name'][0].get('value', '')

                    if not title:
                        continue

                    main_image_id = item.get('main_image_id', '')
                    if not main_image_id:
                        continue

                    shoes_data.append({
                        'id': item_id,
                        'text': title,
                        'category': 'SHOES',
                        'image_id': main_image_id
                    })

                    if len(shoes_data) >= 800:
                        break
        if len(shoes_data) >= 800:
            break

    print(f"Found {len(shoes_data)} SHOES items.")
    shoes_df = pd.DataFrame(shoes_data)
    images_df = images_df[['image_id', 'path']]
    merged_df = pd.merge(shoes_df, images_df, on='image_id', how='inner')
    merged_df = merged_df.head(760)
    print(f"Final dataset size: {len(merged_df)}")

    print("Downloading 760 images...")
    base_image_url = "https://amazon-berkeley-objects.s3.amazonaws.com/images/small/"
    downloaded_paths = []

    for idx, row in tqdm(merged_df.iterrows(), total=len(merged_df)):
        img_path = row['path']
        img_filename = img_path.split('/')[-1]
        local_img_path = os.path.join(images_dir, img_filename)
        full_img_url = base_image_url + img_path

        try:
            if not os.path.exists(local_img_path):
                urllib.request.urlretrieve(full_img_url, local_img_path)
            downloaded_paths.append(local_img_path)
        except Exception as e:
            print(f"Failed to download {full_img_url}")
            downloaded_paths.append(None)

    merged_df['local_image_path'] = downloaded_paths
    merged_df = merged_df.dropna(subset=['local_image_path'])

    print(f"Successfully downloaded {len(merged_df)} images.")
    clean_csv_path = os.path.join(data_dir, "shoes_dataset.csv")
    merged_df.to_csv(clean_csv_path, index=False)
    print(f"Dataset saved to {clean_csv_path}")

if __name__ == "__main__":
    main()
