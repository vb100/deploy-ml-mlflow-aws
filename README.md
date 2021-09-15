<h1>Deploying Models to Production with MLflow and Amazon Sagemaker</h1>

<p>This repo introduces how to prepare you Machine Learning (ML) model for production in AWS Sagemaker with the help of MLflow and AWS Command Line Inteface (AWS CLI). Before start, we should know what is what:
  <ul>
    <li><b>Mlflow</b> - an open source platform for the ML lifecycle.</li>
    <li><b>AWS CLI</b> - is an unified tool to manage your Amazon Web Services (AWS) services.</li>
  </ul>
With this repo you can follow the provided steps on your local machine and AWS account. All steps will be explained clearly with screens and real example.
</p>

<h2>Setup the environment</h2>
<p>For this tutorial you will need:
  <ul>
    <li>AWS Account.</li>
    <li>Docker installed on your local machine.</li>
    <li>Python <b>3.6</b> (or higher) with <code>mlflow>=1.0.0</code> installed.</li>
    <li>Anaconda software to create conda virtual environment.</li>
  </ul>
 Next, I will demonstrate how to install <i>mlflow</i> to your dedicated virtual environment. For this I will use Mac OS, but you can do the same steps on both Windows and Mac OS.
 
 <p><h3>Step 1. Prepare you Python Virtual environment</h3>
 With this step we will create dedicated virtual environment to perform the whole example in this repo. Do the following steps.
 <ul>
  <li>Create a new conda virtual environment in you working directory with the following command in your terminal:<br><code>conda create --name deploy_ml python=3.6</code><br>With this command you will create a new conda based virtual environment on your local machine.</li>
  <li>Once your virtual environment is sucessfully create, you can easily to activate it with the following command:<br><code>conda activate deploy_ml</code><br>At this moment we are having an almost empty virtual environment which is ready to be filled with new dependencies.</li>
 </ul>
 </p>
 
 <p><h3>Step 2. Install dependencies in you virtual environment</h3></p>
<ul>
  <li>Install <i>mlflow</i> package into our virtual environment with the following command:<br><code>pip install -q mlflow==1.18.0</code>.<br>At the moment of preparing this repo, the version of <i>mlfflow</i> is <code>mlflow==1.18.0</code>.</li>
  <li>To run properly the ML model itself we have to install following modules and packages to our virtual environment as well:
  <ul>
    <li>Pandas: <code>pip install pandas</code>.</li>
    <li>Scikit-learn: <code>pip install -U scikit-learn</code>.</li>
    <li>AWS Command Line Interface (<i>AWS CLI</i>): <code>pip install awscli --upgrade --user</code>.</li>
    <li>Boto3: <code>pip install boto3</code>.</li>
    </ul>
  </li>
</ul>
</p>

<p><h3>Step 3. Setup AWS IAM User and AWS CLI configuration</h3></p>
<ul>
  <li><b>Create a new AWS AIM User</b></li>
  <ul>
    <li>Open <b><i>Identity and Access management (IAM) dashboard</i></b>.</ll>
  <li>Click on <b><i>Users</i></b>.</li>
  <li>Click <b>Add users</b> on the right side of the screenshot.</li>
  <li>Set the <i>User name</i> and mark <i>Programmatic access</i> tick below.</li>
  <li>Click on <i><b>Create group</b></i> as the part of <i>Add user to group</i> option.</li>
  <li>Type a group name you want to assign to your IAM User.</li>
  <li>From the list below select following policies:
    <ul>
      <li><i><b>AmazonSageMakerFullAccess</b></i>.</li>
      <li><i><b>AmazonEC2ContainerRegistryFullAccess</b></i>.</li>
      <li><i><b>...</b></i>.</li>
    </ul>
  </li>
  <li>Click on <b><i>Create group</i></b>, then the current <i>Policies</i> window will be closed.</li>
  <li>Click on <b><i>Next: Tags</i></b>.</li>
  <li>Click on <b><i>Next: Review</i></b>.</li>
  <li>Click on <b><i>Create user</i></b>.</li>
  <li>You will get a notification about sucessfully created new User on AWS IAM, see the screenshot below.
  <img src="images/Screenshot 2021-09-02 at 17.01.04.png" alt="New IAM User", width=585><br>
    <p><b>Important</b>. Keep safe you credentials on your own notes. This step is only one occasion you see <i>AWS Secret Access Key</i>. Rewrite it carefully.</p>
  </li>
  
  </ul></ul>
  <ul>
  <li><b>Setup AWS CLI configuration</b></li>
  <ul>
    <li>Be sure you have installed <i>AWS CLI</i> and type command in your terminal: <code>aws configure</code>.</li>
    <li>Then you will have to enter your own credentials as follows:
      <ul>
        <li><i><b>AWS Access Key ID</b></i>: go to <i>IAM</i>, then <i>Users</i>, and click on your user just created. Select <i>Security credentials</i> tab and copy the value of <i>AWS Access Key ID</i></li>
        <li><i><b>AWS Secret Access Key</b></i>: paste this code from your own notes. You have seen this code originally from <i>Security credentials</i> of your user.</li>
        <li><i><b>Default region name</b></i>: go to main AWS interface, click on your region, and check which region is activated for you (<i>us-east-1</i>, <i>eu-west-1</i>, and so on).</li>
        <li><i><b>Default output format</b></i>: set it as <i>json</i>.</li>
      </ul>
    <li>The filled AWS CLI configurations should looks like in the screenshot below.<br>
      <img src="images/Screenshot 2021-09-02 at 23.50.22.png" alt="AWS CLI Configuration credentials", width=475><br>
    </li>
    </li>
  </ul>
  </ul>
