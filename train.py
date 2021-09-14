import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn import datasets

mlflow.set_experiment('my_classification_model')

iris = datasets.load_iris()
x = iris.data[:, 2:]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=7)

with mlflow.start_run(run_name='My model experiment') as run:
    
	# add parameters for tuning
	num_estimators = 100
	mlflow.log_param('num_estimators', num_estimators)

	# train the model
	rf = RandomForestRegressor(n_estimators=num_estimators)
	rf.fit(X_train, y_train)
	predictions = rf.predict(X_test)

	mlflow.sklearn.log_model(rf, 'random-forest-model')

	# log model performance 
	mse = mean_squared_error(y_test, predictions)
	mlflow.log_metric('mse', mse)
	print('mse: %f' % mse)

	run_id = run.info.run_uuid
	experiment_id = run.info.experiment_id
	mlflow.end_run()
	print(f'artifact_uri = {mlflow.get_artifact_uri()}')
	print(f'runID: {run_id}')