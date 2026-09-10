# Contributing Guide — IndoToxic Project

## 🛠 Setup Development Environment

### Prerequisites
- Python 3.10+
- Docker & docker-compose
- Git
- Make (opsional, sangat direkomendasikan)

### Quick Start
```bash
# 1. Clone repository
git clone https://github.com/Josshua-DSA/Vox.git
cd Vox

# 2. Setup environment (venv + dependencies + dev tools)
make setup

# 3. Jalankan database PostgreSQL
cp .env.example .env
make db-up

# 4. Migrasi dataset ke database
make migrate

# 5. Verifikasi: jalankan test
make test
```

### Manual Setup (tanpa Make)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
docker-compose up -d
python scripts/migrate_csv_to_postgres.py
pytest tests/ -v
```

---

## 📏 Code Style & Linting

Project ini menggunakan **Ruff** sebagai linter dan formatter.

```bash
# Cek lint errors
make lint

# Auto-format kode
make format
```

Konfigurasi ada di `pyproject.toml` section `[tool.ruff]`. Rules utama:
- Line length: 120
- Target: Python 3.10+
- Checks: pycodestyle, pyflakes, isort, pep8-naming, pyupgrade

---

## 🧪 Testing

Semua test menggunakan **pytest** dengan shared fixtures di `tests/conftest.py`.

```bash
# Jalankan semua test
make test

# Jalankan test spesifik
.venv/bin/pytest tests/test_database.py -v
```

⚠️ Test database membutuhkan PostgreSQL container berjalan (`make db-up`).

---

## 🌿 Branch & PR Workflow

### Branch Naming
```
feature/<deskripsi>    # Fitur baru
fix/<deskripsi>        # Bug fix
docs/<deskripsi>       # Dokumentasi
infra/<deskripsi>      # CI/CD, Docker, config
test/<deskripsi>       # Penambahan/perbaikan test
```

### Commit Convention
Gunakan **Conventional Commits**:
```
type(scope): deskripsi singkat

Contoh:
feat(database): tambah repository layer untuk auto-scraping
fix(preprocessing): perbaiki regex cleaner untuk karakter unicode
docs: update README dengan panduan setup database
test(evaluation): tambah test case untuk edge case macro-f1
infra: konfigurasi CI/CD GitHub Actions workflow
```

### Pull Request Flow
1. Buat branch dari `main`:
   ```bash
   git checkout main && git pull origin main
   git checkout -b feature/nama-fitur
   ```
2. Kerjakan perubahan, commit granular (1 file / 1 commit jika memungkinkan).
3. Pastikan lint dan test pass sebelum push:
   ```bash
   make lint
   make test
   ```
4. Push dan buat Pull Request ke `main`.
5. Tunggu review dari minimal 1 anggota tim.
6. CI pipeline (lint + test) harus hijau sebelum merge.

---

## 📁 Struktur Modul

| Direktori | Tanggung Jawab |
|---|---|
| `src/database/` | PostgreSQL models, connection, repository |
| `src/preprocessing/` | Text cleaning, tokenization, padding, splitting |
| `src/models/` | CNN model architecture, embedding loader |
| `src/training/` | Trainer, imbalance handler |
| `src/evaluation/` | Metrics, confusion matrix, error analysis |
| `src/explainability/` | Saliency mapping |
| `src/utils/` | Config, logger, seed |
| `scripts/` | Automation scripts (migrasi, dll) |
| `tests/` | Unit tests + conftest.py |
| `app/` | Streamlit UI prototype |

---

## ⚠️ Yang Tidak Boleh Di-commit

- File `.env` (gunakan `.env.example` sebagai template)
- Folder `__pycache__/`, `.pytest_cache/`
- Model weights besar (`*.h5`, `*.pt`, `*.bin`, `*.pkl`)
- PDF penelitian (track via `research/PAPERS.md`)
- Folder `context/` (dokumen internal lokal)
