# Projeto Integrador II — **Congelados “Sim Porque Não!?”**

Vitrine online com **cadastro** e **login**  
Stack: **Python (Flask)** · **HTML/CSS/JS** · **SQLAlchemy**  
Banco padrão (dev): **SQLite** (`app.db`)

---

## 🚀 Como rodar (dev, com SQLite)

```bash
# 1) (opcional) criar e ativar venv
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# 2) dependências
pip install --upgrade pip
pip install Flask Flask_SQLAlchemy

# 3) subir o servidor (pacote 'Projeto' com create_app)
flask --app Projeto run --port 5001

Acesse no navegador:

http://127.0.0.1:5001/vitrine

http://127.0.0.1:5001/login

http://127.0.0.1:5001/cadastro

Ajuste de banco (se estiver MySQL)

No arquivo Projeto/__init__.py, use SQLite no dev:

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
