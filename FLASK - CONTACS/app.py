from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'lalo'
app.config['MYSQL_PASSWORD'] = '1743'
app.config['MYSQL_DB'] = 'flaskcontacs'
mysql = MySQL(app)
##Session
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT *FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_Contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact added sucessfully')
        return redirect(url_for('index'))


@app.route('/edit/<string:id>')
def get_Contact(id):
   cur = mysql.connection.cursor()
   cur.execute('SELECT *from contacts where id = {0}'. format(id))
   data = cur.fetchall()
   return render_template('edit_Contact.html', contact = data[0])

@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts where id = {0}'. format(id))
    mysql.connection.commit()
    flash('Contact removed successfully')
    return redirect(url_for('index'))

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        Update contacts
        SET fullname = %s,
        email = %s,
        phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact Updated Succesfully')
        return redirect(url_for('index'))

        
if __name__ == "__main__":
    app.run(port=3000, debug=True)
