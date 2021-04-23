import boto3

ath = boto3.client('athena')

with open('user_parquet.ddl') as ddl:
    ath.start_query_execution(
        QueryString=ddl.read(),
        ResultConfiguration={'OutputLocation': 's3://clis3/queries/'})
