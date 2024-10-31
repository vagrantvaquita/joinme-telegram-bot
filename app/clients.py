import boto3


class DynamoDB:
    client = boto3.resource("dynamodb")

    def __init__(self, table):
        self.table = self.client.Table(table)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs): ...

    def delete(self, keys):
        self.table.delete_item(Key=keys)
