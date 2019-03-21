# SteemChain v1.3.0

Dashboard application for analysing and charting transactions and operations from the STEEM Blockchain.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

The application is set up to use a Mysql database.

```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install mysql-server
```

Secure mysql and set up database and user.
```
mysql_secure_installation
mysql -u root -p

CREATE DATABASE steem_dashboard;
GRANT ALL PRIVILEGES ON steem_dashboard.* TO 'dashboard'@'localhost' IDENTIFIED BY '<password>';
FLUSH privileges;
exit
```

Install required packages and virtual environment.

```
sudo apt install default-libmysqlclient-dev python3-pip libssl-dev
pip3 install pipenv 
```

### Installing

A step by step series of examples that tell you how to get a development env running

Download the code from github.

```
git clone https://github.com/Juless89/steem-dashboard.git
```


Install the virtual enviroment
```
cd steem_dashboard
pipenv install
```
Enter virtual environment and create settings.cnf

```
pipenv shell
nano front-end/settings.cnf
```

Settings.cnf should be as follow:
```
[client]
database = steem_dashboard
user = 
password = 
```

When everything is done correctly the models can be migrated
```
cd front-end
python manage.py migrate

```

## Deployment

Run the Django server as is or set up with a custom webserver.

```
python manage.py runserver 0.0.0.0:8000
```

The back end has can be used in head mode or scraping mode. Head mode continues from the last collected block updates the database on every block and only uses 1 thread. The scraping requires: start block, amount of blocks and amount of threads to be used. For scarping a temp folder is required.


```
cd back-end
mkdir temp

# scrape mode
python main.py 30000000 28800 32

# head mode
python main.py
```

## Built With

* [Django Framework](https://github.com/django/django) - The web framework used
* [Django REST Framework](https://github.com/django/django) - The REST framework used
* [Bootstrap](https://getbootstrap.com/) - HTML/CSS Framework
* [Charts.js](https://www.chartjs.org/) - Javascript charts library


## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Julian Kramer** - *Initial work* - [Juless89](https://github.com/Juless89)

## License

This project is licensed under the GIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This projected is contributed to [Utopian-io](https://colony.utopian.io/) a platform for open source collaboration, home to all digital professionals with a passion for open source innovation. Utopian Colony gives everyone a voice and a place to contribute, reward and be rewarded.
