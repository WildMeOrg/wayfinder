from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Link(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	label = db.Column(db.String(100), nullable=False)
	href = db.Column(db.String(421), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.String(200), nullable = False)
	completed = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f'<Task {self.id}>'

@app.route('/')
def index():
	links = Link.query.order_by(Link.date_created).all()
	return render_template('index.html', links=links)

@app.route('/delete/<int:id>')
def delete(id):
	link_to_update = Link.query.get_or_404(id)
	try:
		db.session.delete(link_to_update)
		db.session.commit()
		return redirect('/edit')
	except:
		return 'Catastrophic failure'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	link_to_update = Link.query.get_or_404(id)

	if request.method == 'POST':
		link_to_update.label = request.form['label']
		link_to_update.href = request.form['href']
		try:
			db.session.commit()
			return redirect('/edit')
		except:
			return 'Catastrophic failure'
	else:
		return render_template('update.html', link=link_to_update)

@app.route('/add', methods=['GET', 'POST'])
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
		except:
			return 'Catastrophic failure'
	elif request.method == 'GET':
		return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	links = Link.query.order_by(Link.date_created).all()
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		return render_template('edit.html', links=links)

if __name__ == '__main__':
	app.run(debug=True)
