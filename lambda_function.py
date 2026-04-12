import random

def lambda_handler(event, context):
    # AIに言わせたい「うざい台詞」のリスト
    messages = [
        "まだそんなとこで止まってるとかやる気ある？",
        "進捗どうですか？あ、聞くまでもなかったですね。画面が止まってますもんね（笑）",
        "今のペースだと、試験合格率は統計的に見て10%以下です。応援してますよ、一応（笑）"
    ]
    
    # リストの中からランダムに1つ選ぶ
    selected_message = random.choice(messages)
    
    # 選んだメッセージを返す
    return {
        'statusCode': 200,
        'body': selected_message
    }
