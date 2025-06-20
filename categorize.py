
import json
import boto3
import re

MODEL_ID = "us.amazon.nova-lite-v1:0"
REGION = "us-east-1"

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        message = body.get("message", "")

        # モデルに渡すメッセージ
        prompt = f"""
        以下のユーザーのメッセージに返答してください。また、その返答の感情を
        ポジティブ、ネガティブ、中立 の３つの中から一つだけ選んでください。
        返答はJSON形式で、"response" に返答文、"sentiment" に感情を入れてください。

        ユーザーのメッセージ:
        {message}
        """

        bedrock_messages = [{
            "role": "user",
            "content": [{"text": prompt}]
        }]

        request_payload = {
            "messages": bedrock_messages,
            "inferenceConfig": {
                "maxTokens": 512,
                "temperature": 0.7,
                "topP": 0.9
            }
        }

        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            body=json.dumps(request_payload)
        )
        response_body = json.loads(response["body"].read())
        model_output = response_body["output"]["message"]["content"][0]["text"]
        match = re.search(r"```json\s*(\{.*?\})\s*```", model_output, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            json_text = model_output
        try:
            result = json.loads(json_text)
        except json.JSONDecodeError:
            result = {
                "respose":model_output,
                "sentiment":"不明"
            }



        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }