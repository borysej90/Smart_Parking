from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

# Set where db is going to be
# Currently - in current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Create model and columns for sqlalchemy DB
class ParkingModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_lots = db.Column(db.Integer, nullable=False)
    free_lots = db.Column(db.Integer, nullable=True)

# Initialize DB
# NOTE: Run only once so you won't initialize DB every time you run script!!!!!!!!!!!!!!!
# db.create_all()

# Arg parser for PUT
parking_put_args = reqparse.RequestParser()
parking_put_args.add_argument("total_lots", type=int, help="Total number of lots in parking space", required = True)
parking_put_args.add_argument("free_lots", type=int, help="Number of available lots in parking space", required = True)

# Arg parser for UPDATE(patch)
parking_update_args = reqparse.RequestParser()
parking_update_args.add_argument("total_lots", type=int, help="Total number of lots in parking space")
parking_update_args.add_argument("free_lots", type=int, help="Number of available lots in parking space")



resource_filed = {
    'id': fields.Integer,
    'total_lots': fields.Integer,
    'free_lots': fields.Integer
}

class Parking(Resource):
    """

    BASIC GET REQUEST :
        BASE = 'http://127.0.0.1:5000/'
        response = requests.get(BASE + "parking/1")
        print(response.json())

    BASIC PUT REQUSET :
        BASE = 'http://127.0.0.1:5000/'
        response = request.put(BASE + parking/1,{"total_lots":10,"free_lots":4})
        print(response.json())

    BASIC UPDATE AND DELETE WILL BE ADDED LATER
    """
    @marshal_with(resource_filed)
    def get(self,parking_id):

        # Find specified parking
        result = ParkingModel.query.filter_by(id=parking_id).first()

        # Check if parking with specified id exists
        if not result:
            abort(404, message="Could not find parking space with this id")

        return result

    @marshal_with(resource_filed)
    def put(self,parking_id):

        # Read args
        args = parking_put_args.parse_args()

        # Check if there are no parkings with such id
        if ParkingModel.query.filter_by(id=parking_id).first():
            abort(409, message = 'Parking id already exists')

        # Create new parking instance
        parking = ParkingModel(id=parking_id, total_lots=args['total_lots'], free_lots=args['free_lots'])

        # Add new instance to DB
        db.session.add(parking)
        db.session.commit()

        # Return instance and 201 code
        return parking,201

    # NOT WORKING IN THIS ISSUE
    @marshal_with(resource_filed)
    def patch(self, parking_id):

        args = parking_update_args.parse_args()

        result = ParkingModel.query.filter_by(id=parking_id).first()

        if not result:
            abort(404, message="Parking spot does not exist, cannot update")

        if args['total_lots']:
            ParkingModel.total_lots = args['total_lots']
        if args['free_lots']:
            ParkingModel.free_lots = args['free_lots']

        db.session.commit()

        return result

    # WILL ADD LATER
    def delete(self, parking_id):
        pass

api.add_resource(Parking, "/parking/<int:parking_id>")


if __name__ == '__main__':
    """
    DO NOT USE "debug = True" on production deployment
    """
    app.run(debug=True)
