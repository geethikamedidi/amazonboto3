import boto3

athena = boto3.client('athena')

athena.start_query_execution(QueryString='create database parquetdb2',
                             ResultConfiguration={'OutputLocation': 's3://clis3/'})
