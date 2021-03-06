import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr

class CacheTable:
    def __init__(self, table_name, ttl_days):
        self.table = boto3.resource('dynamodb').Table(table_name)
        self.ttl_days = ttl_days

    def get_item(self, id):
        options = {
            'KeyConditionExpression': Key('id').eq(id)
        }
        response = self.table.query(**options)
        if not response.get('Items'):
            return None

        d = {'id': id}
        for item in response.get('Items'):
            if 'data_' in item:
                d[item['column']] = item['data_']
            else:
                d[item['column']] = item['data']
        return d

    def get_data(self, id, column):
        response = self.table.get_item(
            Key = {
                'id': id,
                'column': column
            }
        )
        return response.get('Item')

    def put_item(self, id, data):
        ttl = datetime.datetime.now() + datetime.timedelta(days=self.ttl_days)
        with self.table.batch_writer() as batch:
            for k, v in data.items():
                if not v:
                    # print(f'id:{id} column:{k} is none')
                    continue
                if k == 'id':
                    continue
                if type(v) is list or type(v) is tuple or type(v) is set or type(v) is dict:
                    batch.put_item(
                        Item={
                            'id': id,
                            'column': k,
                            'data': '_',
                            'data_': v,
                            'TTL': int(ttl.timestamp())
                        }
                    )
                else:
                    batch.put_item(
                        Item={
                            'id': id,
                            'column': k,
                            'data': str(v),
                            'TTL': int(ttl.timestamp())
                        }
                    )
