
# SafeBank - Modified BankBot (Demo)

This project is a modified copy of a BankBot-style Flask application with:
- Different frontend design (templates + CSS intentionally changed)
- Updated login credentials (username: **Ruthish**, password: **qwe@123**)
- A placeholder training script (train.py) to match original workflow

## Files
- app.py - Flask application (entrypoint)
- train.py - Placeholder training script
- templates/ - HTML templates (login, dashboard, chat)
- static/ - CSS and static assets
- requirements.txt - Python dependencies
- infosys_springboard_notes.pdf - (copied reference)
- BankBot_Deployment_Guide.pdf - (copied reference)

## Local run (same flow as original deployment guide)
1. Create virtualenv & install dependencies:
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt

2. Train (placeholder):
   python train.py

3. Run:
   python app.py
   Open http://127.0.0.1:5000
   Login with: username: Ruthish   password: qwe@123

## Deploying to Render (mirrors the original BankBot_Deployment_Guide)
1. Push this project to GitHub.
2. Create a new Web Service on Render, connect to the repository.
3. Set Start Command to:
   web: gunicorn app:app
4. Deploy.

For detailed deployment steps please refer to the included `BankBot_Deployment_Guide.pdf` and `infosys_springboard_notes.pdf` (they were provided by you and are included here as references).
