import boto3

athena = boto3.client('athena')

athena.start_query_execution(QueryString='create database foodb',
                             ResultConfiguration={'OutputLocation': 's3://clis3/'})
