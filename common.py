# common.py
import json
import boto3

# Bedrock クライアント初期化
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def invoke_model(prompt, model_id="us.amazon.nova-lite-v1:0", max_tokens=512, temperature=0.7, top_p=0.9):
    """
    指定されたモデルにプロンプトを送信し、応答を取得する関数。

    :param prompt: モデルに送信するプロンプト（文字列）
    :param model_id: 使用するモデルのID（デフォルトは Nova Lite）
    :param max_tokens: 応答の最大トークン数
    :param temperature: 応答の多様性を制御するパラメータ
    :param top_p: 応答の多様性を制御するパラメータ

    :return: モデルの応答（文字列）
    """
    request_payload = {
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p
        }
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        contentType="application/json",
        body=json.dumps(request_payload)
    )

    response_body = json.loads(response["body"].read())
    model_output = response_body["output"]["message"]["content"][0]["text"]
    return model_output
