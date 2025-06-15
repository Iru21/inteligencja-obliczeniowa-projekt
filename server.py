from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import sys

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/run_script')
def run_script():
    script_name = request.args.get('script')
    subject = request.args.get('subject')
    
    if not script_name or not subject:
        return jsonify({'success': False, 'error': 'Missing script name or subject'}), 400
    
    allowed_scripts = ['analyze_sentiment.py', 'cloud.py']
    if script_name not in allowed_scripts:
        return jsonify({'success': False, 'error': 'Invalid script name'}), 400
    
    try:
        python_executable = sys.executable
        cmd = [python_executable, script_name, '--subject', subject]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            return jsonify({
                'success': False,
                'error': f'Script execution failed: {stderr}'
            }), 500
        
        return jsonify({
            'success': True,
            'output': stdout
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error executing script: {str(e)}'
        }), 500

@app.route('/sentiments/<path:filename>')
def serve_sentiment_image(filename):
    return send_from_directory('sentiments', filename)

@app.route('/wordclouds/<path:filename>')
def serve_wordcloud_image(filename):
    return send_from_directory('wordclouds', filename)

if __name__ == '__main__':
    os.makedirs('sentiments', exist_ok=True)
    os.makedirs('wordclouds', exist_ok=True)
    
    print("Starting server at http://localhost:5000")
    app.run(debug=True)