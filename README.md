# WeatherReport

## Overview

Ingest some weather and crop yield data (provided), design a database schema for it, and expose the data through a REST API.

## Weather Data Description

The data directory has files containing weather data records from 1985-01-01 to 2014-12-31. Each file corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio.

Each line in the file contains 4 records separated by tabs:

1. The date (YYYYMMDD format)
2. The maximum temperature for that day (in tenths of a degree Celsius)
3. The minimum temperature for that day (in tenths of a degree Celsius)
4. The amount of precipitation for that day (in tenths of a millimeter)

Missing values are indicated by the value -9999.

## Data Modeling

Used PostgreSQL to design data model to represent the weather data records.

## Ingestion

Ingest the weather data from the raw text files supplied into the database, using the designed model.
Check for duplicates: if the code is run twice, it should not end up with multiple rows with the same data in your database.
The code should also produce log output indicating start and end times and number of records ingested.

## Data Analysis

For every year, for every weather station, calculate:

- Average maximum temperature (in degrees Celsius)
- Average minimum temperature (in degrees Celsius)
- Total accumulated precipitation (in centimeters)

Ignored missing data when calculating these statistics.

Design a new data model to store the results. Use NULL for statistics that cannot be calculated.

Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.

## REST API

Choose a web framework (e.g. Flask, Django REST Framework). Create a REST API with the following GET endpoints:

/api/weather
/api/weather/stats

Both endpoints should return a JSON-formatted response with a representation of the ingested/calculated data in your database. Allow clients to filter the response by date and station ID (where present) using the query string. Data should be paginated.

Include a Swagger/OpenAPI endpoint that provides automatic documentation of your API.

Include all files necessary to run the API locally, along with any unit tests.
