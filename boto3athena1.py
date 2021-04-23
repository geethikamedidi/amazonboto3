import boto3                                    # python library to interface with S3 and athena.
s3 = boto3.resource('s3')                       # Passing resource as s3
client = boto3.client('athena')                 # and client as athena
database = 'clidb'                      # Data base name
query=""" create external table clidb.table1 (
'x' Int,
'y' string)
Location "s3://clis3/";
"""
s3_output = 's3://clis3/output_folder/'  # output location
response = client.start_query_execution(QueryString=query, QueryExecutionContext={'Database': database}, ResultConfiguration={'OutputLocation': s3_output})