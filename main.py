from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os, requests
from sqlalchemy import desc


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing_image.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Helper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, default=datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/articles', methods=['POST'])
def create_articles():
    title = request.form['title']
    content = request.form['content']
    pic = request.files['image']
    if not pic:
        return jsonify({'message': 'No image uploaded'}), 400
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    submit_id = Helper() 
    db.session.add(submit_id)
    get_id = Helper.query.order_by(Helper.id.desc()).first()
    submit = Article(title = title, content = content, image_url= 'https://'+request.host + '/articles/image/' + str(get_id.id), img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(submit)
    db.session.commit()
    return jsonify({'message': 'Article submit success'}), 201

@app.route('/articles', methods=['GET'])
def get_articles():
    reports = Article.query.order_by(desc(Article.id)).all()
    output = []
    for report in reports:
        report_data = {'id': report.id, 'title': report.title, 'content': report.content, 'image_url': report.image_url, 'created_at': report.created_at, 'updated_at': report.updated_at}
        output.append(report_data)
    return jsonify({'message':'Success','data': output})

@app.route('/articles/image/<int:img_id>', methods=['GET'])
def get_image(img_id):
    img = Article.query.filter_by(id=img_id).first()
    if not img:
        return jsonify({'message': 'Image not found'}), 404
    return Response( img.img, mimetype=img.mimetype) 

@app.route('/articles/<int:report_id>', methods=['DELETE'])
def del_admin_report(report_id):
    report = Article.query.filter_by(id=report_id).first()
    if not report:
        return jsonify({'message': 'Report not found'}), 404
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Report deleted successfully!'})

@app.route('/articles/<int:report_id>', methods=['GET'])
def del_admin_report(report_id):
    report = Article.query.filter_by(id=report_id).first()
    if not report:
        return jsonify({'message': 'Report not found'}), 404
    return jsonify({'message': 'Success', 'data':report})

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
