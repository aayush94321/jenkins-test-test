
# # Connecting to Jenkins 

# # from flask import Flask, request, jsonify
# # from config import Config
# # from pipeline_template import pipeline_template
# # from utils import update_pipeline_script, trigger_jenkins_job
# # import os
# # import shutil
# # import git
# # import jenkins

# # app = Flask(__name__)
# # app.config.from_object(Config)

# # # Temporary directory to clone the Git repository
# # TEMP_DIR = "/tmp/git_repo"

# # # Connect to Jenkins
# # jenkins_server = jenkins.Jenkins(
# #     app.config['JENKINS_URL'],
# #     username=app.config['JENKINS_USER'],
# #     password=app.config['JENKINS_TOKEN']
# # )

# # @app.route('/update-pipeline', methods=['POST'])
# # def update_pipeline():
# #     data = request.json

# #     git_branch = data.get('git_branch')
# #     git_repo_url = data.get('git_repo_url')
# #     job_name = data.get('job_name')
    
# #     if not all([git_branch, git_repo_url, job_name]):
# #         return jsonify({"error": "Missing required parameters"}), 400

# #     try:
# #         if os.path.exists(TEMP_DIR):
# #             shutil.rmtree(TEMP_DIR)  # Remove any existing directory
# #         os.makedirs(TEMP_DIR)

# #         git.Repo.clone_from(git_repo_url, TEMP_DIR, branch=git_branch)

# #         # Prepare Jenkins pipeline script
# #         pipeline_script = pipeline_template %(
# #             git_branch,
# #             Config.GIT_CREDENTIALS_ID,
# #             git_repo_url
# #         )

# #         # Path to the Jenkins pipeline script
# #         pipeline_file_path = '/tmp/jenkins_pipeline_script.groovy'

# #         update_pipeline_script(pipeline_file_path, pipeline_script)

# #         # Check if the Jenkins job exists
# #         if not jenkins_server.job_exists(job_name):
# #             # Create a new Jenkins job
# #             job_config = f"""
# #             <flow-definition>
# #               <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
# #                 <script>{pipeline_script}</script>
# #                 <sandbox>true</sandbox>
# #               </definition>
# #               <triggers/>
# #               <disabled>false</disabled>
# #             </flow-definition>
# #             """
# #             jenkins_server.create_job(job_name, job_config)

# #         # Trigger Jenkins job
# #         trigger_jenkins_job(app.config['JENKINS_URL'], job_name, app.config['JENKINS_USER'], app.config['JENKINS_TOKEN'])

# #         return jsonify({"message": "Pipeline updated and triggered successfully"}), 200
    
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500
    
# #     finally:
# #         if os.path.exists(TEMP_DIR):
# #             shutil.rmtree(TEMP_DIR)

# # if __name__ == '__main__':
# #     app.run(debug=True, host="0.0.0.0", port=5001)


# # Pipeline creation with Docker and AWS

# from flask import Flask, request, jsonify
# from config import Config
# from pipeline_template import pipeline_template
# from utils import update_pipeline_script, trigger_jenkins_job
# from yaml_files import default_deployment_content, default_service_content
# import os
# import shutil
# import git
# import jenkins
# import subprocess

# app = Flask(__name__)
# app.config.from_object(Config)

# # Temporary directory to clone the Git repository
# TEMP_DIR = "/tmp/git_repo"

# # Connect to Jenkins
# jenkins_server = jenkins.Jenkins(
#     app.config['JENKINS_URL'],
#     username=app.config['JENKINS_USER'],
#     password=app.config['JENKINS_TOKEN']
# )

# @app.route('/update-pipeline', methods=['POST'])
# def update_pipeline():
#     data = request.json

#     git_branch = data.get('git_branch')
#     git_repo_url = data.get('git_repo_url')
#     job_name = data.get('job_name')
    
#     if not all([git_branch, git_repo_url, job_name]):
#         return jsonify({"error": "Missing required parameters"}), 400

#     try:
#         if os.path.exists(TEMP_DIR):
#             shutil.rmtree(TEMP_DIR)  # Remove any existing directory
#         os.makedirs(TEMP_DIR)

#         git.Repo.clone_from(git_repo_url, TEMP_DIR, branch=git_branch)
        
#         dockerfile_path = os.path.join(TEMP_DIR, 'Dockerfile')
        
#         if not os.path.exists(dockerfile_path):
#             return jsonify({"error": "Dockerfile not found in the repository"}), 400
        
#         # repo_name = os.path.basename(git_repo_url).replace('.git', '')
#         # docker_image_name = f"{repo_name}:{git_branch}"
        
#         repo_name = os.path.basename(git_repo_url).replace('.git', '')
#         docker_image_name = f"{Config.DOCKER_HUB_USERNAME}/{repo_name}:{git_branch}"
        
