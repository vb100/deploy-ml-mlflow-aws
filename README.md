<h1>Deploying Models to Production with MLflow and Amazon Sagemaker</h1>

<p>This repo introduces how to prepare you Machine Learning (ML) model for production in AWS Sagemaker with the help of MLflow and AWS Command Line Inteface (AWS CLI). Before start, we should know what is what:
  <ul>
    <li><b>Mlflow</b> - an open source platform for the ML lifecycle.</li>
    <li><b>AWS CLI</b> - is an unified tool to manage your Amazon Web Services (AWS) services.</li>
  </ul>
With this repo you can follow the provided steps on your local machine and AWS account. All steps will be explained clearly with screens and real example.
</p>

<h2>Setup</h2>
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
  <li>Install <i>mlflow</i> package into our virtual environment with the following command:<br><code>pip install mlflow</code>.<br>At the moment of preparing this repo, the version of <i>mlfflow</i> is <code>mlflow==1.20.1</code>.</li>
  <li>To run properly the ML model itself we have to install following modules and packages to our virtual environment as well:
  <ul>
    <li>Pandas: <code>pip install pandas</code>.</li>
    <li>Scikit-learn: <code>pip install -U scikit-learn</code>.</li>
    </ul>
  </li>
</ul>
</p>

<p><h3>Step 3. Test if <i>mlflow</i> is working good</h3>
<ul>
<li>Before doing all following steps, we must be sure if our freshly installed <i>mlflow</i> service if working good on our local machine. To do it, type the following command in the terminal: <code>mlflow ui</code>.</li>
  <li>Open the <i>mlflow</i> dashboard on you browser by entering following URL to your <i>localhost</i>: <code>http://127.0.0.1:5000</code><br>Please keep in mind that this service uses port <code>5000</code> on your machine.<br>You should see <i>mlflow</i> dashboard interface it is shown in the screenshot below:<br>
  <img src="images/Screenshot 2021-08-28 at 17.02.00.png" alt="MLflow Dashboard Interface", width=585><br>
    If you see the same on your browser too, <i>mlflow</i> works fine and we are ready to go to the next steps.
  </li>
</ul>
</p>

<p><h3>Step 4. Adapt your ML training code for <i>mlflow</i></h3>
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
with mlflow.start_run(run_name="Iris RF Experiment") as run:
    mlflow.log_param("num_estimators",num_estimators)
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

<p><h3>Step 5. Run the model and track metrics in <i>mlflow</i></h3>
Once we finished the latest step in this tutorial, <i>mlflow</i> is able to track desired metrics (in our example, <code>mse</code>) in <i>mlflow</i> dashboard. To do it properly, do the following:
<ul>
  <li>Open another terminal windown (be sure the first one with activated <i>mlflow</i> service in port <code>:5000</code> is still running).</li>
  <li>Activate the same virtual environment on the second terminal window as we have created in <b>Step no. 1</b> with the following command: <code>conda activate deploy_ml</code></li>
  <li>Navigate you terminal to the project environment with <code>cd</code> (<i>change directory</i>) terminal command.</li>
  <li>From the second terminal window, simply run the model training code <i>train.py</i> with the command in your terminal: <code>python train.py</code></li>
  <li>Once the train script executed sucessfully, you will be notificated about creation of new experiment in <i>mlflow</i>, calculated MSE, absolute directory path to model artifacts, and <code>runID</code>, see the screen below.<br>
  <img src="images/Screenshot 2021-08-29 at 00.17.59.png" alt="Model trained sucessfully", width=595><br>
  </li>
  <li>Open the browser window again where <i>mlflow</i> service is running on. <b>Refresh the browser window</b>. Then, on the left menu <i>Experiments</i> you will see updated list of experiments ran so far, which includes that one you ran recently in this step (<code>my_classification_model</code>), see the screenshot below.<br>
    <img src="images/Screenshot 2021-08-29 at 00.31.35.png" alt="Mlflow UI with new experiment", width=505><br>
  </li>
  <li>Click on the new experiment, and freely navigate through available options to check metric values and other parameters from the experiment.</li>
  <li>Once you entered to your new experiment space, click on the most recent run tagged with <i>Random Forest Experiment</i> Run time tag. Be sure, that on the <i>Artifacts</i> section you are seeing this kind of structured experiment files with filled content for each file. See screenshot below.<br>
  <img src="images/Screenshot 2021-08-29 at 01.09.13.png" alt="Generated model artifacts in Mlflow UI", width=575><br>
Among the artifact files, there is a <i>conda.yaml</i> file. This is the environment your model needs to run, and it can be heavily customized based on your needs. 
  </li>
  <li>Also, check the file structure in you <i>Finder</i> (Mac OS), or in <i>Windows explorer</i> (Windows OS). You should see new folder <i><b>mlruns</b></i> created in your project directory with run numbers folder(<i>0</i>, <i>1</i>, and so on), <code>runID</code> folder, and full set of artifacts inside. See the screenshot below.<br>
  <img src="images/Screenshot 2021-08-29 at 00.47.20.png" alt="Generated model artifacts in Finder", width=725><br>
  </li>
</ul>
When we are sure that our model can be sucessfully tracked with local <i>mlflow</i> user interface on your local machine, we can go forward to bring our model to the clouds.
</p>

