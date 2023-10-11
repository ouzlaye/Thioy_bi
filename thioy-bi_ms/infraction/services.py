from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#engine = create_engine("sqlite:///infraction.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///infraction.db'  
db = SQLAlchemy(app)


#create model

class Infraction( db.Model):
    __tablename__ = 'infraction' 
    id = db.Column(Integer, primary_key=True)
    types = db.Column(String(100))
    code = db.Column(Integer)
    
#db.create_all()
print ("Table infraction cree ...")


# definition des endpoints 
@app.route("/api/infraction", methods=["POST"])
def create():
    
    try:
        
        new_infraction = Infraction(
            types = request.json['types'],
            code = request.json['code'])
            
        db.session.add(new_infraction)
        db.session.commit()
        return 'ok'
    except Exception as e:
        print(f" erreur '{e}' ")
        return {"error": "erreur ."}, 500
    

@app.route("/api/infraction", methods=['GET'])
def get():
    try:
        
        infraction = db.session.query(Infraction).all()
        if infraction:
            result =[]
            for inf in infraction:
                result.append({"id": inf.id, "types": inf.types, "code":inf.code})
            return jsonify(result)
        else:
            return jsonify({"error": f"infraction non trouvé"}), 404    
    except Exception as e:
        print(f"erreur '{e}'")
        return {"une erreur est survenue"}, 500
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)
    

