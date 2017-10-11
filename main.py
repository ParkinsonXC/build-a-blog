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
    #CHECK for query param. If not present, move onto the main blog page where they are all displayed.
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('displaypost.html', blog=blog)

    else:
        blogs = Blog.query.all() #TRY A FILTER_BY HERE to change the order the blogs appear in
        return render_template('blogs.html', blogs=blogs)


@app.route('/newpost')
def display_newpost_form():
    return render_template('newpost.html')

@app.route('/newpost', methods = ['POST'])
def add_blog():
    blog_title = request.form['title']
    blog_body = request.form['blog-body']
    #SET CONDITIONALS TO CHECK IF EITHER THE TITLE OR THE POST IS LEFT EMPTY

    title_error = ""
    body_error = ""

    if len(blog_title) == 0:
        title_error = "Your blog needs a title!"

    if len(blog_body) == 0:
        body_error = "Type a post! There's nothing here yet!"

    #If not, we are good to go. Initialize the new post into the class/database, add it, then commit it.
    #After it has been committed, it will have an ID. Use that to redirect to the post itself.
    if not title_error and not body_error:
        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog?id={}'.format(new_post.id))
        
        
    else:
        return render_template('newpost.html',
        title_error=title_error,
        body_error=body_error)


if __name__ == "__main__":
    app.run()