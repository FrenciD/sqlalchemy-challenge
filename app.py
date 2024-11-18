# Import the dependencies.

import pandas as pd
import datetime as dt
import numpy as np
from sqlalchemy.orm import session 
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save references to each table


# Create our session (link) from Python to the DB
session = session(engine)

#################################################
# Flask Setup

#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation data for the last year<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the last year<br/>"
        f"/api/v1.0/<start> - Temperature stats from a start date<br/>"
        f"/api/v1.0/<start>/<end> - Temperature stats for a date range<br/>"
    )
# Route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the last data point
    last_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query precipitation data for the last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

# Route for weather stations
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    station_data = session.query(Station.station, Station.name).all()

    # Convert query results to a list of dictionaries
    stations_list = [{"station": station, "name": name} for station, name in station_data]

    return jsonify(stations_list)

# Route for temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Calculate the date one year ago from the last data point
    last_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query temperature observations for the most active station in the last year
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert query results to a list of dictionaries
    temperature_list = [{"date": date, "temperature": tobs} for date, tobs in temperature_data]

    return jsonify(temperature_list)

# Route for temperature stats with a start date
@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # Query temperature stats (min, max, avg) from a start date
    stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()

    # Convert query results to a dictionary
    stats_dict = {
        "start_date": start,
        "min_temp": stats[0][0],
        "avg_temp": stats[0][1],
        "max_temp": stats[0][2]
    }

    return jsonify(stats_dict)

# Route for temperature stats with a start and end date
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    # Query temperature stats (min, max, avg) for a date range
    stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert query results to a dictionary
    stats_dict = {
        "start_date": start,
        "end_date": end,
        "min_temp": stats[0][0],
        "avg_temp": stats[0][1],
        "max_temp": stats[0][2]
    }

    return jsonify(stats_dict)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)