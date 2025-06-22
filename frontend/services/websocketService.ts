export interface CallEvent {
  type: 'new_call' | 'call_update' | 'call_end' | 'call_transfer' | 'call_status_update' | 'risk_assessment_update' | 'transcript_update' | 'frontend_update'
  data: {
    user_phone: string
    user_name: string
    call_duration: string
    self_harm_percentage: number
    homicidal_percentage: number
    psychosis_percentage: number
    distress_percentage: number
    call_priority: string
    call_transcript: string
    summary: string
  }
}

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private eventListeners: Map<string, Function[]> = new Map()
  private isConnecting = false

  connect(url: string = 'ws://localhost:5000/ws') {
    if (this.isConnecting) return
    
    try {
      this.isConnecting = true
      this.ws = new WebSocket(url)
      
      this.ws.onopen = () => {
        console.log('✅ WebSocket connected to Flask backend')
        this.reconnectAttempts = 0
        this.isConnecting = false
        this.emit('connected')
      }

      this.ws.onmessage = (event) => {
        try {
          const callEvent: CallEvent = JSON.parse(event.data)
          this.handleCallEvent(callEvent)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onclose = () => {
        console.log('❌ WebSocket disconnected from Flask backend')
        this.isConnecting = false
        this.emit('disconnected')
        this.attemptReconnect()
      }

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        this.isConnecting = false
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      this.isConnecting = false
    }
  }

  private handleCallEvent(event: CallEvent) {
    switch (event.type) {
      case 'new_call':
        this.emit('newCall', event.data)
        break
      case 'call_update':
        this.emit('callUpdate', event.data)
        break
      case 'call_end':
        this.emit('callEnd', event.data.user_phone)
        break
      case 'call_transfer':
        this.emit('callTransfer', event.data)
        break
      case 'call_status_update':
        this.handleCallStatusUpdate(event.data)
        break
      case 'risk_assessment_update':
        this.handleRiskAssessmentUpdate(event.data)
        break
      case 'transcript_update':
        this.handleTranscriptUpdate(event.data)
        break
      case 'frontend_update':
        this.handleFrontendUpdate(event.data)
        break
      default:
        console.warn('Unknown event type:', event.type)
    }
  }

  private handleCallStatusUpdate = (data: any) => {
    this.emit('callStatusUpdate', data)
  }

  private handleRiskAssessmentUpdate = (data: any) => {
    this.emit('riskAssessmentUpdate', data)
  }

  private handleTranscriptUpdate = (data: any) => {
    this.emit('transcriptUpdate', data)
  }

  private handleFrontendUpdate = (data: any) => {
    this.emit('frontendUpdate', data)
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      setTimeout(() => {
        this.connect()
      }, this.reconnectDelay * this.reconnectAttempts)
    } else {
      console.error('❌ Max reconnection attempts reached')
    }
  }

  on(event: string, callback: Function) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, [])
    }
    this.eventListeners.get(event)!.push(callback)
  }

  off(event: string, callback: Function) {
    const listeners = this.eventListeners.get(event)
    if (listeners) {
      const index = listeners.indexOf(callback)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }

  private emit(event: string, data?: any) {
    const listeners = this.eventListeners.get(event)
    if (listeners) {
      listeners.forEach(callback => callback(data))
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  // Test methods for debugging
  sendTestMessage() {
    this.send({
      type: 'ping',
      message: 'Hello from React frontend!'
    })
  }

  simulateNewCall() {
    this.send({
      type: 'simulate_call',
      data: {
        user_phone: '+1 (555) 999-9999',
        user_name: 'Test User',
        call_duration: '2m 30s',
        self_harm_percentage: 25,
        homicidal_percentage: 5,
        psychosis_percentage: 15,
        distress_percentage: 40,
        call_priority: 'Normal',
        call_transcript: 'Agent: Hello, how can I help you today?\nUser: Hi, this is a test call.',
        summary: 'Test call for WebSocket functionality.'
      }
    })
  }
}

export const websocketService = new WebSocketService()
