from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


app = Flask(__name__)
api = Api(app)

# Set where db is going to be
# Currently - in current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Model for parking sites
class Sites(db.Model):
    __tablename__ = "sites"

    id = db.Column(db.Integer, primary_key=True)
    lots = relationship("Lots", backref='site')
    address = db.Column(db.String(50))

# Model for parking lots
class Lots(db.Model):
    __tablename__ = "lots"

    id = db.Column(db.Integer, primary_key=True)
    lot_number = db.Column(db.Integer)
    is_paid = db.Column(db.Boolean)
    site_id = db.Column(db.Integer, ForeignKey('sites.id'))

# Initialize DB
# NOTE: Run only once so you won't initialize DB every time you run script!!!!!!!!!!!!!!!
db.create_all()

lot_resource_filed = {
    'site_id': fields.Integer,
    'lot_id': fields.Integer,
    'is_paid': fields.Boolean,
    'lot_number': fields.Integer,
    'address': fields.String(50)
}
site_resource_field = {
    'id': fields.Integer,
    'address': fields.String(50)
}
class GetParkingLot(Resource):
    @marshal_with(lot_resource_filed)
    def get(self, address, lot_number):
        """
            THIS CLASS IS USED TO GET PARKING LOTS ONLY

            BASIC GET REQUEST :

            BASE = 'http://127.0.0.1:5000/'
            response = requests.get(BASE + "parking/Prospect_Ratushnyaka/lot_number/1")
            print(response.json())
        """

        # Find specified parking site
        site = Sites.query.filter_by(address=address).first()

        # Check if site exists
        if site:

            lot = Lots.query.filter_by(site=site, lot_number=lot_number).first()

            # Check if lot exists
            if not lot:
                 abort(404, message=f"Could not find parking lot with number - {lot_number}")

            # Create and return result
            result = {'lot_id': lot.id, 'lot_number': lot.lot_number,
                      'is_paid': bool(lot.is_paid), 'site_id': site.id, 'address': site.address}
            return result
        # If site was not found
        elif not site:
            abort(404, message=f"Could not find parking site with address - {address}")


api.add_resource(GetParkingLot, "/parking/<string:address>/lot_number/<int:lot_number>")

class ParkingLot(Resource):
    """
    THIS CLASS IS USED TO CREATE PARKING LOTS ONLY

    BASIC POST REQUEST :

    BASE = 'http://127.0.0.1:5000/'
    response = requests.get(BASE + 'parking/Prospect_Ratushnyaka/lot_number/4/is_paid/1')
    print(response.json())

    """
    @marshal_with(lot_resource_filed)
    def post(self, is_paid, lot_number, address):

        # Find site with specified id
        site = Sites.query.filter_by(address=address).first()

        # If it exists
        if site:

            site_id = site.id

            # Check if specified lot number already exists and if there are any lots
            if len(site.lots) > 0  and Lots.query.filter_by(lot_number=lot_number).filter_by(site_id=site_id).first():
                abort(400, message=f'Lot with number - {lot_number} already exists in site with address - {address}')
            else:
                # Create lot
                lot = Lots(site=site, is_paid=bool(is_paid), lot_number=lot_number)

                # Add lot to db and commit
                db.session.add(lot)
                db.session.commit()

                #Create and return result
                result = {'lot_id': lot.id, 'site_id': site.id, 'lot_number': lot_number,
                          'is_paid': bool(is_paid), 'address': site.address}
                return result, 200

        elif not site:
            abort(404,
                  message=f"Parking site with address - {address} does not exist, please create parking site and then add lots")
            return None

api.add_resource(ParkingLot, "/parking/<string:address>/lot_number/<int:lot_number>/is_paid/<int:is_paid>")

class GetAllParkingSites(Resource):

    """
    THIS CLASS IS USED TO GET ALL PARKING LOTS THAT CORRESPOND
    TO SPECIFIED SITE

    BASIC REQUEST:

    BASE = 'http://127.0.0.1:5000/'
    response = requests.get(BASE + 'parking/Another_Prospect/all')
    print(response.json())

    """

    @marshal_with(lot_resource_filed)
    def get(self,address):
        result = []

        # Find parking site with specified address
        site = Sites.query.filter_by(address=address).first()

        # Check if site with specified address exists and has parking lots
        if not site:
            abort(404, message=f"Could not find parking site with this address - {address}")
        if len(site.lots) == 0:
            abort(404, message=f'Parking site with address - {address} has no parking lots')


        for lot in site.lots:
            result.append({'lot_id': lot.id, 'site_id': site.id, 'lot_number': lot.lot_number,
                          'is_paid': bool(lot.is_paid), 'address': site.address})

        return result, 200
api.add_resource(GetAllParkingSites, "/parking/<string:address>/all")


class ParkingSite(Resource):
    """
    THIS CLASS IS USED TO POST OR GET PARKING SITE ONLY

    BASIC GET REQUEST :

        BASE = 'http://127.0.0.1:5000/'
        response = requests.get(BASE + "parking/Prospect_Ratushnyaka")
        print(response.json())

    BASIC PUT REQUSET :

        BASE = 'http://127.0.0.1:5000/'
        response = request.put(BASE + parking/Prospect_Ratushnyaka)
        print(response.json())
    """
    @marshal_with(site_resource_field)
    def get(self, address):

        # Find specified parking
        site = Sites.query.filter_by(address=address).first()

        # Check if parking with specified address exists
        if not site:
            abort(404, message=f"Could not find parking site with this address - {address}")

        return {'site_id': site.id, 'address': site.address}, 200

    @marshal_with(site_resource_field)
    def post(self, address):

        # Check if site with specified address exists
        if Sites.query.filter_by(address=address).first():
            abort(400, message=f"Site with this address - {address} already exists")
        else:
            # Create new site
            site = Sites(address=address)
            db.session.add(site)
            db.session.commit()

            # Return instance and 200 code
            return site, 200

api.add_resource(ParkingSite, "/parking/<string:address>")


if __name__ == '__main__':
    """
    DO NOT USE "debug = True" on production deployment
    """
    app.run(debug=False)