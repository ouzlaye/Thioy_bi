from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
engine = create_engine("sqlite:///citizen.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///citizen.db'  
db = SQLAlchemy(app)

#create model
Base = declarative_base()
class Citizen( db.Model):
    __tablename__ = 'citizen' 
    id = db.Column(Integer, primary_key=True)
    prenom = db.Column(String(20))
    nom = db.Column(String(20)) 
    cni = db.Column(String(50))
    
#db.create_all()
#print('okffffff')
#Base.metadata.create_all(engine)
#print ("Table citizen crée ...")
Session = sessionmaker(bind= engine)

# definition des endpoints 
@app.route("/api/citizen", methods=["POST"])
def create():
    try:
        #session = Session()
        new_citizen = Citizen(
            prenom = request.json['prenom'],
            nom = request.json['nom'],
            cni = request.json['cni'])
        db.session.add(new_citizen)
        db.session.commit()
        return new_citizen.cni
    except Exception as e:
        print(f" erreur '{e}' ")
        return {"error": "erreur lors de la creation du citoyen."}, 500
    

@app.route("/api/citizen", methods=['GET'])
def get():
    try:
        session = Session()
        citizen = db.session.query(Citizen).all()
        if citizen:
            result =[]
            for c in citizen:
                result.append({"id": c.id, "name": c.prenom, "nom":c.nom, "cni":c.cni})
            return jsonify(result)
        else:
            return jsonify({"error": f"Citizen non trouvé"}), 404    
    except Exception as e:
        print(f"erreur '{e}'")
        return {"une erreur est survenue"}, 500
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    