</ul>

<p><h3>Step 4. Test if <i>mlflow</i> is working good</h3>
<ul>
<li>Before doing all following steps, we must be sure if our freshly installed <i>mlflow</i> service if working good on our local machine. To do it, type the following command in the terminal: <code>mlflow ui</code>.</li>
  <li>Open the <i>mlflow</i> dashboard on you browser by entering following URL to your <i>localhost</i>: <code>http://127.0.0.1:5000</code><br>Please keep in mind that this service uses port <code>5000</code> on your machine (open the second terminal window on the same working directory before run this command).<br>You should see <i>mlflow</i> dashboard interface it is shown in the screenshot below:<br>
  <img src="images/Screenshot 2021-08-28 at 17.02.00.png" alt="MLflow Dashboard Interface", width=585><br>
    If you see the same on your browser too, <i>mlflow</i> works fine and we are ready to go to the next steps.
  </li>
</ul>
</p>

<h2>Prepare you Machine Learning model for <i>mlflow</i></h2>
<p><h3>Step 1. Adapt your ML training code for <i>mlflow</i></h3>
Usually we work with plain Python code in our local machine to train, debug and improve our ML models. In order to make out ML code be understandable for <i>mlflow</i> we must do quick changes in model training codes, described in the following steps.
<ul>
  <li>Copy and paste the full code from <i>train.py</i> (available in this repo).</li>
  <li>Adapt the Python code inside to track some model metrics in <i>mlfflow</i> with following changes in code:</li>
  
```` py
import mlflow
import mlflow.sklearn
````
  
```` py
mlflow.set_experiment("my_classification_model")
````
  
```` py
with mlflow.start_run(run_name="My model experiment") as run:
    mlflow.log_param("num_estimators", num_estimators)
````
  
```` py
    mlflow.sklearn.log_model(rf, "random-forest-model")
````
  
```` py
    # Log model metrics (mse - mean squared error)
    mlflow.log_metric("mse", mse)
````
  
```` py
    # close mlflow connection
    run_id = run.info.run_uuid
    experiment_id = run.info.experiment_id
    mlflow.end_run()
    print(mlflow.get_artifact_uri())
    print("runID: %s" % run_id)
````

  With the code changes above, we are ready to track <code>mse</code> (</i>Mean Squared Error</i>) metric for the model and generate some run artifacts in <i>mlflow</i> dashboard.
</ul>
</p>

