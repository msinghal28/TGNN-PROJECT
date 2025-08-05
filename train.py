import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import re

# --- Load and merge using wallet_id match ---
def load_and_merge_data(data_dir):
    tx_path = os.path.join(data_dir, 'training_data.csv')
    label_path = os.path.join(data_dir, 'fraud_labels.csv')

    df_tx = pd.read_csv(tx_path)
    df_labels = pd.read_csv(label_path)

    df_tx.columns = [c.strip().lower() for c in df_tx.columns]
    df_labels.columns = [c.strip().lower() for c in df_labels.columns]

    # Ensure wallet_id column exists in labels
    if 'wallet_id' not in df_labels.columns or 'src_wallet' not in df_tx.columns:
        print("Error: Required columns ('wallet_id' in labels or 'src_wallet' in tx) not found.")
        return pd.DataFrame()

    # Merge on src_wallet == wallet_id
    df = pd.merge(df_tx, df_labels, how='inner', left_on='src_wallet', right_on='wallet_id')
    df.drop(columns=['wallet_id'], inplace=True)

    if 'is_fraud' in df.columns:
        df.rename(columns={'is_fraud': 'is_phishing'}, inplace=True)

    df = df.dropna(subset=['is_phishing'])
    df['is_phishing'] = df['is_phishing'].astype(int)
    return df

# --- Feature Engineering ---
def feature_engineering(df):
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['time_gap'] = pd.to_numeric(df['time_gap'], errors='coerce')
    df['tx_count'] = pd.to_numeric(df['tx_count'], errors='coerce')

    df['src_wallet_length'] = df['src_wallet'].apply(lambda x: len(str(x)))
    df['dst_wallet_length'] = df['dst_wallet'].apply(lambda x: len(str(x)))
    df['has_0x_src'] = df['src_wallet'].apply(lambda x: 1 if str(x).startswith('0x') else 0)
    df['has_0x_dst'] = df['dst_wallet'].apply(lambda x: 1 if str(x).startswith('0x') else 0)

    def entropy(s):
        s = str(s)
        p = [s.count(c) / len(s) for c in set(s) if len(s) > 0]
        return -sum([x * np.log2(x) for x in p if x > 0]) if p else 0

    df['src_entropy'] = df['src_wallet'].apply(entropy)
    df['dst_entropy'] = df['dst_wallet'].apply(entropy)

    # Drop rows with any NaNs in features
    df = df.dropna(subset=['amount', 'time_gap', 'tx_count', 'src_entropy', 'dst_entropy'])

    features = ['amount', 'time_gap', 'tx_count', 'src_wallet_length', 'dst_wallet_length',
                'has_0x_src', 'has_0x_dst', 'src_entropy', 'dst_entropy']
    X = df[features]
    y = df['is_phishing']
    return X, y

# --- Train & Evaluate ---
def train_phishing_model(data_dir):
    df = load_and_merge_data(data_dir)
    if df.empty:
        print("Error loading and merging data. Aborting training.")
        return

    X, y = feature_engineering(df)
    print(f"\n✅ Training on {len(X)} samples ({y.sum()} phishing, {len(y)-y.sum()} legit)")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\n✅ Model Results:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# --- Main ---
if __name__ == "__main__":
    train_phishing_model("blockchain_data")
