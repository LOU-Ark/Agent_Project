from web.app import app
import os

# このファイルが直接 `python run.py` として実行された場合のみ、
# Flaskの開発サーバーを起動します。
# (Gunicornからモジュールとしてインポートされた場合は、このブロックは実行されません)
if __name__ == '__main__':
    # Cloud Run環境ではPORT環境変数が設定されますが、ローカル開発では5000番ポートを使います。
    port = int(os.environ.get("PORT", 5000))
    # ローカルでテストしやすいように、debug=Trueにしておきます。
    app.run(debug=True, host='0.0.0.0', port=port)