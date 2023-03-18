# MLFlow_example

A repo containing a notebooks used for experiment tracking with MLFlow.

## Configure A Remote Tracking Server On AWS

* Note: You can use a **remote tracking server** (e.g EC2 instance) or a **local tracking server**.

The guide can be found [here](https://github.com/chineidu/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md)

Postgres DB Config:

- db_instance_identifier: enter the value
- db_username: enter the value
- db_password: enter the value
- initial_db_name: enter the value
- db_endpoint: enter the db endpoint

S3 Bucket:

- bucket-name
  
### Install the requirements (on the remote server using ssh)

```console
pip3 install mlflow boto3 psycopg2-binary
```
  
Run the server:

```console
mlflow server -h 0.0.0.0 -p 5000 \
--backend-store-uri postgresql://$DB_USER:$DB_PASSWORD@$DB_ENDPOINT:5432/$DB_NAME \
--default-artifact-root s3://$S3_BUCKET_NAME
```

### Save The Environment Variables

```console
export DB_USER="" \ 
export DB_PASSWORD="" \
export DB_ENDPOINT="" \
export DB_NAME="" \
export S3_BUCKET_NAME=""
```
