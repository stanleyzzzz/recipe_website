echo "lubuntu" | sudo -S apt-get update
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt -y update
sudo apt -y install curl
sudo apt -y install postgresql-14
sudo apt -y install python3-pip

pip install -U pip
pip install flask
pip install flask_restx
pip install flask_cors
pip install psycopg2-binary
pip install pytest

 sudo -u postgres -H -- psql -c "ALTER USER postgres PASSWORD 'fantasticpassword';" 