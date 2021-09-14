import mlflow.sagemaker as mfs

experiment_id = '1'
run_id = '52aafa205df548daa790bfdea355f79a'
region = 'us-east-2'
aws_id = '047810789005'
arn = 'arn:aws:iam::047810789005:role/aws-sagemaker-for-deploy-ml-model'
app_name = 'model-application'
model_uri = f'mlruns/{experiment_id}/{run_id}/artifacts/random-forest-model'
tag_id = '1.18.0'


image_url = aws_id + '.dkr.ecr.' + region + '.amazonaws.com/mlflow-pyfunc:' + tag_id


mfs.deploy(app_name,
	model_uri=model_uri,
	region_name=region,
	mode='create',
	execution_role_arn=arn,
	image_url=image_url)