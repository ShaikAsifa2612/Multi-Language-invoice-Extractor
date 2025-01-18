INSTALLATION OF MySQL:

[Click Me!! to see Tutorial](https://www.youtube.com/watch?v=u96rVINbAUI)

Now,
Also install MySQL extension in VS Code by Weijan Chen

In activity bar click on MySQL icon to open Database explorer panel

Now,
Click on create connection or add connection

Host:localhost
Port: 3306 (During installation and setup of MySQL Workbench you will be given 3306 as default port if you                change it there please change it over here)
username: <username>
password: <password>

In cmd, 

pip install mysql-connector-python
pip install Flask mysql-connector-python
pip install Flask-mysqldb
pip install -r requirements.txt
(There is a requirements.txt, to check give prompt as 'pip list', the list shall contain 'Flask', 'Flask-MySQLdb', 'mysqlclient')



