# chess_tracker

Tracks recent US Chess tournament results for students and uploads them to Google Sheets.

---

## Requirements

- Python 3.10+
- A Google service account JSON file (`service_account.json`)
- Access to the target Google Spreadsheet

---

## Setup

### 1. Get the project files

**Option A — Download ZIP:**
1. Go to the GitHub repository page: https://github.com/alecmtz/chess_tracker
2. Click the green **Code** button → **Download ZIP**
3. Locate the downloaded ZIP file and extract it

**Option B — Clone with Git:**
```bash
git clone git@github.com:yourusername/chess_tracker.git
```

---

### 2. Open a terminal and navigate to the project folder

**Mac:**
1. Open **Terminal** (search for it in Spotlight with `Cmd + Space`)
2. Navigate to the project folder:

> Drag the folder into the Terminal window and it will fill in the path automatically.

**Windows:**
1. Open **Command Prompt** (search for `cmd` in the Start menu) or **PowerShell**
2. Navigate to the project folder:
```bash
cd C:\Users\YourName\Downloads\chess_tracker
```
> Replace `YourName` with your Windows username and adjust the path if you extracted it elsewhere.
> Tip: In File Explorer, hold `Shift` and right-click the project folder → **Open PowerShell window here** to open the terminal already in the right place.

---

### 3. Create a virtual environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### How to tell if it worked
 
After running the activate command, look at the beginning of your terminal line.
 
**✅ Activated — you should see `(venv)` at the start:**
 
Mac:
```
(venv) yourname@Macbook chess_tracker %
```
Windows:
```
(venv) C:\Users\YourName\Downloads\chess_tracker>
```
 
**❌ Not activated — no `(venv)` prefix:**
 
Mac:
```
yourname@Macbook chess_tracker %
```
Windows:
```
C:\Users\YourName\Downloads\chess_tracker>
```
 
> ⚠️ If you don't see `(venv)`, do not continue. Re-run the activate command above before moving on. You must activate the virtual environment every time you open a new terminal window.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

> ✅ You only need to do this **once**. The packages are saved inside the `venv` folder permanently. Do not delete the `venv` folder or you will need to repeat steps 3 and 4.

### 5. Add your service account file

Place your `service_account.json` file in the root of the project:

```
chess_tracker/
├── service_account.json   ← here
├── main.py
├── chess_api.py
├── chess_data.py
├── google_sheets.py
└── requirements.txt
```

> ⚠️ Never commit `service_account.json` to GitHub. It is already listed in `.gitignore`.

---

## Running the program
 
> ⚠️ The steps below must be repeated **every time** you want to run the program. You do not need to reinstall dependencies — just navigate, activate, and run.
 
**1. Open a terminal and navigate to the project folder** (see step 2 in Setup above)
 
**2. Activate the virtual environment**
 
Mac:
```bash
source venv/bin/activate
```
Windows:
```bash
venv\Scripts\activate
```
 
Make sure you see `(venv)` at the start of your terminal line before continuing.
 
**3. Run the program**
 
Mac:
```bash
python3 main.py
```
Windows:
```bash
python main.py
```

---

## What it does

1. Reads student US Chess IDs from the `Student Information` sheet in Google Sheets
2. Fetches recent tournament data from the US Chess API for each student
3. Filters to tournaments from the past week
4. Creates a new dated worksheet tab and uploads the results

---

## Troubleshooting

**`ModuleNotFoundError`** — Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

**`FileNotFoundError: service_account.json`** — Make sure the file is in the root of the project folder.

**`gspread.exceptions.APIError`** — Make sure the service account email has been granted access to the Google Spreadsheet.