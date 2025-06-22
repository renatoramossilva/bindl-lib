"""Common utilities for AWS operations."""


class AWSClient:  # pylint: disable=too-few-public-methods
    """
    A class to encapsulate AWS client configuration.
    """

    def __init__(self):
        self.region = "eu-central-1"
        self.account_id = "845590645935"
        self.registry = f"{self.account_id}.dkr.ecr.{self.region}.amazonaws.com"
