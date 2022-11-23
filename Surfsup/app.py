import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

last_twelve_months = '2016-08-23'

@app.route("/")
def welcome():
    return (
        f"<p>Welcome to the Climate weather API!</p>"
        f"<p>Usage:</p>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"   
            )

@app.route("/api/v1.0/precipitation")
def precipitation():
     p_results = dict(session.query(Measurement.date, func.avg(Measurement.prcp)).\
    filter(Measurement.date >= last_twelve_months).group_by(Measurement.date).all())

    return jsonify(p_results)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = dt.date(2017, 8 ,23)
    year_ago = last_date - dt.timedelta(days=365)
    
     most_pop_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()

    pop_station_tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.station=='USC00519281').all()

    lists = pd.DataFrame(pop_station_tobs).rename(columns={0:'temperature'}).temperature.tolist()

    return jsonify(lists)

@app.route("/api/v1.0/<start>")
# route example: /api/v1.0/2017-01-01


@app.route('/api/v1.0/<start>') 
def start(start):
    # route example: /api/v1.0/2017-01-01

    start = Measurement.date <= '2010-01-01'
    end = Measurement.date >= '2017-08-23'
    start = Measurement.date <= '2010-01-01'
    end = Measurement.date >= '2017-08-23'

    tobs_only = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
            
    tobs_df = pd.DataFrame(tobs_only).rename(columns = {0:'tobs'})
    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()

    df = [tavg,tmax,tmin]
    label = ['tavg','tmax','tmin']

    dictionary = zip(label,df)
    final_df = dict(dictionary)
    
    return jsonify(final_df)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    start = dt.date(2010, 1 ,1)
    end = dt.date(2017, 8 ,23)
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(multi_day_temp_results)


if __name__ == '__main__':
    app.run(debug=True)