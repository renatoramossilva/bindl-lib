"""Client for managing Docker images in AWS Elastic Container Registry (ECR)."""

import base64

import boto3
import docker
from bindl.aws_wrapper.common import AWSClient


class ECRClient(AWSClient):
    def __init__(self):
        super().__init__()
        self.ecr_client = boto3.client("ecr", region_name=self.region)
        self.docker_client = docker.from_env()

    def login(self) -> None:
        """Logs in to the AWS ECR Docker registry."""
        print(f"Getting ECR token for region {self.region} ...")
        token_response = self.ecr_client.get_authorization_token()
        auth_data = token_response["authorizationData"][0]
        token = auth_data["authorizationToken"]
        proxy_endpoint = auth_data["proxyEndpoint"]

        # Decode token
        decoded = base64.b64decode(token).decode("utf-8")
        username, password = decoded.split(":", 1)

        print(f"Logging in to Docker registry {proxy_endpoint} ...")
        self.docker_client.login(
            username=username, password=password, registry=proxy_endpoint
        )
        print("✅ Login successful")

    def push_image(self, repository: str, tag: str) -> None:
        """
        Pushes a Docker image to the specified ECR repository with the given tag.

        **Request Body:**
        - `repository`: The name of the ECR repository to push the image to.
        - `tag`: The tag for the Docker image.
        """

        image_uri = f"{self.registry}/{repository}:{tag}"
        print(f"Pushing image {image_uri} ...")

        push_logs = self.docker_client.images.push(image_uri, stream=True, decode=True)
        for line in push_logs:
            msg = (
                line.get("status") or line.get("errorDetail", {}).get("message") or line
            )
            print(msg)

    def build_image(
        self, dockerfile_path: str, context_path: str, tag: str
    ) -> docker.models.images.Image:
        """
        Builds a Docker image from the specified Dockerfile and context path.

        **Request Body:**
        - `dockerfile_path`: The path to the Dockerfile.
        - `context_path`: The path to the build context.
        - `tag`: The tag to assign to the built image.

        **Returns:**
        - The built Docker image object.

        **Raises:**
        - `docker.errors.BuildError`: If the build fails.
        """
        print(f"Building image {tag} ...")
        image, logs = self.docker_client.images.build(
            path=context_path,
            dockerfile=dockerfile_path,
            tag=tag,
            rm=True,
        )
        for chunk in logs:
            line = chunk.get("stream") or chunk.get("status") or chunk.get("error")
            if line:
                print(line.strip())
        return image
