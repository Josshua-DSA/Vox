# Indonesian Hate Speech & Toxicity Analyzer
### Kelompok 4 — Workshop Proyek Sistem Cerdas 2026
> **Metode:** Convolutional Neural Network (CNN) for Text Classification  
> **Dataset:** IndoToxic2024 / IndoDiscourse  
> **Dosen Pengampu:** Dr. Selvia Ferdiana Kusuma, M.Kom  

---

Group Contribution:
1. Joshua Remedial Syeba           : Infrastruktur, Database & Arsitektur CNN
2. Siti Cholilah                   : CI/CD
3. Much. Hafidz Indrajid           : Frontend and API Integration
4. Muhammad Zidan Akmal Nurrochman : Backend and API build up

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk mendeteksi ujaran kebencian (*hate speech*) dan teks toksik berbahasa Indonesia pada media sosial menggunakan pendekatan **Convolutional Neural Network (CNN) for Text** berbasis arsitektur multi-kernel Yoon Kim (2014). Sistem dirancang secara modular, berorientasi objek (OOP), reprodusibel, terintegrasi dengan database PostgreSQL untuk data pipeline & auto-scraping, serta dilengkapi dengan modul *explainability* (feature saliency) dan antarmuka visual berbasis Streamlit.

### Fitur Utama
1. **End-to-End NLP Pipeline**: Preprocessing teks (regex cleaning, tokenisasi, sequence padding) terstandarisasi.
2. **Hybrid Database Layer (PostgreSQL)**: Penyimpanan dataset terstruktur (28.445 baris) + tabel raw dump JSONB fleksibel untuk kebutuhan auto-scraping multi-platform.
3. **Multi-Kernel Conv1D Architecture**: Ekstraksi representasi n-gram lokal paralel (kernel sizes: 3, 4, 5) dengan GlobalMaxPooling.
4. **Imbalance Mitigation**: Penanganan ketidakseimbangan kelas menggunakan *Class Weighting*, *Focal Loss*, dan *Oversampling*.
5. **Comprehensive Evaluation**: Pengukuran performa menyeluruh (Macro-F1, Precision, Recall, Confusion Matrix) dan Error Analysis mendalam (False Positive & False Negative).
6. **Model Explainability**: Visualisasi atribusi kata (*word saliency / integrated gradients proxy*) untuk transparansi prediksi.
7. **Interactive Prototype**: Web UI interaktif berbasis Streamlit.

---

## 📁 Struktur Direktori

```text
.
├── main.py                        # Master CLI launcher (Pipeline Trainer & Evaluator)
├── pyproject.toml                 # Project metadata, pytest & ruff config
├── Makefile                       # One-command dev workflow (make test, make lint, dll)
├── docker-compose.yml             # Service container PostgreSQL
├── .env.example                   # Template konfigurasi environment & database URL
├── .gitattributes                 # Git LFS tracking rules untuk data/raw/
├── requirements.txt               # Daftar dependensi Python (legacy, lihat pyproject.toml)
├── CONTRIBUTING.md                # Panduan kontribusi, setup, branch & PR workflow
├── README.md                      # Dokumentasi teknis proyek
│
├── .github/workflows/
│   └── ci.yml                     # GitHub Actions: Ruff lint + pytest on PR
│
├── data/
│   ├── raw/                       # Dataset mentah — Git LFS tracked (CSV & JSONL)
│   ├── processed/                 # Dataset hasil cleaning
│   └── splits/                    # train.csv, val.csv, test.csv (Stratified 70/15/15)
│
├── src/
│   ├── database/                  # Modul PostgreSQL (models, connection, repository)
│   ├── preprocessing/             # TextCleaner, TextTokenizer, SequencePadder, DataSplitter
│   ├── models/                    # BaseModel (ABC), CNNTextClassifier, EmbeddingLoader
│   ├── training/                  # ModelTrainer, ImbalanceHandler
│   ├── evaluation/                # MetricCalculator, ConfusionMatrixPlotter, ErrorAnalyzer
│   ├── explainability/            # SaliencyMapper (Token attribution)
│   └── utils/                     # Config (Hyperparams & DB URL), Logger, Seed (SEED=42)
│
├── scripts/                       # Skrip otomatisasi (migrasi CSV ke PostgreSQL)
│   └── migrate_csv_to_postgres.py
│
├── app/                           # Prototype Web Streamlit
│   ├── streamlit_app.py           # Entry point aplikasi
│   └── components/                # Modular UI components (Input, Prediction, Explanation)
│
├── notebooks/                     # Jupyter Notebooks untuk riset & eksperimen terisolasi
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_baseline.ipynb
│   └── 04_cnn_experiment.ipynb
│
├── outputs/                       # Artefak hasil eksekusi (Models, Tokenizer, Metrics, Plots)
├── tests/                         # Unit tests + conftest.py (shared fixtures)
└── research/                      # Katalog literatur & paper acuan (research/PAPERS.md)
```

