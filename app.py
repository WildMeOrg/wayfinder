from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from config import users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

def log_error_info(e):
	print('Encountered an error!')
	print(str(e))
	print(f'Args: {e.args}')

class Link(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	label = db.Column(db.String(100), nullable=False)
	href = db.Column(db.String(421), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f'<Link {self.id}>'

db.create_all()

@auth.verify_password
def verify_password(username, password):
	if username in users and \
	          check_password_hash(users.get(username), password):
		return username

@app.route('/')
def index():
	links = Link.query.order_by(Link.date_created).all()
	return render_template('index.html', links=links)

@app.route('/delete/<int:id>')
@auth.login_required
def delete(id):
	link_to_update = Link.query.get_or_404(id)
	try:
		db.session.delete(link_to_update)
		db.session.commit()
		return redirect('/edit')
	except Exception as e:
		log_error_info(e)
		return 'Catastrophic failure'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def update(id):
	link_to_update = Link.query.get_or_404(id)

	if request.method == 'POST':
		link_to_update.label = request.form['label']
		link_to_update.href = request.form['href']
		try:
			db.session.commit()
			return redirect('/edit')
		except Exception as e:
			log_error_info(e)
			return 'Catastrophic failure'
	else:
		return render_template('update.html', link=link_to_update)

@app.route('/add', methods=['GET', 'POST'])
@auth.login_required
def add():
	if request.method == 'POST':
		print(request.form)
		new_label = request.form['label']
		new_href = request.form['href']
		print(new_label)
		print(new_href)
		new_link = Link(label=new_label, href=new_href)
		try:
			db.session.add(new_link)
			db.session.commit()
			return redirect('/edit')
		except Exception as e:
			log_error_info(e)
	elif request.method == 'GET':
		return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
@auth.login_required
def edit():
	links = Link.query.order_by(Link.date_created).all()
	return render_template('edit.html', links=links)

if __name__ == '__main__':
	app.run(debug=True)
