from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm
from models import QuestionModel, ReplyModel
from exts import db
from decorators import login_require

bp = Blueprint("qa", __name__, url_prefix="/qa")


@bp.route("/mt")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("movieTalk.html", questions=questions)


@bp.route("/post", methods=['GET', 'POST'])
@login_require
def post():
    if request.method == 'GET':
        return render_template("post.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa/post"))


@bp.route("/dt/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    replies = ReplyModel.query.filter(
        (ReplyModel.question_id == question.id)
    ).all()
    print(question, replies)
    return render_template("detail.html", question=question, replies=replies)
