from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coords.db'
db = SQLAlchemy(app)
api = Api(app)

class coordModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coords = db.Column(db.String(100),nullable=False)
    #coords1 = db.Column(db.String(100),nullable=False)
    #coords2 = db.Column(db.String(100),nullable=False)
    #coords3 = db.Column(db.String(100),nullable=False)
    #coords4 = db.Column(db.String(100),nullable=False)
    #coords5 = db.Column(db.String(100),nullable=False)
    #coords6 = db.Column(db.String(100),nullable=False)
    #coords7 = db.Column(db.String(100),nullable=False)
    #coords8 = db.Column(db.String(100),nullable=False)
    #coords9 = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Coords = {self.coords}"
    
coord_args = reqparse.RequestParser()
coord_args.add_argument('coords', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords1', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords2', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords3', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords4', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords5', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords6', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords7', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords8', type=str, required=True, help="Coord string can't be empty")
#coord_args.add_argument('coords9', type=str, required=True, help="Coord string can't be empty")

coordFields = {
    'id':fields.Integer,
    'coords':fields.String,
    #'coords1':fields.String,
    #'coords2':fields.String,
    #'coords3':fields.String,
    #'coords4':fields.String,
    #'coords5':fields.String,
    #'coords6':fields.String,
    #'coords7':fields.String,
    #'coords8':fields.String,
    #'coords9':fields.String,
    
}

class Coords(Resource):
    @marshal_with(coordFields)
    def get(self):
        coords = coordModel.query.all()
        return coords
    
    @marshal_with(coordFields)
    def post(self):
        args = coord_args.parse_args()
        coordinate = coordModel(coords=args["coords"])
        db.session.add(coordinate)
        db.session.commit()
        coordinates = coordModel.query.all()
        return coordinates, 201
    
    @marshal_with(coordFields)
    def delete(self):
        coordModel.query.delete()
        db.session.commit()
        coords = coordModel.query.all()
        return coords, 204




    
api.add_resource(Coords, '/api/coords/')

@app.route('/')
def home():
    
    response = requests.get('http://127.0.0.1:5500/api/coords/')
    dataR = response.json()
    #dataTest = 'Hello'

    

    return render_template("index.html",data=dataR)
    '''
    for i in data:
        #print(i['coords'])
        dataStr = i['coords']
        return render_template("index.html" data=dataStr) 
    '''

    #return '</h1>Coordinate streaming API</h1>'

if __name__ == '__main__':
    app.run(debug=True,port=5500)