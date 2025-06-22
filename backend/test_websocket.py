import socketio
import time
import json

# Create a Socket.IO client
sio = socketio.Client()

# Event handlers
@sio.event
def connect():
    print('✅ Connected to WebSocket server')

@sio.event
def disconnect():
    print('❌ Disconnected from WebSocket server')

@sio.on('new_call')
def on_new_call(data):
    print(f'📞 Received new call: {json.dumps(data, indent=2)}')

@sio.on('call_status_update')
def on_call_status_update(data):
    print(f'🔄 Call status update: {json.dumps(data, indent=2)}')

@sio.on('risk_assessment_update')
def on_risk_assessment_update(data):
    print(f'⚠️ Risk assessment update: {json.dumps(data, indent=2)}')

@sio.on('transcript_update')
def on_transcript_update(data):
    print(f'📝 Transcript update: {json.dumps(data, indent=2)}')

@sio.on('frontend_update')
def on_frontend_update(data):
    print(f'🖥️ Frontend update: {json.dumps(data, indent=2)}')

def test_websocket():
    try:
        # Connect to the Flask-SocketIO server
        sio.connect('http://localhost:5000')
        
        # Send a ping to test connection
        sio.emit('ping', {'message': 'Hello from test client'})
        
        # Simulate a new call
        test_call = {
            'user_phone': '+1234567890',
            'user_name': 'Test User',
            'call_duration': '5:30',
            'self_harm_percentage': 25,
            'homicidal_percentage': 10,
            'psychosis_percentage': 15,
            'distress_percentage': 60,
            'call_priority': 'High Priority',
            'call_transcript': 'I am feeling very distressed and need help.',
            'summary': 'User is experiencing high distress levels.'
        }
        
        print('📡 Sending test call...')
        sio.emit('simulate_call', test_call)
        
        # Keep the connection alive for a few seconds
        time.sleep(5)
        
        # Test frontend update function
        print('📡 Testing frontend update...')
        sio.emit('request_call_update', {
            'call_id': 1001,
            'update_type': 'status',
            'new_status': 'connected-to-agent'
        })
        
        time.sleep(2)
        
    except Exception as e:
        print(f'❌ Error: {e}')
    finally:
        sio.disconnect()

if __name__ == '__main__':
    print('🧪 Starting WebSocket test...')
    test_websocket() 