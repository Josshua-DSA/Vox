# Direktori Riset Leksikon Bahasa Kotor & Hate Speech Indonesia (`research/EDA_bahasa_kotor`)

Dokumen katalog dan referensi leksikon kata makian, ujaran kebencian (*hate speech*), kata vulgar/profanity, dan kata kunci scraping (*seed keywords*) yang relevan untuk analisis dataset **IndoToxic2024** / **IndoDiscourse**.

---

## 1. Ringkasan Berkas & Sumber Data

| Nama File | Format | Jumlah Entri | Sumber / Asal | Peran / Kategori Utama |
|---|---|---:|---|---|
| `susanto2024_scraping_keywords.json` | JSON | 67 kata (8 topik) | Susanto et al. (2024) [arXiv:2406.19349v2](https://arxiv.org/abs/2406.19349) | **Ground Truth Scraping Keywords** (seed pencarian data IndoToxic) |
| `susanto2024_scraping_keywords.csv` | CSV | 67 baris | Susanto et al. (2024) [arXiv:2406.19349v2](https://arxiv.org/abs/2406.19349) | Versi tabel per-topik kata kunci scraping |
| `ibrohim_budi_abusive.csv` | CSV | 125 kata | Ibrohim & Budi (2019) [GitHub Repo](https://github.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection) | **Standar Baseline NLP Indonesia** (kata makian/abusive umum) |
| `drizki_badwords.json` | JSON | 210 kata | drizki [GitHub Repo](https://github.com/drizki/indonesian-badwords) | Kamus badwords & slang kotor Indonesia |
| `abaron_profanity.txt` | TXT | 438 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Kata makian vulgar/kotor (`profanity_obscenity`) |
| `abaron_harassment.txt` | TXT | 259 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Hinaan & cercaan personal (`insults`) |
| `abaron_hate_speech.txt` | TXT | 171 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Ujaran kebencian berbasis identitas/SARA (`identity_attack`) |
| `abaron_violence.txt` | TXT | 193 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Ancaman kekerasan fisik (`threat_incitement_to_violence`) |
| `abaron_sexual.txt` | TXT | 283 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Istilah seksual vulgar (`sexually_explicit`) |
| `abaron_spam.txt` | TXT | 367 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Kata-kata promosi, judi, obat, dan spam (`is_noise_or_spam`) |
| `abaron_reserved.txt` | TXT | 306 baris | abaron [GitHub Repo](https://github.com/abaron/bad-words) | Istilah sensitif cadangan / domain-spesifik |

---

## 2. Pemetaan Langsung ke 5 Sub-label IndoToxic2024

Dataset IndoToxic2024 memiliki 5 sub-label toksisitas. Berkas-berkas di atas terpetakan secara presisi:

```
┌──────────────────────────────────────┬─────────────────────────────┬────────────────────────────────────────────────────────┐
│ Sub-label IndoToxic (Raw Schema)     │ File Leksikon Referensi     │ Contoh Kata Kunci                                      │
├──────────────────────────────────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ profanity_obscenity                  │ abaron_profanity.txt        │ anjing, bangsat, jancuk, kontol, memek, tai, puki      │
│                                      │ ibrohim_budi_abusive.csv    │                                                        │
├──────────────────────────────────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ insults                              │ abaron_harassment.txt       │ bego, tolol, bodoh, dungu, idiot, pengecut, muka tembok│
├──────────────────────────────────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ identity_attack                      │ abaron_hate_speech.txt      │ kadrun, cebong, antek aseng, cina loleng, kafir, wahabi│
│                                      │ susanto2024_scraping_*.json │                                                        │
├──────────────────────────────────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ threat_incitement_to_violence        │ abaron_violence.txt         │ bantai, bunuh, bacok, gantung, habisi, mutilasi, tembak│
├──────────────────────────────────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ sexually_explicit                    │ abaron_sexual.txt           │ bokep, colmek, ngentot, tobrut, sange, open bo, vcs    │
└──────────────────────────────────────┴─────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 3. Relevansi Penemuan Terhadap Temuan EDA & Wave 2

1. **Mengapa Subjek Geopolitik/Agama Frekuensinya Masif di Dataset?**
   - Dalam file `susanto2024_scraping_keywords.json`, Susanto et al. mengonfirmasi bahwa kata seperti `israel`, `palestina`, `syiah`, `cina`, `tionghoa`, `yahudi`, `zionis` adalah **seed keywords pengumpul korpus**, bukan kata makian.
   - Oleh karena itu, kata-kata tersebut sering muncul di kelas non-toxic maupun toxic.

2. **Kesesuaian dengan Log-Odds Wave 2**:
   - Kata-kata dengan log-odds tertinggi di kelas toxic IndoToxic (`kontol` 4.01, `bego` 3.38, `pengecut` 3.19, `kadrun` 2.83, `bangsat` 2.81, `tolol` 2.71, `pesek` 2.67, `wahabi` 2.63, `iblis` 2.61, `goblok` 2.49) beririsan 100% dengan leksikon `ibrohim_budi_abusive.csv` dan `abaron_profanity.txt` / `abaron_harassment.txt`.

---

## 4. Potensi Pemanfaatan di Tahap Modeling (Sesuai `context/PLAN.md`)

- **Fitur Hitungan Kata Kasar (*Abusive Word Count Feature*)**:
  Sesuai PyCaret-Indonesia §3.2 dan model `dictNN` (Kupi et al., 2021; arXiv:2103.08780), jumlah kemunculan kata yang cocok dengan leksikon ini dapat diinjeksikan sebagai *handcrafted feature vector* ke Dense Layer arsitektur CNN.
- **Data Integrity Rule**:
  Leksikon ini bersifat referensi/fitur eksternal; dataset mentah `data/raw/` tetap tidak boleh dimutasi.
