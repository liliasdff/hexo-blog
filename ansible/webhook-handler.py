#!/usr/bin/env python3
"""
GitHub Webhook处理器 - 自动触发博客部署
"""

from flask import Flask, request, jsonify
import subprocess
import hmac
import hashlib
import os
import logging

app = Flask(__name__)

# 配置
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', 'your-secret-key')
DEPLOY_SCRIPT = 'deploy.bat'  # Windows版本

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_signature(payload_body, secret_token, signature_header):
    """验证GitHub webhook签名"""
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        secret_token.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """处理GitHub webhook"""
    signature_header = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    
    if not verify_signature(payload, WEBHOOK_SECRET, signature_header):
        logger.warning("Invalid webhook signature")
        return jsonify({'error': 'Invalid signature'}), 403
    
    event = request.headers.get('X-GitHub-Event')
    
    if event == 'push':
        data = request.json
        
        # 只处理main分支的推送
        if data.get('ref') == 'refs/heads/main':
            logger.info("Received push to main branch, starting deployment...")
            
            try:
                # 执行部署脚本
                result = subprocess.run([DEPLOY_SCRIPT], 
                                      capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    logger.info("Deployment completed successfully")
                    return jsonify({'status': 'success', 'message': 'Blog deployed successfully'})
                else:
                    logger.error(f"Deployment failed: {result.stderr}")
                    return jsonify({'status': 'error', 'message': 'Deployment failed'}), 500
                    
            except subprocess.TimeoutExpired:
                logger.error("Deployment timeout")
                return jsonify({'status': 'error', 'message': 'Deployment timeout'}), 500
            except Exception as e:
                logger.error(f"Deployment error: {str(e)}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            return jsonify({'status': 'ignored', 'message': 'Not main branch'})
    
    return jsonify({'status': 'ignored', 'message': 'Event not handled'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)