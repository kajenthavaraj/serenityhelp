import io from "socket.io-client";

export interface CallData {
  id: number
  user_phone: string
  user_name: string
  call_duration: string
  self_harm_percentage: number
  homicidal_percentage: number | null
  psychosis_percentage: number
  distress_percentage: number
  call_priority: string | number
  call_transcript: string
  summary: string
}

class WebSocketService {
  private socket: ReturnType<typeof io> | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private eventListeners: Map<string, Function[]> = new Map()
  private isConnecting = false

  connect(url: string = 'http://localhost:5001') {
    if (this.isConnecting || this.socket?.connected) return
    
    try {
      this.isConnecting = true
      this.socket = io(url, {
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: this.reconnectDelay,
      })
      
      this.socket.on('connect', () => {
        console.log('✅ Connected to Flask Socket.IO backend. Socket ID:', this.socket?.id)
        this.reconnectAttempts = 0
        this.isConnecting = false
        this.emit('connected')
        this.socket?.emit('frontend_ready')
      })

      this.socket.on('disconnect', () => {
        console.log('❌ Disconnected from Flask Socket.IO backend')
        this.isConnecting = false
        this.emit('disconnected')
      })

      this.socket.on('connect_error', (error: any) => {
        console.error('❌ Socket.IO connection error:', error)
        this.isConnecting = false
      })

      this.socket.on('new_call', (callData: CallData) => {
        console.log('📞 Received new call via WebSocket:', callData)
        this.emit('newCall', callData)
      })

      this.socket.on('call_status_update', (data: any) => {
        console.log('🔄 Received call status update:', data)
        this.emit('callStatusUpdate', data)
      })

      this.socket.on('risk_assessment_update', (data: any) => {
        console.log('⚠️ Received risk assessment update:', data)
        this.emit('riskAssessmentUpdate', data)
      })

      this.socket.on('transcript_update', (data: any) => {
        console.log('📝 Received transcript update:', data)
        this.emit('transcriptUpdate', data)
      })

    } catch (error) {
      console.error('Failed to connect Socket.IO:', error)
      this.isConnecting = false
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
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  send(event: string, data?: any) {
    if (this.socket && this.socket.connected) {
      this.socket.emit(event, data)
    } else {
      console.warn('Socket.IO is not connected')
    }
  }
}

export const websocketService = new WebSocketService()
