import argparse
import os

def download_dataset(download_dir):
    """
    Instructions to download the PlantVillage dataset.
    Because the dataset is ~2.5GB, we cannot bundle it directly.
    """
    print("PlantVillage Dataset Download Instructions")
    print("========================================")
    print("The PlantVillage dataset is too large to download automatically in this demo.")
    print("Please follow these steps to download it manually:\n")
    print("1. Go to Kaggle: https://www.kaggle.com/datasets/abdallahalbin/plantvillage-dataset")
    print("2. Download the dataset archive (.zip).")
    print(f"3. Extract the contents into the '{download_dir}' directory.")
    print("4. Ensure the structure looks like this:")
    print(f"   {download_dir}/")
    print("       color/")
    print("           Apple___Apple_scab/")
    print("           ...")
    print("       grayscale/")
    print("       segmented/\n")
    print("Once downloaded and extracted, you can run `train.py`.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download PlantVillage Dataset")
    parser.add_argument("--dir", type=str, default="../dataset", help="Directory to save the dataset")
    args = parser.parse_args()
    
    os.makedirs(args.dir, exist_ok=True)
    download_dataset(args.dir)
