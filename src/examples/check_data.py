import numpy as np
import os

data_dir = 'data' 
features_path = os.path.join(data_dir, 'features_train.npy')
labels_path = os.path.join(data_dir, 'labels_train.npy')

print("--- Running Data Integrity Check ---")
try:
    features = np.load(features_path)
    labels = np.load(labels_path)
    
    print(f"Loaded features from: {features_path}")
    print(f"Number of features: {len(features)}")
    
    print(f"Loaded labels from: {labels_path}")
    print(f"Number of labels:   {len(labels)}")

    if len(features) == len(labels):
        print("\nSUCCESS: The number of features and labels match.")
    else:
        print(f"\nERROR: Mismatch found! Features: {len(features)}, Labels: {len(labels)}")
        print("This is the source of your error. Please apply the fix in processor.py and regenerate your data.")

except FileNotFoundError as e:
    print(f"ERROR: Could not find file. Make sure data has been generated. {e}")