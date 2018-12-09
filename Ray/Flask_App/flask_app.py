from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [

	{

		'author': 'Lukas Frei yo',
		'title': 'Post',
		'date': 'April 20, 2018'


	},

	{

		'author': 'Jane Doe',
		'title': 'Post 2',
		'date': 'April 21, 2018'


	}



]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title=about)


 

if __name__ == '__main__':
	app.run(debug=True)