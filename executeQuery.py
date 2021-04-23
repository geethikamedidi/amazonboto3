import time

import boto3


def query_session():
    ath = boto3.client('athena')

    params = {
        'region': 'us-west-2',
        'database': 'foodb',
        'bucket': 'clis3',
        'path': 'clis3/output/',
        'query': 'SELECT * FROM user_parquet limit 10;'
    }

    response_query_execution_id = ath.start_query_execution(QueryString=params['query'],
                                                            QueryExecutionContext={'Database': params['database']},
                                                            ResultConfiguration={
                                                                'OutputLocation': 's3://' + params['bucket'] + '/' +
                                                                                  params[
                                                                                      'path']})
    query_execution_details = ath.get_query_execution(QueryExecutionId=response_query_execution_id['QueryExecutionId'])
    print(query_execution_details)

    status = "RUNNING"
    maxIterations = 5
    while maxIterations > 0:
        maxIterations = maxIterations - 1
        query_execution_details = ath.get_query_execution(QueryExecutionId=response_query_execution_id['QueryExecutionId'])
        status = query_execution_details['QueryExecution']['Status']['State']
        print(status)
        if (status == 'FAILED') | (status == 'CANCELLED'):
            return False
        elif status == 'SUCCEEDED':
            location = query_execution_details['QueryExecution']['ResultConfiguration']['OutputLocation']
            print("location: "+location)
            response_query_result = ath.get_query_results(QueryExecutionId=response_query_execution_id['QueryExecutionId'])
            resultSet = response_query_result['ResultSet']
            print(resultSet)
            return True
        else:
            time.sleep(1)


print(query_session())