<p><h3>Step 2. Run the model and track metrics in <i>mlflow</i></h3>
Once we finished the latest step in this tutorial, <i>mlflow</i> is able to track desired metrics (in our example, <code>mse</code>) in <i>mlflow</i> dashboard. To do it properly, do the following:
<ul>
  <li>Open another terminal windown (be sure the first one with activated <i>mlflow</i> service in port <code>:5000</code> is still running).</li>
  <li>Activate the same virtual environment on the second terminal window as we have created in <b>Step no. 1</b> with the following command: <code>conda activate deploy_ml</code></li>
  <li>Navigate your terminal to the project environment with <code>cd</code> (<i>change directory</i>) terminal command.</li>
  <li>From the second terminal window, simply run the model training code <i>train.py</i> with the command in your terminal: <code>python train.py</code>.</li>
  <li>Once the train script executed sucessfully, you will be notificated about creation of new experiment in <i>mlflow</i>, calculated <i>MSE</i>, absolute directory path to model artifacts, and <code>runID</code>, see the screenshot below.<br>
  <img src="images/Screenshot 2021-09-03 at 00.40.38.png" alt="Model trained sucessfully", width=645><br>
  </li>
  <li>Open the browser window again where <i>mlflow</i> service is running on. <b>Refresh the browser window</b>. Then, on the left menu <i>Experiments</i> you will see updated list of experiments ran so far, which includes that one you ran recently in this step (<code>my_classification_model</code>), see the screenshot below.<br>
    <img src="images/Screenshot 2021-08-29 at 00.31.35.png" alt="Mlflow UI with new experiment", width=505><br>
  </li>
  <li>Click on the new experiment, and freely navigate through available options to check metric values and other parameters from the experiment.</li>
  <li>Once you entered to your new experiment space, click on the most recent run tagged with <i>Random Forest Experiment</i> Run time tag. Be sure, that on the <i>Artifacts</i> section you are seeing this kind of structured experiment files with filled content for each file. See screenshot below.<br>
  <img src="images/Screenshot 2021-09-03 at 00.46.45.png" alt="Generated model artifacts in Mlflow UI", width=575><br>
Among the artifact files, there is a <i>conda.yaml</i> file. This is the environment your model needs to run, and it can be heavily customized based on your needs. 
  </li>
  <li>Also, check the file structure in you <i>Finder</i> (Mac OS), or in <i>Windows explorer</i> (Windows OS). You should see new folder <i><b>mlruns</b></i> created in your project directory with run numbers folder(<i>0</i>, <i>1</i>, and so on), <code>runID</code> folder, and full set of artifacts inside. See the screenshot below.<br>
  <img src="images/Screenshot 2021-09-03 at 00.49.48.png" alt="Generated model artifacts in Finder", width=765><br>
  </li>
</ul>
When we are sure that our model can be sucessfully tracked with local <i>mlflow</i> user interface on your local machine, we can go forward to bring our model to the clouds.
</p>

<h2>Deploy the model to AWS</h2>
<p><h3>Step 1. Build a Docker Image and push it to AWS ECR</h3>
<ul>
  <li>On the second terminal windows, got to the <i>artifact</i> directory of selected model run in <i>mlruns</i> folder (in my example I set this directory as: <i>/mlruns/1/ccc73fe5e7784df69b8518e3b9daa0c6/artifacts/random-forest-model</i>), then type and run a command:<br><code>mlflow sagemaker build-and-push-container</code>.<br>You will see all processes running in real time in your terminal, as shown in a screenshot below.<br>
    <img src="images/Screenshot 2021-09-03 at 01.05.35.png" alt="Creating Container Image in Terminal", width=625><br>
    The finished processes on building and pushing Docker container images looks as it is in a screenshot below:<br>
    <img src="images/Screenshot 2021-09-03 at 01.08.48.png" alt="Finished to Create Container Image", width=625><br>
    If you have set up AWS correctly with the proper permissions, this will build an image locally and push it to your image (name is <i>mlflow-pyfunc</i>) registry on AWS.
  </li>
  <li>Once you finished the previous action without any issues, you should check local <b>Docker Desktop</b> to be sure that everything is well at this moment. Open your Docker Desktop application and go to <i>Images</i> section. You should see two images created. The first one indicates your <i><b>AWS ECR</b></i> container image, and the other one is <code>mlflow-pyfunc</code>. See the screenshot below.<br>
  <img src="images/Screenshot 2021-09-03 at 01.11.01.png" alt="Docker Images in Docker Dekstop", width=625><br>
  </li>
  <li>Check <b>AWS ECR</b> repos list. You should see the same image name as it was listed first in Docker Desktop application. See the screenshot below.<br>
  <img src="images/Screenshot 2021-09-03 at 01.12.20.png" alt="Docker Images in AWS ECR", width=625><br>
  </li>
  <li>Check image parameters in <b>AWS ECR</b> by clicking on <code>mlflow-pyfunc</code> image repository. On a image properties window you will see the main parameters of your image such as <i>Image URI</i>, <i>Size</i>, and other ones, see the screenshot below.<br>
  <img src="images/Screenshot 2021-09-03 at 01.13.01.png" alt="Docker Image Details in AWS ECR", width=625><br>
    If you see the same set of image parameters with meaningful values, move forward with next steps.
  </li>
