db = {
    'user': '',
    'password' : '',
    'host' : '',
    'port' : 5432,
    'database' : ''
}

DB_URL = f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"