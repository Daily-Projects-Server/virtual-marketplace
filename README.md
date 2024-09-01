# Virtual Marketplace

## ⚙️ Setup Backend

### Clone the Repo
`git clone https://github.com/Daily-Projects-Server/virtual-marketplace.git`

### Navigate to backend directory
> cd virtual-marketplace/backend

### Setup Virtual Environment
`python -m venv <VENV_NAME>`
> if you are on Linux you can activate it with `source venv/bin/activate`

### Install dependencies
> pip install -r requirements.txt

### Setup `.env`
> To access the secrets, create an .env file in the backend directory

### For Database setup
By default, django is setup with `sqlite3`. For this project, set `DATABASE_URL` in your `.env` to set the database

#### For sqlite3
> DATABASE_URL="sqlite:////Path\\To\\Your\\Project\\db.sqlite3"

Note that four `/` after `sqlite:` are mandatory

*For windows users* -> `\\` after each folder is required

#### For PostgreSQL
> DATABASE_URL="postgres://username:password@HOSTNAME:PORT/DATABASE_NAME

*Examples are given in `.env.sample`*

### Migrate the Database
> `python manage.py migrate`

### Create Superuser to access the admin panel (Optional)
> `python manage.py createsuperuser`

### Run local server (Runs on port 8000)
> `python manage.py runserver`


Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)