</ul>
</p>

<p><h3>Step 2. Deploy image to Sagemaker</h3>
Now all what we have to do is provide <i>mlflow</i> our image URL and desired model and then we can deploy these models to SageMaker.
<p>
  <b>Important:</b> Before doing all following steps, you should create a special CLI token between your terminal and AWS. For this <code>boto3</code> package is responsible, and you can do it in very simple way, just by setting your environment variables in your terminal like following:
  <ul>
    <li>Type <code>AWS_ACCESS_KEY=XXXXXXXXX</code>, where <code>XXXXXXXXX</code> is your <i>AWS Access Key</i> for your <i>User</i> in AWS.</li>
    <li>Type <code>AWS_SECRET_ACCESS_KEY=XXXXXXXXX</code>, where <code>XXXXXXXXX</code> is your <i>AWS Secret Access Key</i> for your <i>User</i> in AWS.</li>
</ul>
Ocje you set your virtual environment, the terminal with active CLI is able to communicate with AWS services and make required operations.
</p>

<ul>
  <li>Create a new Python script in your root project directory by terminal command <code>touch deploy.py</code>. This command will create a new file <i>deploy.py</i>.</li>
  <li>Write the following script logic in the <i>deploy.py</i> you have just created:
  
```` py
import mlflow.sagemaker as mfs

experiment_id = '1'
run_id = 'XXXXXXXXXXXXXX'
region = 'us-east-2'
aws_id = 'XXXXXXXXXXXXXX'
arn = 'arn:aws:iam::XXXXXXXXXXXXXX:role/sagemaker-full-access-role'
app_name = 'model-application'
model_uri = 'mlruns/%s/%s/artifacts/random-forest-model' % (experiment_id, run_id)
tag_id = '1.18.0'

image_url = aws_id + '.dkr.ecr.' + region + '.amazonaws.com/mlflow-pyfunc:' + tag_id

mfs.deploy(app_name=app_name, 
           model_uri=model_uri, 
           region_name=region, 
           mode="create",
           execution_role_arn=arn,
           image_url=image_url)
````
    
As you can see from the <i>deploy.py</i> skeleton code, we will need to get <code>run_id</code>, <code>region</code>, <code>aws_id</code>, ARN for <i>AmazonSageMakerFullAccess</i> (<code>arn</code>), <code>model_uri</code>, and <i>image_url</i>. Let's extract these values one by one.
    
  </li>
  <ul>
    <li><code>experiment_id</code><br>
      <ul>
        <li>Open the <i>Mlflow</i> user interface in <i>http://127.0.0.1:5000</i>.</li>
        <li>Click on your experiment (for example <b><i>my_classification_model</i></b>).</li>
        <li>You will see an <i>Experiment ID</i> in the upper side of the screen next to Experiment ID text. Copy the value (in my case it is <code>1</code>).</li>
      </ul>
    </li>
    <li><code>run_id</code>:<br>
      <ul>
        <li>Open the <i>Mlflow</i> user interface in <i>http://127.0.0.1:5000</i>.</li>
        <li>Click on your experiment (for example <b><i>my_classification_model</i></b>).</li>
        <li>Click on run which has an image to an AWS ECR.</li>
        <li>On <i><b>Artifacts</b></i> section expand the list of artifacts by clicking on an arrow, and select <i><b>MLModel</b></i>.</li>
        <li>On the data window on the right, you can see main data about the model. One of these is <code>run_id</code>. Copy it.</li>
      </ul>  
      </li>
    <li><code>aws_id</code>:<br>Get your AWS ID from the terminal by running this command: <code>aws sts get-caller-identity --query Account --output text</code>.</li>
    <li><code>arn</code>:<br>Create the Role for the <i>SageMakerFullAccess</i> and grab it's <i>ARN</i>.
  <ul>
    <li>Open <b>IAM</b> Dashboard.</li>
      <li>Click on <b><i>Create role</i></b>.</li>
      <li>Select <b>SageMaker</b> service from the given list and click <b><i>Next: Permissions</i></b>.</li>
      <li>Click <b><i>Next: Tags</i></b>.</li>
      <li>Once you completed to create this role, copy Role ARN for further usage (<i>Role ARN</i>).</li>
  </ul>
  <li><code>region</code>:<br>Go to main AWS interface, click on your region, and check which region is activated for you (<i>us-east-1</i>, <i>eu-west-1</i>, and so on).</li>
    <li><code>app_name</code>:<br>Set any name you want to recognize your application.</li>
    <li><code>tag_id</code><br>This the version of <i>mlflow</i>. Open <b><i>AWS ECR</i></b>, then open your repository, and copy the value of <i>Image tag</i>.</li>
  </li>
  </ul><br>
  <li>Open again terminal with activated virtual environment <i>deploy_ml</i> and enter run the <i>deploy.py</i> Python script with the command: <code>python deploy.py</code>.<br>The output should be notify you about sucessfuly complete deploying the image to <i>SageMaker</i>, see the screen below.<br>
