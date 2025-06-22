export interface CallEvent {
  type: 'new_call' | 'call_update' | 'call_end' | 'call_transfer'
  data: {
    id: number
    callerName: string
    phoneNumber: string
    duration: string
    status: string
    topic: string
    summary: string
    priority: string
    transcript: string
    riskAssessment: {
      selfHarm: number
      distress: number
      homicidal: number
      psychosis: number
    }
    date?: string
    time?: string
  }
}

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private eventListeners: Map<string, Function[]> = new Map()

  connect(url: string = 'ws://localhost:8000/ws/calls') {
    try {
      this.ws = new WebSocket(url)
      
      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
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
        console.log('WebSocket disconnected')
        this.emit('disconnected')
        this.attemptReconnect()
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
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
        this.emit('callEnd', event.data.id)
        break
      case 'call_transfer':
        this.emit('callTransfer', event.data)
        break
      default:
        console.warn('Unknown event type:', event.type)
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      setTimeout(() => {
        this.connect()
      }, this.reconnectDelay * this.reconnectAttempts)
    } else {
      console.error('Max reconnection attempts reached')
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
    }
  }
}

export const websocketService = new WebSocketService() 