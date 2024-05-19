from flask import Flask, render_template, session, g, jsonify, request
from flask_migrate import Migrate

from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from config import Config
from exts import db
from forms import SearchForm
from models import UserModel, Post, QuestionModel, ReplyModel

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

from exts import db as db1


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm(request.form)
    posts = Post.query.all()
    if form.validate():
        query = form.query.data
        posts = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) |
            (Post.content.ilike(f'%{query}%'))
        ).all()
    return render_template("index.html", form=form, posts=posts)

@app.route('/movieTalk', methods=["GET", "POST"])
def movie_talk():
    if request.method == 'POST':
        data = request.form.to_dict()
        question = QuestionModel(title=data.get('title'), content=data.get('content'), author_id=g.user.id)
        db1.session.add(question)
        db1.session.commit()

    search = request.args.get('search', '')
    questions = QuestionModel.query.filter(
        (QuestionModel.title.ilike(f'%{search}%'))
    )
    return render_template('movieTalk.html', questions=questions)


@app.route('/reply', methods=["GET", "POST"])
def reply():
    if request.method == 'POST':
        data = request.form.to_dict()
        reply_db = ReplyModel(content=data.get('content'), user_id=g.user.id, question_id=data.get('question_id'))
        db1.session.add(reply_db)
        db1.session.commit()

    search = request.args.get('search', '')
    questions = QuestionModel.query.filter(
        (QuestionModel.title.ilike(f'%{search}%'))
    )
    return render_template('movieTalk.html', questions=questions)


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}

@app.route('/mn')
def mn():
    return render_template("movie-news.html")

@app.route('/movie1')
def movie1():
    return render_template("movie1.html")
@app.route('/movie2')
def movie2():
    return render_template("movie2.html")
@app.route('/movie3')
def movie3():
    return render_template("movie3.html")
@app.route('/movie4')
def movie4():
    return render_template("movie4.html")

@app.route('/mc')
def mc():
    return render_template("movie-column.html")

if __name__ == '__main__':
    app.run(debug=True)