<img src="images/Screenshot 2021-09-06 at 01.24.01.png" alt="Sucessfully deployed model to SageMaker", width=675><br>
  <p>You should see the <i>inService</i> message in you terminal resuting into sucessfully deployed model to <i>SageMaker</i>.</p>
</li>
</ul>
</p>

<h2>Use the model with the new data</h2>
<p>Once you are sure that your model is running in AWS, you can make a new prediction for a new given data with the help of <code>boto3</code> library. Follow the following steps to do it.
  <ul>
    <li>Open the terminal with activated virtual environment <i>deploy_ml</i>.</li>
    <li>Create a new file <i>predict.py</i> with command <code>touch predict.py</code>.</li>
    <li>For <i>predict.py</i> use this Python code:<br>

```` py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
import json
import boto3

global app_name
global region
app_name = 'model-application'
region = 'us-east-2'

def check_status(app_name):
    sage_client = boto3.client('sagemaker', region_name=region)
    endpoint_description = sage_client.describe_endpoint(EndpointName=app_name)
    endpoint_status = endpoint_description["EndpointStatus"]
    return endpoint_status

def query_endpoint(app_name, input_json):
    client = boto3.session.Session().client("sagemaker-runtime", region)

    response = client.invoke_endpoint(
        EndpointName=app_name,
        Body=input_json,
        ContentType='application/json; format=pandas-split',
    )
    preds = response['Body'].read().decode("ascii")
    preds = json.loads(preds)
    print("Received response: {}".format(preds))
    return preds

## check endpoint status
print("Application status is: {}".format(check_status(app_name)))

# Prepare data to give for predictions
iris = datasets.load_iris()
x = iris.data[:, 2:]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=7)

## create test data and make inference from enpoint
query_input = pd.DataFrame(X_train).iloc[[3]].to_json(orient="split")
prediction = query_endpoint(app_name=app_name, input_json=query_input)  
````
      
</li>
    <li>Set variables <code>app_name</code> and <code>region</code> based on your preferences.</li>
    <li>Save the <i>predict.py</i> file.</li>
    <li>Open again the terminal with activated virtual environment <i>deploy_ml</i> and run the file with command <code>python predict.py</code>.</li>
    <li>As a result, you should see an <i>inService</i> message in terminal informing about sucessful new prediction made in the cloud, see the screenshot below.<br>
    <img src="images/Screenshot 2021-09-06 at 17.20.14.png" alt="Sucessfully deployed model to SageMaker", width=575><br>
    </li>
  </ul>
  <p>Once you sucessfully did all the steps above and achieved the same results, in order to avoid extra billing, do not forget to remove <i>SageMaker</i> endpoint and <i>AWS ECR</i> repository with Docker image.</p>
</p>

<h1>Youtube Tutorial is live now - all explained without missing parts</h1>
<p>
<h3>Full Hands-on tutorial of this repo is available now on Youtube!</h3>
<img src="images/cover_ml_deploy_smaller.png" alt="Youtube tutorial - full explained", width=595><br>
<a href="https://youtu.be/FsoSBsrcx9Q">Video Tutorial: Deploy ML model to AWS Sagemaker with mlflow and Docker</a>
</p>