#         docker_build_command = f"docker build -t {docker_image_name} -f {dockerfile_path} {TEMP_DIR}"
#         build_result = subprocess.run(docker_build_command, shell=True, capture_output=True, text=True)

#         if build_result.returncode != 0:
#             return jsonify({"error": f"Docker build failed: {build_result.stderr}"}), 500
        
#         docker_login_command = f"docker login -u {Config.DOCKER_HUB_USERNAME} -p {Config.DOCKER_HUB_PASSWORD}"
#         login_result = subprocess.run(docker_login_command, shell=True, capture_output=True, text=True)

#         if login_result.returncode != 0:
#             return jsonify({"error": f"Docker login failed: {login_result.stderr}"}), 500

#         docker_push_command = f"docker push {docker_image_name}"
#         push_result = subprocess.run(docker_push_command, shell=True, capture_output=True, text=True)

#         if push_result.returncode != 0:
#             return jsonify({"error": f"Docker push failed: {push_result.stderr}"}), 500
        
#         deployment_content = default_deployment_content.format(
#             job_name=job_name,
#             image_name=docker_image_name
#         )
        
#         service_content = default_service_content.format(
#             job_name=job_name,
#         )
        
#         deployment_file_path = '/tmp/deployment.yaml'
#         service_file_path = '/tmp/service.yaml'

#         with open(deployment_file_path, 'w') as f:
#             f.write(deployment_content)
        
#         with open(service_file_path, 'w') as f:
#             f.write(service_content)
            
#         # pipeline_script = pipeline_template %(
#         #     git_branch,
#         #     Config.GIT_CREDENTIALS_ID,
#         #     git_repo_url,
#         #     Config.DOCKER_CREDENTIALS_ID,
#         #     docker_image_name,
#         #     Config.DOCKER_CREDENTIALS_ID,
#         #     docker_image_name,
#         #     Config.AWS_CREDENTIALS_ID,
#         #     Config.AWS_REGION,
#         #     Config.AWS_REGION,
#         #     Config.EKS_CLUSTER_NAME,
#         #     deployment_file_path,
#         #     service_file_path,
#         #     job_name,
#         #     job_name,
#         #     docker_image_name
#         # )
        
#         pipeline_script = pipeline_template %(
#             git_branch,
#             Config.GIT_CREDENTIALS_ID,
#             git_repo_url,
#             Config.DOCKER_CREDENTIALS_ID,
#             docker_image_name,
#             Config.DOCKER_CREDENTIALS_ID,
#             docker_image_name,
#             deployment_file_path,
#             service_file_path,
#             job_name,
#             job_name,
#             docker_image_name
#         )
        
#         # pipeline_script = pipeline_template %(
#         #     git_branch,
#         #     Config.GIT_CREDENTIALS_ID,
#         #     git_repo_url,
#         #     Config.git_pwd,
#         #     Config.GIT_USERNAME,
#         #     Config.git_pwd,
#         #     # Config.DOCKER_CREDENTIALS_ID,
#         #     # docker_image_name,
#         #     # deployment_file_path,
#         #     # service_file_path,
#         #     # job_name,
#         #     # job_name,
#         #     # docker_image_name
#         # )
        
#         # pipeline_script = pipeline_template.format(
#         #     git_branch=git_branch,
#         #     git_credentials_id=Config.GIT_CREDENTIALS_ID,
#         #     git_repo_url=git_repo_url,
#         #     docker_credentials_id=Config.DOCKER_CREDENTIALS_ID,
#         #     docker_image_name=docker_image_name,
#         #     deployment_file=deployment_file_path,
#         #     service_file=service_file_path,
#         #     job_name=job_name,
#         # )
        
#         pipeline_file_path = '/tmp/jenkins_pipeline_script.groovy'
        
#         update_pipeline_script(pipeline_file_path, pipeline_script)
        
#         if not jenkins_server.job_exists(job_name):
#             job_config = f"""
#             <flow-definition>
#               <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
#                 <script>{pipeline_script}</script>
#                 <sandbox>true</sandbox>
#               </definition>
#               <triggers/>
#               <disabled>false</disabled>
#             </flow-definition>
#             """
#             jenkins_server.create_job(job_name, job_config)
            
#         trigger_jenkins_job(app.config['JENKINS_URL'], job_name, app.config['JENKINS_USER'], app.config['JENKINS_TOKEN'])

#         return jsonify({"message": "Pipeline updated and triggered successfully"}), 200
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
#     finally:
#         if os.path.exists(TEMP_DIR):
#             shutil.rmtree(TEMP_DIR)


# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5001)



# Flask Application to interact with Jenkins

