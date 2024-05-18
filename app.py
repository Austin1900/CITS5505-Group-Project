from flask import Flask, jsonify,session,g, render_template
from config import Config
from exts import db
from models import UserModel, AnswerModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
# config settings
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def index():
    return render_template("index.html")


@app.before_request
def my_before_request():
    user_id= session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g,"user", user)
    else:
        setattr(g,"user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

@app.route('/db')
def db():
    # 查询数据库中的所有用户并返回JSON响应
    users = UserModel.query.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        })
    return jsonify(user_data)

@app.route('/answers')
def print_answers():
    # 查询数据库中的所有答案并返回 JSON 响应
    answers = AnswerModel.query.all()
    answer_data = []
    for answer in answers:
        answer_data.append({
            'id': answer.id,
            'content': answer.content,
            'create_time': answer.create_time,
            'question_id': answer.question_id,
            'author_id': answer.author_id
        })
    return jsonify(answer_data)

if __name__ == '__main__':
    app.run(debug=True)

