import streamlit as st
import openai
import time
import base64

# APIキーを設定
api_key = 'APIキーをここに入力'

# OpenAIクライアントを初期化
openai.api_key = api_key

# Streamlitアプリケーションのタイトルを設定
st.title("GPT-4-vision Chatbot")

# ユーザーからの入力を受け取る
prompt = st.text_input("プロンプトを入力してください:")

# 画像アップロード
image_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])

if image_file:
    # アップロードされた画像ファイルをバイナリ形式に変換
    image_data = image_file.read()
    # Base64エンコード
    image_base64 = base64.b64encode(image_data).decode()
    
    #サムネイル表示
    st.image(image_data, caption="アップロード画像", use_column_width=True)


if st.button("生成") and image_file:
    while True:
        try:
            # 開始時間を記録
            start_time = time.time()

            # Chat Completions APIを使用してテキスト生成をリクエスト
            response = openai.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": image_base64},  # 画像データをバイナリ形式で渡す
                ],
                max_tokens=2000,
            )

            # 終了時間を記録
            end_time = time.time()

            # 実行時間を表示
            execution_time_ms = (end_time - start_time) * 1000
            st.write(f"実行時間(ms): {execution_time_ms}ms")

            # ChatCompletionオブジェクトから生成されたテキストを取得
            generated_text = response.choices[0].message.content
            st.write("返答:\n" + generated_text)
            break  # ループを終了してエラーから抜け出す

        except openai.OpenAIError as e:
            # OpenAI APIからの一般的なエラーをハンドリング
            st.write(f"OpenAI APIエラー")
            st.write(e)
            break  # ループを終了してエラーから抜け出す
        except Exception as e:
            # その他の例外をハンドリング
            st.write(f"エラー")
            st.write(e)
            break  # ループを終了してエラーから抜け出す
