from flask import Flask, render_template, jsonify
import logging
import os
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """メインダッシュボード"""
    return render_template('index.html')

@app.route('/settings')
def settings():
    """設定ページ"""
    return render_template('settings.html')

@app.route('/api/status')
def get_status():
    """ボットのステータスを返す"""
    # 注: この実装は簡略化されています
    return jsonify({
        'status': 'online',
        'uptime': '0h',
        'message_count': 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))