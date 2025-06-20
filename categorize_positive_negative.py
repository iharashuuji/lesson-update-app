# lambda_positive_negative.py
from common import invoke_model
import json

def lambda_handler(event, context):
    data = json.loads(event['body'])
    msg = data.get('message', '')
    prompt = f"""
次の受講者コメントについて、以下の形式で返してください：
- positive: 良かった点
- negative: 改善が必要な点

コメント:
{msg}

JSONで返答してください。
"""
    text = invoke_model(prompt)
    return {"statusCode":200, "body": text}
