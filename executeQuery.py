import time

import boto3


def query_session():
    ath = boto3.client('athena')

    params = {
        'region': 'us-west-2',
        'database': 'parquetdb2',
        'bucket': 'clis3',
        'path': 'output/',
        'query': 'SELECT * FROM user_parquet limit 10;'
    }

    response_query_execution_id = ath.start_query_execution(QueryString=params['query'],
                                                            QueryExecutionContext={'Database': params['database']},
                                                            ResultConfiguration={
                                                                'OutputLocation': 's3://' + params['bucket'] + '/' +
                                                                                  params[
                                                                                      'path']})
    query_execution_details = ath.get_query_execution(QueryExecutionId=response_query_execution_id['QueryExecutionId'])
    print("query_execution_details: " + str(query_execution_details))

    status = "RUNNING"
    maxIterations = 10
    while maxIterations > 0:
        maxIterations = maxIterations - 1
        query_execution_details = ath.get_query_execution(
            QueryExecutionId=response_query_execution_id['QueryExecutionId'])
        status = query_execution_details['QueryExecution']['Status']['State']
        print("Status of the query execution: " + status)
        if (status == 'FAILED') | (status == 'CANCELLED'):
            return False
        elif status == 'SUCCEEDED':
            location = query_execution_details['QueryExecution']['ResultConfiguration']['OutputLocation']
            print("location of the result of the query execution: " + location)
            response_query_result = ath.get_query_results(
                QueryExecutionId=response_query_execution_id['QueryExecutionId'])
            resultSet = response_query_result['ResultSet']
            print("ResultSet----------" + str(resultSet))
            return True
        else:
            time.sleep(1)


query_session()
