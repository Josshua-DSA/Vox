# Research Papers Catalog — Kel4 Indonesian Hate Speech (CNN)

Katalog jurnal dan paper referensi untuk proyek deteksi hate speech Bahasa Indonesia menggunakan CNN for Text Classification (Dataset: IndoToxic2024).

---

## 1. Dataset & Karakteristik Bahasa Indonesia (`research/01_dataset_indonesia/`)
1. **IndoToxic2024: A Demographically-Enriched Dataset of Hate Speech and Toxicity Types for Indonesian Language (2024)**  
   *Susanto et al.* | [arXiv:2406.19349](https://arxiv.org/abs/2406.19349)  
   *File:* `research/01_dataset_indonesia/2024_IndoToxic2024_Dataset_Paper.pdf`  
   *Peran:* Paper acuan primer dataset `data/raw/`, skema anotasi biner & multi-label, dan baseline evaluasi.
2. **A Multi-Labeled Dataset for Indonesian Discourse: Examining Toxicity, Polarization, and Demographics Information (2025)**  
   *Susanto et al.* | [arXiv:2503.00417](https://arxiv.org/abs/2503.00417)  
   *File:* `research/01_dataset_indonesia/2025_IndoDiscourse_IndoToxic2024_Extension.pdf`  
   *Peran:* Ekstensi dataset IndoToxic2024 / IndoDiscourse.
3. **Indonesian NLP Benchmarks & IndoBERTweet (2024)**  
   *arXiv:2403.01817* | [arXiv:2403.01817](https://arxiv.org/abs/2403.01817)  
   *File:* `research/01_dataset_indonesia/2024_Indonesian_NLP_Benchmarks_IndoNLU_IndoBERTweet.pdf`  
   *Peran:* Analisis kata slang, normalisasi teks media sosial, dan representasi leksikal Bahasa Indonesia.

---

## 2. Arsitektur CNN for Text & Hate Speech (`research/02_cnn_architecture/`)
4. **Convolutional Neural Networks for Sentence Classification (2014)**  
   *Yoon Kim (EMNLP 2014)* | [arXiv:1408.5882](https://arxiv.org/abs/1408.5882)  
   *File:* `research/02_cnn_architecture/1408.5882_CNN_Sentence_Classification_YoonKim.pdf`  
   *Peran:* Paper fondasi multi-kernel Conv1D (filter sizes 3, 4, 5) dan max-over-time pooling.
5. **A Comparative Study of PyCaret AutoML and CNN-BiLSTM for Binary Hate Speech Detection in Indonesian Twitter (2026)**  
   *arXiv:2605.04885* | [arXiv:2605.04885](https://arxiv.org/abs/2605.04885)  
   *File:* `research/02_cnn_architecture/2026_Comparative_Study_PyCaret_CNN_BiLSTM_Indonesian.pdf`  
   *Peran:* Benchmark komparasi baseline TF-IDF vs Convolutional neural network pada hate speech Indonesia.
6. **Enhancing Hate Speech Detection on Social Media: A Comparative Analysis of Machine Learning Models and Text Transformation Approaches (2026)**  
   *arXiv:2602.20634* | [arXiv:2602.20634](https://arxiv.org/abs/2602.20634)  
   *File:* `research/02_cnn_architecture/2026_Enhancing_Hate_Speech_Detection_CNN_LSTM.pdf`  
   *Peran:* Analisis representasi n-gram teks untuk layer konvolusi.
7. **dictNN: A Dictionary-Enhanced CNN Approach for Classifying Hate Speech on Twitter (2021)**  
   *Kupi et al.* | [arXiv:2103.08780](https://arxiv.org/abs/2103.08780)  
   *File:* `research/02_cnn_architecture/2021_dictNN_Dictionary_Enhanced_CNN_Hate_Speech.pdf`  
   *Peran:* Penggabungan embedding kata dan kamus hate speech ke arsitektur CNN.
8. **A Survey of Toxic Comment Classification Methods (2021)**  
   *Wang et al.* | [arXiv:2112.06412](https://arxiv.org/abs/2112.06412)  
   *File:* `research/02_cnn_architecture/2021_Survey_Toxic_Comment_Classification_CNN_LSTM.pdf`  
   *Peran:* Evaluasi empiris CNN Conv1D pada deteksi komentar toksik.
9. **Highly Generalizable Models for Multilingual Hate Speech Detection (2022)**  
   *Deshpande et al.* | [arXiv:2201.11294](https://arxiv.org/abs/2201.11294)  
   *File:* `research/02_cnn_architecture/2022_Multilingual_Hate_Speech_Detection_CNN_GRU.pdf`  
   *Peran:* Evaluasi model neural berbasis CNN pada dataset lintas bahasa (termasuk Indonesia).
10. **Explainable Deep Learning Models for Patent / Text Classification with FastText (2023)**  
    *arXiv:2310.20478* | [arXiv:2310.20478](https://arxiv.org/abs/2310.20478)  
    *File:* `research/02_cnn_architecture/2023_Explainable_CNN_FastText_Text_Classification.pdf`  
    *Peran:* Penggunaan representasi embedding FastText pada model CNN.
11. **Towards Intelligent Legal Document Analysis: CNN-Driven Classification of Texts (2026)**  
    *arXiv:2604.17674* | [arXiv:2604.17674](https://arxiv.org/abs/2604.17674)  
    *File:* `research/02_cnn_architecture/2026_CNN_FastText_Text_Classification.pdf`  
    *Peran:* Implementasi multi-kernel CNN dan subword embedding.
12. **Explicit Grammar Semantic Feature Fusion for Robust Text Classification (2026)**  
    *Sultana & Ahmed* | [arXiv:2602.20749](https://arxiv.org/abs/2602.20749)  
    *File:* `research/02_cnn_architecture/2026_Semantic_Feature_Fusion_Text_Classification.pdf`  
    *Peran:* Feature fusion pada model sekuensial deep learning.
13. **A Survey on Multimodal Aspect-Based Sentiment Analysis**  
    *File:* `research/02_cnn_architecture/A_Survey_on_Multimodal_Aspect-Based_Sentiment_Analysis.pdf`  
    *Peran:* Rujukan komparatif pemrosesan multi-modal.

---

## 3. Penanganan Class Imbalance & Loss Function (`research/03_imbalance_loss/`)
14. **Improving Model Performance through Imbalance Handling and Focal Loss (2025)**  
    *arXiv:2505.00021* | [arXiv:2505.00021](https://arxiv.org/abs/2505.00021)  
    *File:* `research/03_imbalance_loss/2025_Imbalance_Handling_and_Focal_Loss_Text_Classification.pdf`  
    *Peran:* Formulasi Focal Loss dan teknik oversampling pada klasifikasi teks.
15. **Overlapping word removal is all you need: revisiting data imbalance in hope/hate speech detection (2022)**  
    *arXiv:2204.05488* | [arXiv:2204.05488](https://arxiv.org/abs/2204.05488)  
    *File:* `research/03_imbalance_loss/2022_Focal_Loss_and_Imbalance_in_Hate_Speech.pdf`  
    *Peran:* Mitigasi imbalance dan noise leksikal pada klasifikasi hate speech.
16. **Multimodal Metadata Assignment: ResNet CNN and Multitask Focal Loss for Imbalance (2024)**  
    *arXiv:2406.00423* | [arXiv:2406.00423](https://arxiv.org/abs/2406.00423)  
    *File:* `research/03_imbalance_loss/2024_CNN_Focal_Loss_Imbalance_Multimodal.pdf`  
    *Peran:* Strategi penanganan class imbalance menggunakan loss adaptif.
17. **RAKSHAK: Multi-Task Architecture with Focal Loss for Toxic Intent Classification (2026)**  
    *arXiv:2607.20450* | [arXiv:2607.20450](https://arxiv.org/abs/2607.20450)  
    *File:* `research/03_imbalance_loss/2026_RAKSHAK_Toxic_Intent_Focal_Loss.pdf`  
    *Peran:* Penanganan kategori toksik langka (extreme class imbalance).
18. **A Survey of Machine Learning Models and Datasets for Multi-label Classification of Textual Hate Speech (2025)**  
    *arXiv:2504.08609* | [arXiv:2504.08609](https://arxiv.org/abs/2504.08609)  
    *File:* `research/03_imbalance_loss/2025_Survey_Multilabel_Textual_Hate_Speech.pdf`  
    *Peran:* Evaluasi loss function pada multi-label hate speech.

---

## 4. Data Augmentation untuk Hate Speech (`research/04_data_augmentation/`)
19. **A Comprehensive Study on NLP Data Augmentation in Hate Speech Detection (2024)**  
    *Jahan et al.* | [arXiv:2404.00303](https://arxiv.org/abs/2404.00303)  
    *File:* `research/04_data_augmentation/2024_Comprehensive_Study_NLP_Data_Augmentation.pdf`  
    *Peran:* Evaluasi back-translation, synonym replacement, dan contextual augmentation.
20. **A Target-Aware Analysis of Data Augmentation for Hate Speech Detection (2024)**  
    *arXiv:2410.08053* | [arXiv:2410.08053](https://arxiv.org/abs/2410.08053)  
    *File:* `research/04_data_augmentation/2024_Target_Aware_Data_Augmentation_Hate_Speech.pdf`  
    *Peran:* Augmentasi data seimbang berbasis target hate speech.
21. **Data Augmentation and Feature Enhancement Techniques for Hate Speech Detection (2026)**  
    *arXiv:2603.04698* | [arXiv:2603.04698](https://arxiv.org/abs/2603.04698)  
    *File:* `research/04_data_augmentation/2026_Data_Augmentation_Feature_Enhancement_Hate_Speech.pdf`  
    *Peran:* Evaluasi SMOTE vs data augmentation pada model deep learning & baseline.
22. **Data Expansion using Back Translation and Paraphrasing for Hate Speech Detection (2021)**  
    *arXiv:2106.04681* | [arXiv:2106.04681](https://arxiv.org/abs/2106.04681)  
    *File:* `research/04_data_augmentation/2021_Data_Expansion_BackTranslation_CNN.pdf`  
    *Peran:* Pipeline augmentasi back-translation yang dievaluasi langsung pada arsitektur CNN teks.
23. **Indonesian Gender-Based Hate Speech Detection with Data Augmentation (2025)**  
    *Ibrahim et al.* | [arXiv:2503.04279](https://arxiv.org/abs/2503.04279)  
    *File:* `research/04_data_augmentation/2025_Indonesian_Gender_Hate_Speech_Data_Augmentation.pdf`  
    *Peran:* Strategi augmentasi teks media sosial berbahasa Indonesia.

---

## 5. Explainability & Saliency Attribution (`research/05_explainability_xai/`)
24. **Axiomatic Attribution for Deep Networks (Integrated Gradients) (2017)**  
    *Sundararajan et al.* | [arXiv:1703.01365](https://arxiv.org/abs/1703.01365)  
    *File:* `research/05_explainability_xai/1703.01365_Axiomatic_Attribution_Integrated_Gradients.pdf`  
    *Peran:* Fondasi matematis kalkulasi feature attribution pada representasi embedding teks.
25. **Application of Integrated Gradients Explainability to Semantic Markers (2025)**  
    *Cervone et al.* | [arXiv:2503.04989](https://arxiv.org/abs/2503.04989)  
    *File:* `research/05_explainability_xai/2025_Integrated_Gradients_Word_Level_Explainability.pdf`  
    *Peran:* Penerapan word-level Integrated Gradients untuk visualisasi highlight kata toksik.
26. **Sequential Integrated Gradients: A Simple Method for Explaining Language Models (2023)**  
    *Enguehard* | [arXiv:2305.15853](https://arxiv.org/abs/2305.15853)  
    *File:* `research/05_explainability_xai/2023_Sequential_Integrated_Gradients_Explainability.pdf`  
    *Peran:* Saliency map efisien untuk visualisasi filter token pada prototype Streamlit.

---

## 6. Preprocessing & Word Representation (`research/06_preprocessing_representation/`)
27. **IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding (2020)**  
    *Wilie et al.* | [arXiv:2009.05387](https://arxiv.org/abs/2009.05387)  
    *File:* `research/06_preprocessing_representation/2020_IndoNLU_Indo4B_Embeddings_Resources.pdf`  
    *Peran:* Pre-trained Indonesian FastText & Word2Vec (Indo4B), penanganan teks informal vs formal, dan vocabulary benchmark.
28. **IndoRobusta: Towards Robustness Against Diverse Code-Mixed Indonesian Local Languages (2023)**  
    *Koto et al.* | [arXiv:2311.12405](https://arxiv.org/abs/2311.12405)  
    *File:* `research/06_preprocessing_representation/2023_IndoRobusta_Indonesian_CodeMixed_Slang_Robustness.pdf`  
    *Peran:* Ketahanan model terhadap variasi dialek daerah, typo, slang, dan strategi tokenisasi subword.
29. **SEAHateCheck: Functional Tests for Detecting Hate Speech in Low-Resource Languages of Southeast Asia (2026)**  
    *arXiv:2603.16070* | [arXiv:2603.16070](https://arxiv.org/abs/2603.16070)  
    *File:* `research/06_preprocessing_representation/2026_SEAHateCheck_Southeast_Asia_Hate_Speech_Obfuscation.pdf`  
    *Peran:* Uji fungsional kebocoran model terhadap penyamaran ejaan (*obfuscation*), leet-speak, negasi, dan variasi ejaan bahasa Indonesia.
30. **Hate Content Detection via Novel Pre-Processing Sequencing and Ensemble Methods (2024)**  
    *Chhabra & Vishwakarma* | [arXiv:2409.05134](https://arxiv.org/abs/2409.05134)  
    *File:* `research/06_preprocessing_representation/2024_Hate_Content_Detection_Preprocessing_Sequencing.pdf`  
    *Peran:* Analisis urutan preprocessing, pembersihan tanda baca, stopwords, dan perbandingan dampak lemmatization/stemming vs non-stemming pada deep learning.
