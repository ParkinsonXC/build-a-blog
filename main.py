from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
#The database
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body


#AFTER we have created the above items, we need to use a python shell to initalize our database.

@app.route('/blog', methods = ['GET'])
def index():

    blogs = Blog.query.all()

    return render_template('blogs.html', blogs=blogs)



@app.route('/newpost', methods = ['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blog-body']
        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/blog')
    else:
        return render_template('newpost.html')



if __name__ == "__main__":
    app.run()