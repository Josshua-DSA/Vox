# Indonesian Hate Speech & Toxicity Analyzer
### Kelompok 4 — Workshop Proyek Sistem Cerdas 2026
> **Metode:** Convolutional Neural Network (CNN) for Text Classification  
> **Dataset:** IndoToxic2024 / IndoDiscourse  
> **Dosen Pengampu:** Dr. Selvia Ferdiana Kusuma, M.Kom  

---

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk mendeteksi ujaran kebencian (*hate speech*) dan teks toksik berbahasa Indonesia pada media sosial menggunakan pendekatan **Convolutional Neural Network (CNN) for Text** berbasis arsitektur multi-kernel Yoon Kim (2014). Sistem dirancang secara modular, berorientasi objek (OOP), reprodusibel, dan dilengkapi dengan modul *explainability* (feature saliency) serta antarmuka visual berbasis Streamlit.

### Fitur Utama
1. **End-to-End NLP Pipeline**: Preprocessing teks (regex cleaning, tokenisasi, sequence padding) terstandarisasi.
2. **Multi-Kernel Conv1D Architecture**: Ekstraksi representasi n-gram lokal paralel (kernel sizes: 3, 4, 5) dengan GlobalMaxPooling.
3. **Imbalance Mitigation**: Penanganan ketidakseimbangan kelas menggunakan *Class Weighting*, *Focal Loss*, dan *Oversampling*.
4. **Comprehensive Evaluation**: Pengukuran performa menyeluruh (Macro-F1, Precision, Recall, Confusion Matrix) dan Error Analysis mendalam (False Positive & False Negative).
5. **Model Explainability**: Visualisasi atribusi kata (*word saliency / integrated gradients proxy*) untuk transparansi prediksi.
6. **Interactive Prototype**: Web UI interaktif berbasis Streamlit.

---

## 📁 Struktur Direktori

```text
.
├── main.py                        # Master CLI launcher (Pipeline Trainer & Evaluator)
├── requirements.txt               # Daftar dependensi Python
├── README.md                      # Dokumentasi teknis proyek
│
├── data/
│   ├── raw/                       # Dataset mentah (indotoxic2024 CSV & JSONL)
│   ├── processed/                 # Dataset hasil cleaning
│   └── splits/                    # train.csv, val.csv, test.csv (Stratified 70/15/15)
│
├── src/
│   ├── preprocessing/             # TextCleaner, TextTokenizer, SequencePadder, DataSplitter
│   ├── models/                    # BaseModel (ABC), CNNTextClassifier, EmbeddingLoader
│   ├── training/                  # ModelTrainer, ImbalanceHandler
│   ├── evaluation/                # MetricCalculator, ConfusionMatrixPlotter, ErrorAnalyzer
│   ├── explainability/            # SaliencyMapper (Token attribution)
│   └── utils/                     # Config (Hyperparams), Logger, Seed (SEED=42)
│
├── app/                           # Prototype Web Streamlit
│   ├── streamlit_app.py           # Entry point aplikasi
│   └── components/                # Modular UI components (Input, Prediction, Explanation)
│
├── notebooks/                     # Jupyter Notebooks untuk riset & eksperimen terisolasi
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_baseline_tfidf.ipynb
│   ├── 04_cnn_baseline.ipynb
│   ├── 05_cnn_imbalance_exp.ipynb
│   ├── 06_cnn_tuning_ablation.ipynb
│   └── 07_error_analysis.ipynb
│
├── outputs/                       # Artefak hasil eksekusi (Models, Tokenizer, Metrics, Plots)
├── tests/                         # Unit tests untuk validasi modul backend
└── research/                      # Katalog literatur & paper acuan (research/PAPERS.md)
```

---

## 🚀 Panduan Instalasi & Penggunaan

### 1. Setup Virtual Environment
```bash
# Buat virtual environment
python3 -m venv .venv

# Aktifkan virtual environment
# Linux / macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Instal dependensi
pip install -r requirements.txt
```

### 2. Menjalankan Pipeline via CLI
Eksekusi pipeline lengkap atau tahapan tertentu menggunakan `main.py`:
```bash
# Menjalankan seluruh pipeline (preprocessing -> build model -> eval)
python3 main.py --stage all

# Menjalankan tahapan tertentu
python3 main.py --stage preprocess
python3 main.py --stage train
python3 main.py --stage eval
```

### 3. Menjalankan Prototype Streamlit UI
```bash
streamlit run app/streamlit_app.py
```

### 4. Menjalankan Unit Tests
```bash
python3 -m unittest discover tests
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
