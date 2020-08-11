# stepik_teacher
 The Second project from stepik academia


## Installation

1. Install Python 3.7.6
2. Install pip and virtual environment
 `python3 -m venv venv`
 For Linux
 `source venv/bin/activate`
 For Windows
 `venv\Scripts\activate.bat`

3. Install dependencies
 Linux
 `pip install -r path-to-service\requirements.txt`
 Windows
 `pip install -r path-to-service/requirements.txt`

 4. Init initiall DB

 `flask db-tasks init_db`

## Commiting changes
Run pre-commit before commiting to repostitory
 `pre-commit --all-files`
