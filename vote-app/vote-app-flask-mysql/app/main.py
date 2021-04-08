from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import os
import random
import socket
import sys

app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config_file.cfg')
app.config.update(EXPLAIN_TEMPLATE_LOADING=True)

button1 = app.config['VOTE1VALUE']
button2 = app.config['VOTE2VALUE']
title = app.config['TITLE'] 
if 'TITLE' in os.environ:
  title  += '_' + os.environ['TITLE']


# cnx = mysql.connector.connect(
# user="mysqladmin@my-my-sql-srv", 
# password={your_password}, 
# host="my-my-sql-srv.mysql.database.azure.com", 
# port=3306, database={your_database}, 
# ssl_ca={ca-cert filename}, 
# ssl_verify_cert=true
# )
# MySQL configurations 
# https://flask-mysql.readthedocs.io/en/stable/#:~:text=Flask%2DMySQL%20is%20a%20Flask,features%20on%20the%20issues%20page.
app.config['MYSQL_ROOT_PASSWORD']     = os.environ['MYSQL_ROOT_PASSWORD']
app.config['MYSQL_DATABASE_USER']     = os.environ['MYSQL_DATABASE_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_DATABASE_PASSWORD']
app.config['MYSQL_DATABASE_DB']       = os.environ['MYSQL_DATABASE_DB']
app.config['MYSQL_DATABASE_HOST']     = os.environ['MYSQL_DATABASE_HOST']
app.config['MYSQL_DATABASE_PORT'] = int(os.environ['MYSQL_DATABASE_PORT'])

print("HELLO!")

# MySQL Object
mysql = MySQL()
mysql.init_app(app)

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    try:
        title = title + '_' + str(socket.gethostname())
    except:
        pass


@app.route('/', methods=['GET', 'POST'])
def index():

    try:
        # MySQL Connection
        connection = mysql.connect()
        cursor = connection.cursor()
    except Exception as err:
        print("Could not connecto to MySQL 1: ", err)

    try:
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS  `{os.environ['MYSQL_DATABASE_DB']}`.`{os.environ['MYSQL_DATABASE_DB']}` (`voteid` INT NOT NULL AUTO_INCREMENT,`votevalue` VARCHAR(45) NULL,PRIMARY KEY (`voteid`));''')
        print(cursor.fetchall())
    except Exception as err:
        print("Could not create DB in MySQL Server: ", err)

    # Vote tracking
    vote1 = 0
    vote2 = 0

    if request.method == 'GET':

        try:
            # MySQL Connection
            connection = mysql.connect()
            cursor = connection.cursor()

           
            # Get current values
            cursor.execute(f'''Select votevalue, count(votevalue) as count From {os.environ['MYSQL_DATABASE_DB']}.{os.environ['MYSQL_DATABASE_DB']}
            group by votevalue''')
            results = cursor.fetchall()
                

            # Parse results
            for i in results:
                if i[0] == app.config['VOTE1VALUE']:
                    vote1 = i[1]
                elif i[0] == app.config['VOTE2VALUE']:
                    vote2 = i[1]
        except Exception as err:
            print("Could not connecto to MySQL 2: ", err)
            vote1 = -1
            vote2 = -2
        # Return index with values
        return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':

            try:
                # Empty table and return results
                cursor.execute(f'''Delete FROM {os.environ['MYSQL_DATABASE_DB']}''')
                connection.commit()
            except Exception as err:
                print("Could not connecto to MySQL 3: ", err)
                vote1 = -1
                vote2 = -2            
            return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            try:
                cursor.execute(
                    f'''INSERT INTO {os.environ['MYSQL_DATABASE_DB']} (votevalue) VALUES (%s)''', (vote))
                connection.commit()

                # Get current values
                cursor.execute(f'''Select votevalue, count(votevalue) as count From {os.environ['MYSQL_DATABASE_DB']}.{os.environ['MYSQL_DATABASE_DB']}
                group by votevalue''')
                results = cursor.fetchall()
   
                # Parse results
                for i in results:
                    if i[0] == app.config['VOTE1VALUE']:
                        vote1 = i[1]
                    elif i[0] == app.config['VOTE2VALUE']:
                        vote2 = i[1]

            except Exception as err:
                print("Could not connecto to MySQL 4: ", err)
                vote1 = -1
                vote2 = -2  
            # Return results
            return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)


@app.route('/results')
def results():
    try:
        # MySQL Connection
        connection = mysql.connect()
        cursor = connection.cursor()

        # Get current values
        cursor.execute(f'''Select * FROM {os.environ['MYSQL_DATABASE_DB']}''')
        rv = cursor.fetchall()
    except Exception as err:
        print("Could not connecto to MySQL 5: ", err)
        rv=None
    return str(rv)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)