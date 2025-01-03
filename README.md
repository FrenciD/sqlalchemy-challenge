# part 1: Analyze and Explore the Climate Date
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, use SQLAlchemy ORM queries, Pandas, and Matplotlib.
Use the SQLAlchemy create_engine() function to connect to your SQLite database.
Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
Link Python to the database by creating a SQLAlchemy session.
Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

# Precipitation Analysis
Find the most recent date in the dataset.
Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
Select only the "date" and "prcp" values.
Load the query results into a Pandas DataFrame. Explicitly set the column names.
Sort the DataFrame values by "date".
Plot the results by using the DataFrame plot method

# Part 2: Design Climate App
/
Start at the homepage.
List all the available routes.
/api/v1.0/precipitation
Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.
/api/v1.0/stations
Return a JSON list of stations from the dataset.
/api/v1.0/tobs
Query the dates and temperature observations of the most-active station for the previous year of data.
Return a JSON list of temperature observations for the previous year.
/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
