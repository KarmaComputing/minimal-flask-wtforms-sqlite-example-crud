# Flask WTforms Minimal example (CRUD)

Minimal example using WTforms with Fask + Sqlite database.

**WARNING** This project is vulnerable to SQL injection.


# How to use

Read `__init__.py`

Install `rye` https://rye.astral.sh/
Activate the rye python environment
`rye sync`

Seed database
```
flask --app forms shell
from forms import init_db

init_db
```

Run flask
`flaks --app forms run --port 5000 --debug`

Observe app
http://127.0.0.1:5000

