CREATE EXTERNAL TABLE IF NOT EXISTS foodb.user_parquet (
  id int,
  first_name string,
  last_name string,
  email string,
  gender string
)
STORED AS PARQUET
LOCATION 's3://bucketforathena1/parquet/userdata1.parquet/';