---

## 🚀 Panduan Instalasi & Penggunaan

### 1. Setup Virtual Environment
```bash
# Quick setup (recommended)
make setup

# Atau manual:
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
pip install -e ".[dev]"
```

### 2. Setup Database PostgreSQL
Pastikan Docker dan docker-compose terpasang, lalu jalankan container database:
```bash
cp .env.example .env
make db-up                      # atau: docker-compose up -d
make migrate                    # atau: python scripts/migrate_csv_to_postgres.py
```

### 3. Menjalankan Pipeline via CLI
```bash
make run                        # atau: python main.py --stage all

# Tahapan tertentu:
python main.py --stage preprocess
python main.py --stage train
python main.py --stage eval
```

### 4. Menjalankan Prototype Streamlit UI
```bash
make run-app                    # atau: streamlit run app/streamlit_app.py
```

### 5. Linting & Testing
```bash
make lint                       # Ruff lint check
make format                     # Ruff auto-format
make test                       # Pytest (9 tests)
```

---

## 📚 Dataset & Sitasi Kredit

Dataset yang digunakan dalam proyek ini adalah **IndoToxic2024 / IndoDiscourse**, korpus ujaran kebencian dan teks terpolarisasi berbahasa Indonesia yang diperkaya dengan anotasi demografi multi-label.

Kami memberikan kredit dan apresiasi penuh kepada para peneliti penyedia dataset:
- **Repository HuggingFace:** [Exqrch/IndoDiscourse](https://huggingface.co/datasets/Exqrch/IndoDiscourse?library=datasets)
- **Repository GitHub:** [izzako/IndoToxic2024](https://github.com/izzako/IndoToxic2024)
- **Paper Referensi Dataset:** [arXiv:2503.00417](https://arxiv.org/abs/2503.00417) & [arXiv:2406.19349](https://arxiv.org/abs/2406.19349)

### BibTeX Citation:
```bibtex
@misc{susanto2025multilabeleddatasetindonesiandiscourse,
      title={A Multi-Labeled Dataset for Indonesian Discourse: Examining Toxicity, Polarization, and Demographics Information}, 
      author={Lucky Susanto and Musa Wijanarko and Prasetia Pratama and Zilu Tang and Fariz Akyas and Traci Hong and Ika Idris and Alham Aji and Derry Wijaya},
      year={2025},
      eprint={2503.00417},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2503.00417}, 
}

@article{susanto2024indotoxic2024,
      title={IndoToxic2024: A Demographically-Enriched Dataset of Hate Speech and Toxicity Types for Indonesian Language},
      author={Lucky Susanto and Musa Izzanardi Wijanarko and Prasetia Anugrah Pratama and Traci Hong and Ika Idris and Alham Fikri Aji and Derry Wijaya},
      year={2024},
      eprint={2406.19349},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2406.19349},
}
```

---

## 🔬 Literatur & Referensi Tambahan

Daftar 25 paper referensi terkait CNN text classification, penanganan imbalance (focal loss), explainability (integrated gradients), dan karakteristik teks bahasa Indonesia tercatat di [`research/PAPERS.md`](research/PAPERS.md).
