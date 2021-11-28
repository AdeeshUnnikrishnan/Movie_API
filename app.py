from models.movies import app, User, Movies, db
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import datetime
import jwt
#------------------------------------------------------Getting Users ----------------------------------------------------------------

@app.route('/user',methods=['GET'])

def get_all_users():

    users = User.query.all() 
    output = [] 
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['genre'] = user.genre
        output.append(user_data)
    return jsonify({"users":output})


@app.route('/user/<id>',methods=['GET'])
def get_one_user(id): 
    user = User.query.filter_by(public_id=id).first()
    if not user:
        return jsonify({"message":"user not found"})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['genre'] = user.genre
    return jsonify({"user":user_data})

#-------------------------------------------------------------Creating User-------------------------------
@app.route('/user',methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'],method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password,genre=data["genre"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'New User Created !'})

#-------------------------------------------------------------Authentication-------------------------------
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not Login', 401, {'WWW-Authenticate':'Basic realm="Login required!'}) 

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Invalid Username', 401, {'WWW-Authenticate':'Basic realm="Login required!'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id':user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config["SECRET_KEY"])

        return jsonify({'token':token})

    return make_response('Invalid Password', 401, {'WWW-Authenticate':'Basic realm="Login required!'})

#-------------------------------------------------------------Movie Routes [POST]------------------------------------------
@app.route("/movie/<id>/create", methods=['POST'])
def create_movie(id):
    data = request.get_json()

    new_movie = Movies(movie_name=data['movie_name'],
        genre=data["genre"],
        Up_vote=data['Up_vote'],
        Down_vote=data['Down_vote'],
        review = data['review'],
        user_id=id)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({"Message":"Data Created"})

#-------------------------------------------------------------Movie Routes [GET]------------------------------------------
@app.route("/movie/public",methods=["GET"])
def get_movies():
    movies = Movies.query.all() 
    output = []  
    for movie in movies:
        movie_data = {} # creating a dict
        movie_data['movie_name'] = movie.movie_name
        movie_data['genre'] = movie.genre
        movie_data['Up_vote'] = movie.Up_vote
        movie_data['Down_vote'] = movie.Down_vote
        movie_data['review'] = movie.review
        
        output.append(movie_data)
    return jsonify({"movies":output})

@app.route("/movies/<g>", methods=['GET'])
def get_movies_id_genre(g):
    M = Movies.query.filter((Movies.genre==g)).all()
    output = [] 
    for movie in M:
        movie_data = {} 
        movie_data['movie_name'] = movie.movie_name
        movie_data['genre'] = movie.genre
        movie_data['Up_vote'] = movie.Up_vote
        movie_data['Down_vote'] = movie.Down_vote
        movie_data['review'] = movie.review
        
        output.append(movie_data)
    return jsonify({"movies":output})
#-------------------------------------------------------------Movie Routes [GET] DownVote/UpVote------------------------------------------
@app.route("/movies/Down_vote/", methods=['GET'])
def get_movies_Down_Vote():
    M = Movies.query.order_by((Movies.Down_vote)).all()
    output = [] 
    for movie in M:
        movie_data = {} 
        movie_data['movie_name'] = movie.movie_name
        movie_data['genre'] = movie.genre
        movie_data['Up_vote'] = movie.Up_vote
        movie_data['Down_vote'] = movie.Down_vote
        movie_data['review'] = movie.review
        
        output.append(movie_data)
    return jsonify({"movies":output})

@app.route("/movies/Up_vote/", methods=['GET'])
def get_movies_Up_Vote():
    M = Movies.query.order_by((Movies.Up_vote)).all()
    output = [] 
    for movie in M:
        movie_data = {} 
        movie_data['movie_name'] = movie.movie_name
        movie_data['genre'] = movie.genre
        movie_data['Up_vote'] = movie.Up_vote
        movie_data['Down_vote'] = movie.Down_vote
        movie_data['review'] = movie.review
        
        output.append(movie_data)
    return jsonify({"movies":output})

if __name__ == '__main__':
    app.run(debug=True)