from flask import Flask, request, jsonify
from config import Config
from pipeline_template import pipeline_template
from utils import update_pipeline_script, trigger_jenkins_job
from yaml_files import default_deployment_content, default_service_content
import os
import shutil
import git
import jenkins
import subprocess

app = Flask(__name__)
app.config.from_object(Config)

# Temporary directory to clone the Git repository
TEMP_DIR = "/tmp/git_repo"

# Temporary directory for Jenkins script files
JENKINS_TMP_DIR = "/Users/aayushagrawal/Desktop/jenkins_demo/jenkins_tmp"  # Define this path, e.g., /Users/aayushagrawal/.jenkins/tmp/

# Connect to Jenkins
jenkins_server = jenkins.Jenkins(
    app.config['JENKINS_URL'],
    username=app.config['JENKINS_USER'],
    password=app.config['JENKINS_TOKEN']
)

@app.route('/update-pipeline', methods=['POST'])
def update_pipeline():
    data = request.json

    git_branch = data.get('git_branch')
    git_repo_url = data.get('git_repo_url')
    job_name = data.get('job_name')
    
    if not all([git_branch, git_repo_url, job_name]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)  # Remove any existing directory
        os.makedirs(TEMP_DIR)

        if not os.path.exists(JENKINS_TMP_DIR):
            os.makedirs(JENKINS_TMP_DIR)  # Ensure temp directory for Jenkins exists

        git.Repo.clone_from(git_repo_url, TEMP_DIR, branch=git_branch)
        
        dockerfile_path = os.path.join(TEMP_DIR, 'Dockerfile')
        
        if not os.path.exists(dockerfile_path):
            return jsonify({"error": "Dockerfile not found in the repository"}), 400
        
        repo_name = os.path.basename(git_repo_url).replace('.git', '')
        docker_image_name = f"{Config.DOCKER_HUB_USERNAME}/{repo_name}:{git_branch}"
        
        docker_build_command = f"docker build -t {docker_image_name} -f {dockerfile_path} {TEMP_DIR}"
        build_result = subprocess.run(docker_build_command, shell=True, capture_output=True, text=True)

        if build_result.returncode != 0:
            return jsonify({"error": f"Docker build failed: {build_result.stderr}"}), 500
        
        docker_login_command = f"docker login -u {Config.DOCKER_HUB_USERNAME} -p {Config.DOCKER_HUB_PASSWORD}"
        login_result = subprocess.run(docker_login_command, shell=True, capture_output=True, text=True)

        if login_result.returncode != 0:
            return jsonify({"error": f"Docker login failed: {login_result.stderr}"}), 500

        docker_push_command = f"docker push {docker_image_name}"
        push_result = subprocess.run(docker_push_command, shell=True, capture_output=True, text=True)

        if push_result.returncode != 0:
            return jsonify({"error": f"Docker push failed: {push_result.stderr}"}), 500
        
        deployment_content = default_deployment_content.format(
            job_name=job_name,
            image_name=docker_image_name
        )
        
        service_content = default_service_content.format(
            job_name=job_name,
        )
        
        deployment_file_path = os.path.join(JENKINS_TMP_DIR, 'deployment.yaml')
        service_file_path = os.path.join(JENKINS_TMP_DIR, 'service.yaml')

        with open(deployment_file_path, 'w') as f:
            f.write(deployment_content)
        
        with open(service_file_path, 'w') as f:
            f.write(service_content)
            
        pipeline_script = pipeline_template % (
            git_branch,
            Config.GIT_CREDENTIALS_ID,
            git_repo_url,
            Config.DOCKER_CREDENTIALS_ID,
            docker_image_name,
            Config.DOCKER_CREDENTIALS_ID,
            docker_image_name,
            '/tmp/jenkins_workspace/deployment.yaml',  # Custom workspace path for deployment YAML
            '/tmp/jenkins_workspace/service.yaml',     # Custom workspace path for service YAML
            job_name,
            job_name,
            docker_image_name
        )
        
        pipeline_file_path = os.path.join(JENKINS_TMP_DIR, 'jenkins_pipeline_script.groovy')
        
        update_pipeline_script(pipeline_file_path, pipeline_script)
        
        if not jenkins_server.job_exists(job_name):
            job_config = f"""
            <flow-definition>
              <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
                <script>{pipeline_script}</script>
                <sandbox>true</sandbox>
              </definition>
              <triggers/>
              <disabled>false</disabled>
            </flow-definition>
            """
            jenkins_server.create_job(job_name, job_config)
            
        trigger_jenkins_job(app.config['JENKINS_URL'], job_name, app.config['JENKINS_USER'], app.config['JENKINS_TOKEN'])

        return jsonify({"message": "Pipeline updated and triggered successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
