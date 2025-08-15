from pathlib import Path

from common import AWSClient
from ecr import ECRClient
from lambda_fn import LambdaClient

# LAMBDA VARIABLES
FUNCTION_NAME = "flnks_lambda"  # lambda function name

# === ECR VARIABLES ===
IMAGE_URI_TEMPLATE = "{registry}/{repository}:{tag}"
REPOSITORY = "my-ecr"  # ECR repository name

# LOCAL VARIABLES
DOCKERFILE_PATH = "docker/Dockerfile"
CONTEXT_PATH = "."

# === EXECUTION FLOW ===
docker_mgr = ECRClient()
lambda_mgr = LambdaClient()

tag = "flnks-1.0.9"
image_uri = IMAGE_URI_TEMPLATE.format(
    registry=AWSClient().registry, repository=REPOSITORY, tag=tag
)

docker_mgr.login()
docker_mgr.build_image(
    dockerfile_path=DOCKERFILE_PATH, context_path=CONTEXT_PATH, tag=image_uri
)
docker_mgr.push_image(repository=REPOSITORY, tag=tag)
lambda_mgr.deploy_image(FUNCTION_NAME, image_uri)
