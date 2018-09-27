from datetime import datetime as dt
import numpy as np
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind=engine)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    results_dic = {date: prcp for date, prcp in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()

    results_dic = {station: name for station, name in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23').all()

    results_dic = {date: tobs for date, tobs in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    results_dic = list(np.ravel(results))

    return jsonify(results_dic)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start, Measurement.date <= end).all()

    results_dic = list(np.ravel(results))
    
    return jsonify(results_dic)

if __name__ == "__main__":
    app.run(debug=True)

#