-- Databricks notebook source
CREATE DATABASE f1_raw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Create circuit table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.circuits;
CREATE TABLE f1_raw.circuits(circuitId INT,
circuitRef STRING,
name STRING,
location STRING,
country STRING,
lat DOUBLE,
lng DOUBLE,
alt INT,
utl STRING)
USING CSV
OPTIONS (path "/mnt/formula1dlmorales/raw/circuits.csv", header true)

-- COMMAND ----------

SELECT * FROM f1_raw.circuits

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.races;
CREATE TABLE f1_raw.races(raceId INT,
year INT,
round INT,
circuitId INT,
name STRING,
date DATE,
time STRING,
url STRING)
USING CSV
OPTIONS (path "/mnt/formula1dlmorales/raw/races.csv", header true)

-- COMMAND ----------

SELECT * FROM f1_raw.races

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create tables for JSON files

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###### Create table for constructors

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.constructors;
CREATE TABLE f1_raw.constructors(constructorId INT,
constructorRef STRING,
name STRING,
nationality STRING,
url STRING)
USING JSON
OPTIONS (path "/mnt/formula1dlmorales/raw/constructors.json")

-- COMMAND ----------

SELECT * FROM f1_raw.constructors

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###### Create table for drivers

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.drivers;
CREATE TABLE f1_raw.drivers(driverId INT,
driverRef STRING,
number INT,
code STRING,
name STRUCT<forename: STRING, surname: STRING>,
dob DATE,
nationality STRING,
url STRING)
USING JSON
OPTIONS (path "/mnt/formula1dlmorales/raw/drivers.json")

-- COMMAND ----------

SELECT * FROM f1_raw.drivers

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###### Create table for results

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.results;
CREATE TABLE f1_raw.results(raceId INT,
driverId INT,
costructorId INT,
number INT,
grid INT,
position INT,
positionText STRING,
poistionOrder INT,
points INT,
laps INT,
time STRING,
milliseconds LONG,
fastestLap INT,
fastestLapTime STRING,
fastestLapSpeed DECIMAL,
statusId INT)
USING JSON
OPTIONS (path "/mnt/formula1dlmorales/raw/results.json")

-- COMMAND ----------

SELECT COUNT(*) FROM f1_raw.results

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###### Create table for pit stops

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.pit_stops;
CREATE TABLE f1_raw.pit_stops(raceId INT,
driverId INT,
stop INT,
lap INT,
time STRING,
duration STRING,
milliseconds INT)
USING JSON
OPTIONS (path "/mnt/formula1dlmorales/raw/pit_stops.json", multiLine true)

-- COMMAND ----------

SELECT * FROM f1_raw.pit_stops

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.laptimes;
CREATE TABLE f1_raw.laptimes(raceId INT,
driverId INT,
lap INT,
position INT,
time STRING,
milliseconds INT)
USING CSV
OPTIONS (path "/mnt/formula1dlmorales/raw/lap_times", header true)

-- COMMAND ----------

SELECT * FROM f1_raw.laptimes

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.qualifying;
CREATE TABLE f1_raw.qualifying(qualifyId INT,
raceId INT,
driverId INT,
constructorId INT,
number INT,
position INT,
q1 STRING,
q2 STRING,
q3 STRING)
USING JSON
OPTIONS (path "/mnt/formula1dlmorales/raw/qualifying", multiLine true)

-- COMMAND ----------

SELECT * FROM f1_raw.qualifying

-- COMMAND ----------

DESC EXTENDED f1_raw.qualifying

-- COMMAND ----------

