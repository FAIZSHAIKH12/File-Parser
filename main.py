from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)

class post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    description=db.Column(db.String(200))
    author=db.Column(db.String(50))

    def __init__(self,title,description,author):
        self.title=title
        self.description=description
        self.author=author

class PostSchema(ma.Schema):
    class Meta:
        fields=("title","author","description")

post_schema=PostSchema()
posts_schema=PostSchema(many=True)

@app.route('/post',methods =['POST'])
def add_post():
    title=request.json['title']
    description=request.json['description']
    author=request.json['author']

    my_posts=post(title,description,author)
    db.session.add(my_posts)
    db.session.commit()
    return post_schema.jsonify(my_posts)



@app.route('/get',methods=['GET'])
def get_post():
    all_posts=post.query.all()
    result=posts_schema.dump(all_posts)
    return jsonify(result)

@app.route('/post_details/<id>/',methods=['GET'])
def post_details(id):
    post=post.query.get(id)
    return post_schema.jsonify(post) 

@app.route('/post_update/<id>/',methods=['PUT'])
def post_update(id):
    p=post.query.get(id)
    title=request.json['title']
    description=request.json['description']
    author=request.json['author']

    p.title=title
    p.description=description
    p.author=author
    db.session.commit()
    return post_schema.dump(p)

@app.route('/post_delete/<id>/',methods=['DELETE'])
def post_delete(id):
    p=post.query.get(id)
    db.session.delete(p)
    db.session.commit()

    return post_schema.jsonify(p)


 
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
