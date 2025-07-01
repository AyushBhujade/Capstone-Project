import os , mlflow
from dotenv import load_dotenv
load_dotenv()
def promote_model():
    dagshub_token=os.getenv('CAPSTONE_PROJECT')
    if not dagshub_token:
        raise EnvironmentError('CAPSTONE_PROJECT environment variable is not set')
    os.environ['MLFLOW_TRACKING_USERNAME']=dagshub_token
    os.environ['MLFLOW_TRACKING_PASSWORD']=dagshub_token

    dagshub_url='https://dagshub.com'
    repo_owner='ayushbhujade2005'
    repo_name='Capstone-Project'

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
    
    client=mlflow.MlflowClient()
    
    model_name='my_model'
    
    latest_version_staging=client.get_latest_versions(model_name,stages=['Staging'])[0].version
    
    # archive the current production model
    prod_version=client.get_latest_versions(model_name,stages=['Production'])
    for version in prod_version:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage='Archived'
        )
    
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage='Production'
    )
    
    print(f"model version {latest_version_staging} promoted to production")
    
if __name__=='__main__':
    promote_model()