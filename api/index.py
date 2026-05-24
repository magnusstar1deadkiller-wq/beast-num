from flask import Flask, request, jsonify, send_from_directory
import requests
import json
import os

app = Flask(__name__)

@app.route('/num', methods=['GET'])
def phone_info():
    # Get parameters from request
    key = request.args.get('key')
    phone = request.args.get('num')
    
    # Validate API key — TERI KEY "beast"
    if key != 'beast':
        return jsonify({
            'error': 'Invalid API key. Use key=beast',
            'developer': '@beastaccuser'
        }), 401
    
    # Validate phone number
    if not phone:
        return jsonify({
            'error': 'Missing phone number. Use ?num=XXXXXXXXXX',
            'developer': '@beastaccuser'
        }), 400
    
    # Call real API (original wali)
    real_api_url = f'https://anon-num-info.vercel.app/num?key=num5017temp&num={phone}'
    
    try:
        response = requests.get(real_api_url, timeout=30)
        response.raise_for_status()
        real_data = response.json()
        
        # Transform to YOUR desired response format
        your_response = {
            'response': real_data.get('response'),
            'developer': '@beastaccuser'  # Your name
        }
        
        return jsonify(your_response)
        
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Real API timeout. Try again.',
            'developer': '@beastaccuser'
        }), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': f'Failed to fetch: {str(e)}',
            'developer': '@beastaccuser'
        }), 502

@app.route('/', methods=['GET'])
def home():
    # Serve the HTML landing page
    try:
        return send_from_directory('public', 'index.html')
    except:
        # Fallback to JSON if HTML is not found
        return jsonify({
            'name': 'Beast Number Info API',
            'endpoint': '/num?key=beast&num=PHONE_NUMBER',
            'example': 'https://beast-num-info.vercel.app/num?key=beast&num=6205769287',
            'developer': '@beastaccuser'
        })

@app.route('/api', methods=['GET'])
def api_info():
    # JSON endpoint for API information
    return jsonify({
        'name': 'Beast Number Info API',
        'endpoint': '/num?key=beast&num=PHONE_NUMBER',
        'example': 'https://beast-num-info.vercel.app/num?key=beast&num=6205769287',
        'developer': '@beastaccuser'
    })

# Vercel needs this
app.debug = True
