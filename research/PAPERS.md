# Research Papers Catalog — Kel4 Indonesian Hate Speech (CNN)

Katalog jurnal dan paper referensi untuk proyek deteksi hate speech Bahasa Indonesia menggunakan CNN for Text Classification (Dataset: IndoToxic2024).

---

## 1. Dataset & Karakteristik Bahasa Indonesia
1. **IndoToxic2024: A Demographically-Enriched Dataset of Hate Speech and Toxicity Types for Indonesian Language (2024)**  
   *Susanto et al.* | [arXiv:2406.19349](https://arxiv.org/abs/2406.19349)  
   *Peran:* Paper acuan primer dataset `data/raw/`, skema anotasi biner & multi-label, dan baseline evaluasi.
2. **A Multi-Labeled Dataset for Indonesian Discourse: Examining Toxicity, Polarization, and Demographics Information (2025)**  
   *Susanto et al.* | [arXiv:2503.00417](https://arxiv.org/abs/2503.00417)  
   *Peran:* Ekstensi dataset IndoToxic2024 / IndoDiscourse.
3. **Indonesian NLP Benchmarks & IndoBERTweet (2024)**  
   *arXiv:2403.01817* | [arXiv:2403.01817](https://arxiv.org/abs/2403.01817)  
   *Peran:* Analisis kata slang, normalisasi teks media sosial, dan representasi leksikal Bahasa Indonesia.

---

## 2. Arsitektur CNN for Text & Hate Speech
4. **Convolutional Neural Networks for Sentence Classification (2014)**  
   *Yoon Kim (EMNLP 2014)* | [arXiv:1408.5882](https://arxiv.org/abs/1408.5882)  
   *Peran:* Paper fondasi multi-kernel Conv1D (filter sizes 3, 4, 5) dan max-over-time pooling.
5. **A Comparative Study of PyCaret AutoML and CNN-BiLSTM for Binary Hate Speech Detection in Indonesian Twitter (2026)**  
   *arXiv:2605.04885* | [arXiv:2605.04885](https://arxiv.org/abs/2605.04885)  
   *Peran:* Benchmark komparasi baseline TF-IDF vs Convolutional neural network pada hate speech Indonesia.
6. **Enhancing Hate Speech Detection on Social Media: A Comparative Analysis of Machine Learning Models and Text Transformation Approaches (2026)**  
   *arXiv:2602.20634* | [arXiv:2602.20634](https://arxiv.org/abs/2602.20634)  
   *Peran:* Analisis representasi n-gram teks untuk layer konvolusi.
7. **dictNN: A Dictionary-Enhanced CNN Approach for Classifying Hate Speech on Twitter (2021)**  
   *Kupi et al.* | [arXiv:2103.08780](https://arxiv.org/abs/2103.08780)  
   *Peran:* Penggabungan embedding kata dan kamus hate speech ke arsitektur CNN.
8. **A Survey of Toxic Comment Classification Methods (2021)**  
   *Wang et al.* | [arXiv:2112.06412](https://arxiv.org/abs/2112.06412)  
   *Peran:* Evaluasi empiris CNN Conv1D pada deteksi komentar toksik.
9. **Highly Generalizable Models for Multilingual Hate Speech Detection (2022)**  
   *Deshpande et al.* | [arXiv:2201.11294](https://arxiv.org/abs/2201.11294)  
   *Peran:* Evaluasi model neural berbasis CNN pada dataset lintas bahasa (termasuk Indonesia).
10. **Explainable Deep Learning Models for Patent / Text Classification with FastText (2023)**  
    *arXiv:2310.20478* | [arXiv:2310.20478](https://arxiv.org/abs/2310.20478)  
    *Peran:* Penggunaan representasi embedding FastText pada model CNN.
11. **Towards Intelligent Legal Document Analysis: CNN-Driven Classification of Texts (2026)**  
    *arXiv:2604.17674* | [arXiv:2604.17674](https://arxiv.org/abs/2604.17674)  
    *Peran:* Implementasi multi-kernel CNN dan subword embedding.
12. **Explicit Grammar Semantic Feature Fusion for Robust Text Classification (2026)**  
    *Sultana & Ahmed* | [arXiv:2602.20749](https://arxiv.org/abs/2602.20749)  
    *Peran:* Feature fusion pada model sekuensial deep learning.

---

## 3. Penanganan Class Imbalance & Loss Function (`ImbalanceHandler`)
13. **Improving Model Performance through Imbalance Handling and Focal Loss (2025)**  
    *arXiv:2505.00021* | [arXiv:2505.00021](https://arxiv.org/abs/2505.00021)  
    *Peran:* Formulasi Focal Loss dan teknik oversampling pada klasifikasi teks.
14. **Overlapping word removal is all you need: revisiting data imbalance in hope/hate speech detection (2022)**  
    *arXiv:2204.05488* | [arXiv:2204.05488](https://arxiv.org/abs/2204.05488)  
    *Peran:* Mitigasi imbalance dan noise leksikal pada klasifikasi hate speech.
15. **Multimodal Metadata Assignment: ResNet CNN and Multitask Focal Loss for Imbalance (2024)**  
    *arXiv:2406.00423* | [arXiv:2406.00423](https://arxiv.org/abs/2406.00423)  
    *Peran:* Strategi penanganan class imbalance menggunakan loss adaptif.
16. **RAKSHAK: Multi-Task Architecture with Focal Loss for Toxic Intent Classification (2026)**  
    *arXiv:2607.20450* | [arXiv:2607.20450](https://arxiv.org/abs/2607.20450)  
    *Peran:* Penanganan kategori toksik langka (extreme class imbalance).
17. **A Survey of Machine Learning Models and Datasets for Multi-label Classification of Textual Hate Speech (2025)**  
    *arXiv:2504.08609* | [arXiv:2504.08609](https://arxiv.org/abs/2504.08609)  
    *Peran:* Evaluasi loss function pada multi-label hate speech.

---

## 4. Data Augmentation untuk Hate Speech
18. **A Comprehensive Study on NLP Data Augmentation in Hate Speech Detection (2024)**  
    *Jahan et al.* | [arXiv:2404.00303](https://arxiv.org/abs/2404.00303)  
    *Peran:* Evaluasi back-translation, synonym replacement, dan contextual augmentation.
19. **A Target-Aware Analysis of Data Augmentation for Hate Speech Detection (2024)**  
    *arXiv:2410.08053* | [arXiv:2410.08053](https://arxiv.org/abs/2410.08053)  
    *Peran:* Augmentasi data seimbang berbasis target hate speech.
20. **Data Augmentation and Feature Enhancement Techniques for Hate Speech Detection (2026)**  
    *arXiv:2603.04698* | [arXiv:2603.04698](https://arxiv.org/abs/2603.04698)  
    *Peran:* Evaluasi SMOTE vs data augmentation pada model deep learning & baseline.
21. **Data Expansion using Back Translation and Paraphrasing for Hate Speech Detection (2021)**  
    *arXiv:2106.04681* | [arXiv:2106.04681](https://arxiv.org/abs/2106.04681)  
    *Peran:* Pipeline augmentasi back-translation yang dievaluasi langsung pada arsitektur CNN teks.
22. **Indonesian Gender-Based Hate Speech Detection with Data Augmentation (2025)**  
    *Ibrahim et al.* | [arXiv:2503.04279](https://arxiv.org/abs/2503.04279)  
    *Peran:* Strategi augmentasi teks media sosial berbahasa Indonesia.

---

## 5. Explainability & Saliency Attribution (`SaliencyMapper`)
23. **Axiomatic Attribution for Deep Networks (Integrated Gradients) (2017)**  
    *Sundararajan et al.* | [arXiv:1703.01365](https://arxiv.org/abs/1703.01365)  
    *Peran:* Fondasi matematis kalkulasi feature attribution pada representasi embedding teks.
24. **Application of Integrated Gradients Explainability to Semantic Markers (2025)**  
    *Cervone et al.* | [arXiv:2503.04989](https://arxiv.org/abs/2503.04989)  
    *Peran:* Penerapan word-level Integrated Gradients untuk visualisasi highlight kata toksik.
25. **Sequential Integrated Gradients: A Simple Method for Explaining Language Models (2023)**  
    *Enguehard* | [arXiv:2305.15853](https://arxiv.org/abs/2305.15853)  
    *Peran:* Saliency map efisien untuk visualisasi filter token pada prototype Streamlit.
