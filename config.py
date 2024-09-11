import os

class Config:
    JENKINS_URL = os.getenv('JENKINS_URL')
    JENKINS_USER = os.getenv('JENKINS_USER')
    JENKINS_TOKEN = os.getenv('JENKINS_TOKEN')
    GIT_CREDENTIALS_ID = os.getenv('GIT_CREDENTIALS_ID')
    GIT_USERNAME = os.getenv('GIT_USERNAME')
    git_pwd = os.getenv('git_pwd')

    DOCKER_HUB_USERNAME = os.getenv('DOCKER_HUB_USERNAME')
    DOCKER_HUB_PASSWORD = os.getenv('DOCKER_HUB_PASSWORD')
    DOCKER_CREDENTIALS_ID = os.getenv('DOCKER_CREDENTIALS_ID')
    
    KUBECONFIG_PATH = os.getenv('KUBECONFIG_PATH', os.path.expanduser('~/.kube/config'))