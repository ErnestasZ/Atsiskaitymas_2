python -m venv .venv <!--  susikurti virtual evinronment -->
Use venv environment .venv

<!-- After clone install dependencies  -->
<!-- generate requirements -->

pip3 freeze > requirements.txt

<!-- update requirements  -->

pip install -r requirements.txt

<!-- flask db init (first time) -->

flask db upgrade

run file run.py

<!--  susimerginti i savo branch development branch'a -->

git pull
git pull origin development

<!-- How run faker db  -->

python -m Services.faker_db
