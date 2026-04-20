import boto3
import json
import urllib.request 
import os

# 各種リソースの準備
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserProgress')
bedrock = boto3.client('bedrock-runtime', region_name='ap-southeast-2') 

def lambda_handler(event, context):
    # 1. ユーザーの入力を取得
    user_input = "今日の進捗はゼロです。ゲームをしていました。"
    
    # 2. AIメンターへの命令（プロンプト）
    prompt = f"あなたは非常に論理的で辛辣なAIメンターです。以下のユーザーの進捗を聞いて、厳しく叱咤激励してください。\n進捗：{user_input}"
    
    # 3. Bedrock(Claude 3 Haiku)を呼び出す設定
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    try:
        # AIの返答を生成
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        
        response_body = json.loads(response.get('body').read())
        ai_message = response_body['content'][0]['text']
        
        # 4. DynamoDBにAIの回答を保存する
        table.put_item(
            Item={
                'user_id': 'test_user_001',
                'status': user_input,
                'last_warning': ai_message
            }
        )

        # 5. Discordに送る処理（ここにまとめました）
        webhook_url = os.environ['DISCORD_WEBHOOK_URL']
        
        # headersに User-Agent を追加して、Discordのブロックを回避します
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        data = {
            "content": f"【AIメンターからの喝】\n{ai_message}"
        }
        
        req = urllib.request.Request(webhook_url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req) as res:
            print("Discord Send Success:", res.read().decode())

        # 成功時のレスポンス
        return {
            'statusCode': 200,
            'body': json.dumps({"mentor_message": ai_message}, ensure_ascii=False)
        }

    except Exception as e:
        # エラーが起きた場合は詳細を返す
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': str(e)
        }