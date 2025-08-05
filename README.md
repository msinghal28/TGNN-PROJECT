# 🛡️ TGNN-Based Multi-Chain Blockchain Fraud Detection

A real-time, graph-based fraud detection system using **Temporal Graph Neural Networks (TGNN)** to detect phishing, scams, rug pulls, and suspicious smart contracts in **Ethereum** and **BNB Chain** networks.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Results](#results)
- [Future Work](#future-work)
- [References](#references)

---

## 📖 Overview

This project implements a **multi-chain fraud detection framework** using **Temporal Graph Neural Networks (TGNNs)** to monitor and classify blockchain activities in real-time. The system builds temporal graphs from live transaction data, models wallet and contract behavior over time, and predicts fraud risk dynamically.

Fraud types handled:
- Phishing scams
- Rug pulls
- Address rotation
- Malicious smart contracts
- Cross-chain laundering

---

## 🚀 Key Features

✅ **Multi-chain support** – Works with Ethereum and BNB Chain.

✅ **Real-time detection** – Fraud predictions via REST API using FastAPI.

✅ **Temporal Graph Modeling** – Captures evolving fraud patterns using TGNN.

✅ **Smart Contract Behavior Analysis** – Flags contracts with malicious intent based on transaction behavior.

✅ **Wallet Clustering** – Detects coordinated fraud rings with similar behaviors.

✅ **Frontend** – Intuitive React.js dashboard for querying wallet risk scores.

---

## 🧠 Architecture

```plaintext
               ┌────────────────────┐
               │ Blockchain Nodes   │
               │ (Ethereum, BNB)    │
               └────────┬───────────┘
                        ↓
        ┌────────────────────────────────────┐
        │ Real-time Transaction Collector    │
        │ (WebSocket/API based)              │
        └────────┬───────────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ Temporal Graph Generator     │
        └────────┬─────────────────────┘
                 ↓
        ┌──────────────────────────────┐
        │ TGNN Model (GConv-GRU Net)  │
        └────────┬─────────────────────┘
                 ↓
       ┌────────────────────────────────┐
       │ Fraud Score + Safer Suggestion │
       └────────────────────────────────┘
                 ↓
       ┌────────────┬───────────────┐
       │ FastAPI    │ React.js UI   │
       └────────────┴───────────────┘
```

---

## 🔬 Methodology

### 📊 Data Preprocessing
- Transaction history is parsed into temporal graph snapshots.
- Nodes = Wallets & Contracts | Edges = Time-stamped Transactions
- Node labels (fraud/legit) are mapped from global IDs.

### 🔄 Stratified Temporal Splitting
- Ensures balanced fraud distribution across training, validation, and test splits.
- Maintains real-world time-ordering and fraud ratio.

### 🧠 Model: Improved GConv-GRU Net
- Combines Graph Convolution + GRU for temporal learning.
- Dropout, BatchNorm, and MLP classifier for fraud detection.
- Trained using weighted CrossEntropy loss with dynamic sampling.

### 🧪 Evaluation
- Threshold optimized using F1-score.
- Final metrics: Accuracy, ROC AUC, PR AUC, Fraud Precision/Recall.

---

## 📁 Project Structure

```
TGNN-PROJECT/
│
├── data/                   # Raw and processed data (CSV, JSON, Snapshots)
├── models/                 # Trained .pt model files and saved thresholds
├── tgnn_model/             # TGNN architecture (ImprovedGConvGRUNet, etc.)
├── graph_utils/            # Graph construction & clustering utils
├── inference/              # Real-time fraud scoring and FastAPI
├── frontend/               # React.js dashboard (optional)
├── train.py                # Training script
├── tgnn_predict.py         # Inference module for wallet/contract scoring
└── README.md
```

---

## 🛠️ How to Run

### 1. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🧠 Train the Model

```bash
python train.py
```

### 3. 🚀 Run Inference API

```bash
uvicorn inference.api:app --reload
```

### 4. 🧪 Query Risk Score

Send POST request to:
```
POST /predict
{
  "wallet_address": "0x123...abc",
  "chain": "ethereum"
}
```

---

## 📈 Results

| Metric                 | Score    |
|------------------------|----------|
| Fraud Recall           | 97.11%   |
| Fraud Precision        | 65.12%   |
| Fraud F1-Score         | 77.96%   |
| ROC AUC                | 0.9424   |
| PR AUC                 | 0.6832   |
| Optimal Threshold      | 0.8680   |
| Total Test Accuracy    | 91.04%   |

✅ High fraud recall ensures effective early warnings  
⚠️ Acceptable trade-off in precision for better fraud coverage

---

## 🔮 Future Work

- 🔗 Extend support for Solana, Polygon, etc.
- 🧠 Integrate Large Language Models for scam reasoning.
- 📊 Visual graph explorer with scam pattern heatmaps.
- 🛠️ Deploy full-stack version for public risk scoring portal.

---

## 📚 References

- 📄 Project Paper (PDF): `ELC_Blockhoppers.pdf`
- 🧠 Temporal Graph Networks: https://arxiv.org/abs/2006.10637
- 🧾 GitHub Repo: https://github.com/msinghal28/TGNN-PROJECT

---

## 🤝 Contributing

Pull requests and discussions are welcome! Please open an issue for major changes.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.