# Virtual Marketplace

## ⚙️ Setup Backend

### Clone the Repo
`git clone https://github.com/Daily-Projects-Server/virtual-marketplace.git`

### Navigate to backend directory
> cd virtual-marketplace/backend

### Setup Virtual Environment
`python -m venv <VENV_NAME>`

### Install dependencies
> pip install -r requirements.txt

### Setup `.env`
> To access the secrets, create .env or rename .env.sample to .env

### Migrate the Database
> `python manage.py migrate`

### Create Superuser to access the admin panel (Optional)
> `python manage.py createsuperuser`

### Run local server (Runs on port 8000)
> `python manage.py runserver`


Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)
