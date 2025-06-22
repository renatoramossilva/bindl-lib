"""Class to wrap AWS Lambda operations."""

import boto3
from bindl.aws_wrapper.ecr import ECRClient
from bindl.aws_wrapper.common import AWSClient


class LambdaClient(AWSClient):
    """A class to encapsulate AWS Lambda operations."""

    def __init__(self):
        super().__init__()
        self.lambda_client = boto3.client("lambda", region_name=self.region)

    def deploy_image(self, function_name: str, image_uri: str) -> dict | None:
        """
        Updates a Lambda function with a new image URI.
        """
        print(f"Deploying image {image_uri} to Lambda function {function_name}...")

        try:
            response = self.lambda_client.update_function_code(
                FunctionName=function_name, ImageUri=image_uri, Publish=True
            )
            print("✅ Lambda updated successfully")
            print(f"Version: {response.get('Version')}")
            return response
        except self.lambda_client.exceptions.ResourceNotFoundException:
            print(f"❌ Lambda function '{function_name}' not found.")
            return None
        except Exception as e:  # pylint: disable=broad-except
            print(f"❌ Error during deploy: {e}")
            return None

    def get_latest_image_digest(
        self, repository_name: str, tag: str = "latest"
    ) -> str | None:
        """
        Optionally retrieve the full image digest from ECR to ensure version tracking.
        """
        try:
            response = ECRClient().ecr_client.describe_images(
                repositoryName=repository_name, imageIds=[{"imageTag": tag}]
            )
            image_digest = response["imageDetails"][0]["imageDigest"]
            print(f"Found image digest: {image_digest}")
            return image_digest
        except Exception as e:  # pylint: disable=broad-except
            print(f"❌ Failed to get image digest: {e}")
            return None
