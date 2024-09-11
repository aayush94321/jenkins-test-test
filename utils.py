import requests

def update_pipeline_script(pipeline_file_path, pipeline_script):
    with open(pipeline_file_path, 'w') as file:
        file.write(pipeline_script)

def trigger_jenkins_job(jenkins_url, job_name, user, token):
    trigger_url = f'{jenkins_url}job/{job_name}/build?token={token}'
    response = requests.post(trigger_url, auth=(user, token))
    response.raise_for_status()
