# データをDynamoDBから引っ張てくるもので主に、精度評価のためのデータを引っ張ってくる目的のファイルである。
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def load_day_data_from_dynamodb(day_key: str) -> list[dict]:
    """
    DynamoDBから特定の日付のフィードバックコメントを取得

    Args:
        day_key (str): 例 "Day1"

    Returns:
        List[dict]: コメントのリスト
    """
    region = os.getenv("AWS_REGION")
    table_name = os.getenv("DYNAMO_TABLE_NAME")

    if not region or not table_name:
        raise ValueError("AWS_REGIONやDYNAMO_TABLE_NAMEが.envに定義されていません")

    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)

    # 例: パーティションキー "day": "Day1" でコメントを取得
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('day').eq(day_key)
    )

    items = response.get("Items", [])
    return items
