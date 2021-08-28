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
  <img src="images/Screenshot 2021-08-29 at 00.42.22.png" alt="Generated model artifacts in Mlflow UI", width=575><br>
Among the artifact files, there is a <i>conda.yaml</i> file. This is the environment your model needs to run, and it can be heavily customized based on your needs. 
  </li>
  <li>Also, check the file structure in you <i>Finder</i> (Mac OS), or in <i>Windows explorer</i> (Windows OS). You should see new folder <i><b>mlruns</b></i> created in your project directory with run numbers folder(<i>0</i>, <i>1</i>, and so on), <code>runID</code> folder, and full set of artifacts inside. See the screenshot below.<br>
  <img src="images/Screenshot 2021-08-29 at 00.47.20.png" alt="Generated model artifacts in Finder", width=695><br>
  </li>
</ul>
  
</p>
