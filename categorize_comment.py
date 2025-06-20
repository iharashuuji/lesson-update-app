# lambda_categorize.py
from common import invoke_model
import json

def lambda_handler(event, context):
    msg = json.loads(event['body']).get('message', '')
    prompt = f"""
以下のフィードバックを分類してください。カテゴリーは「講義内容」「運営」「講義資料」「その他」です。
あと、分類理由も簡単に添えてください。

フィードバック:
{msg}

JSONで返してください。
"""
    text = invoke_model(prompt)
    return {"statusCode":200, "body": text}
