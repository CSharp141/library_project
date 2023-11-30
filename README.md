# library_project

## Operation:

these instructions are designed for once you open the library_project-main folder(folder name when downloaded directed from github as a zip) as a workspace in VSCode so slight differences may be present when using other IDEs or direct access.

### 1. Create a virtual environment
```bash
python -m venv env
```

### 3. Activate virtual environment
Linux/mac
```bash
source env/bin/activate
```
Windows
```bash
env\Scripts\activate
```

### 4. Install requirements
```bash
pip install -r requirements.txt
```

### 6. Run server this command must be run from the root folder
```bash
py manage.py runserver
```

### 7. Access server
Navigate to http://127.0.0.1:8000/ in your browser

## Default Accounts and Passwords 
### Student user
username = test

password = testPassword

### Staff user 
username = staff

password = staffPassword

### Librarian user
username = librarian

password = librarianPassword

### Admin user 
username = admin

password = adminPassword

### Hash test users 
username = hashTest1 or hashTest2

password = hashTestPassword