<p><h3>Setup AWS User and Privileges</h3>
Now that we have saved our model artifact, we need to start thinking about deployment. The first step is to provide a Docker image to <b>AWS Elastic Container Registry</b> which we can use to serve our model.
<ul>
  <li>The first step in here is to create out user in <i>AWS Console</i>. To do it, go to <b><i>IAM (Identity and Access Management)</i></b>, then select <b><i>Users</i></b> from the list menu on the left. Then select <b>Add users</b>. On the next screen, provide the new name of <i>User name</i> and mark following checkboxes:
  <ul>
    <li><i>Programmatic access</i>.</li>
    <li><i>AWS Management Console access</i>.</li>
    </ul>
    Leave other properties as in its default values. Now click on <b><i>Next: Permissions</i></b>.
    <ul>
      <li>Here keep activated <i>Add use to group</i> option and click on <b><i>Next: Tags</i></b>.</li>
      <li>You can skip <i>Add tags (optional)</i> step and click on <b></i>Next: Review</i></b>.</li>
      <li>Finally, you can finish to create your new user by clicking on <b><i>Create user</i></b>.</li>
      <li>If everything is fine, on the next screen you will see a notification informing you about success. With this moment, the <b>Access key ID</b> and <b>Secret access key</b> is being generated especially for your user, see the screenshot below.
<img src="images/Screenshot 2021-08-29 at 16.36.03.png" alt="New User in IAM info", width=685><br>
  <p>
  <u><b>Important</b>:</u> Please keep both your Access key ID and Secret access key in the safe place. We will use it in the next steps.
  </p>
  <p>
  Let's make a quick checkpoint here and write it down what we have at the moment:
    
| Service/Parameter name | Value | Source | 
| :---: | :---: | :---: |
| Experiment name | <code>my_classification_model</code> | <i>mlflow</i> UI |
| User | <code>vytautas</code> | <i>AWS IAM</i> |
| <code>run_id</code> | <code>a77178c0fc0d4dddbe8bd1a856aa7d82</code> | <i>AWS IAM</i> |
| Access key ID | <code>AKIAQWIN6X2GSFUEYSXU</code> | <i>AWS IAM</i> |
| Secret access key | <code>r1h7UdPyVK3B2xy54OgSHhHL/wcuqRWUQpuKBbGA</code> | <i>AWS IAM</i> |
| Password | <code>Oo=HRCpgwg9kq_8</code> | <i>AWS IAM</i> |

Prepare the alternative table of your own parameters also.
  </p>
  
  <li>Finally, click <i>Close</i>. On the <i>IAM Users</i> section you will see a new user is being created by you, see the screenshot below.</li>
  <img src="images/Screenshot 2021-08-29 at 17.04.23.png" alt="New user in IAM", width=685><br>
</li>
    </ul>
  </li>
  <li>Before pushing our model directly to AWS ECR, we must to to provide privileges to access AWS ECR to our Account User. We can do it with following steps:
  <ul>
    <li><b>Create an IAM role</b>.</li>
    <ul>
      <li>In <i>IAM</i> dashboard, click on <i><b>Roles</b></i>.</li>
      <li>Click on <b><i>Create role</i></b>.</li>
      <li>On the next screen, click on <b><i>Elastic Container Registry</i></b>. Click on <b><i>Permissions</i></b>.</li>
      <li>On the next screen, you will see <i>ECRReplicationServiceRolePolicy</i> policy listed. You can extend it to see the full Policy parameters set in JSON format. See the screenshot below to be sure you are on the same position.<br>
      <img src="images/Screenshot 2021-08-30 at 00.07.37.png" alt="ECR Privilege on IAM Role", width=625><br>
      </li>
      <li>Click <b><i>Next: Tags</i></b>.</li>
      <li>Click <b><i>Next: Review</i></b>.</li>
      <li>You can provide an quick role description and finally click <b><i>Create role</i></b>.</li>
    </ul>
    After these steps you should see a new role created in the list, see the screenshot below.
    <img src="images/Screenshot 2021-08-30 at 00.21.21.png" alt="New IAM Role", width=615><br>
    <li><b>Create a Policy for the User.</b>
    <ul>
      <li>Select <b><i>Users</i></b> from the left side menu.</li>
      <li>Click small cross icon on the right side or <b><i>Add inline policy</i></b> option.</li>
      <li>Click <b><i>Choose a service</i></b> followed by <i>Service</i> option.</li>
      <li>From the list below select <b><i>Elastic Container Registry</i></b>, see the screenshot below.
      <img src="images/Screenshot 2021-08-30 at 00.45.06.png" alt="ECR Policy to the User", width=575><br></li>
      <li>Select <i><b>All resources</b></i> in front of <i>Resources</i> section, see the screenshot below.
      <img src="images/Screenshot 2021-08-30 at 00.48.35.png" alt="ECR Policy Resources", width=575><br>
      </li>
      <li>Click <b><i>Review policy</i></b>.</li>
      <li>On the next step, set a name for the policy. I set it as <i>policy-for-ecr</i> in this example, see the screenshot below.
      <img src="images/Screenshot 2021-08-30 at 00.55.54.png" alt="ECR Policy Name", width=575><br>
      </li>
      <li>Click <b><i>Create policy</i></b>.</li>
    </li>
  </ul>
  <p>After these steps you should see a newly created policy in the list of policies for the user. See the screenshot below.
  <img src="images/Screenshot 2021-08-30 at 00.58.52.png" alt="New policy in the list", width=575><br>
  </p>
</li>
</ul>
</p>


<p><h3>Amazon ECR Image</h3>
