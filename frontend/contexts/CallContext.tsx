import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { callLogs as initialCallLogs } from '../utils/mockData'
import { websocketService } from '../services/websocketService'

interface Call {
  id: number
  user_phone: string
  user_name: string
  call_duration: string
  status: string
  topic: string
  summary: string
  priority: string | number
  transcript: string
  riskAssessment: {
    selfHarm: number
    distress: number
    homicidal: number
    psychosis: number
  }
  date?: string
  time?: string
  isNew?: boolean
}

interface CallContextType {
  calls: Call[]
  removeCall: (callId: number) => void
  updateCall: (callId: number, updates: Partial<Call>) => void
  addCall: (call: Call) => void
  connectionStatus: 'connected' | 'disconnected' | 'connecting'
}

const CallContext = createContext<CallContextType | undefined>(undefined)

export const useCallContext = () => {
  const context = useContext(CallContext)
  if (context === undefined) {
    throw new Error('useCallContext must be used within a CallProvider')
  }
  return context
}

interface CallProviderProps {
  children: ReactNode
}

export const CallProvider: React.FC<CallProviderProps> = ({ children }) => {
  // Convert initialCallLogs to match the new Call interface
  const convertedInitialCalls: Call[] = initialCallLogs.map((call, index) => ({
    id: call.id,
    user_phone: call.phoneNumber,
    user_name: call.callerName,
    call_duration: call.duration,
    status: call.status,
    topic: call.topic,
    summary: call.summary,
    priority: call.priority,
    transcript: call.transcript,
    riskAssessment: call.riskAssessment,
    date: call.date,
    time: call.time
  }))

  const [calls, setCalls] = useState<Call[]>(convertedInitialCalls)
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected')
  const [nextId, setNextId] = useState(1000)

  useEffect(() => {
    // Connect to WebSocket when component mounts
    setConnectionStatus('connecting')
    websocketService.connect()

    // Set up event listeners
    const handleNewCall = (callData: any) => {
      console.log('🆕 New call received in context:', callData)

      const newCall: Call = {
        id: callData.id || nextId,
        user_phone: callData.user_phone,
        user_name: callData.user_name,
        call_duration: callData.call_duration,
        status: 'in-progress',
        topic: callData.summary?.split(' ')[0] || 'General',
        summary: callData.summary,
        priority: callData.call_priority,
        transcript: callData.call_transcript,
        riskAssessment: {
          selfHarm: callData.self_harm_percentage || 0,
          distress: callData.distress_percentage || 0,
          homicidal: callData.homicidal_percentage || 0,
          psychosis: callData.psychosis_percentage || 0
        },
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString()
      }

      setCalls(prevCalls => {
        const existingCallIndex = prevCalls.findIndex(
          call => call.user_phone === newCall.user_phone
        );

        if (existingCallIndex !== -1) {
          // Phone number exists, update the call
          console.log(`📞 Found existing call for ${newCall.user_phone}. Updating tile.`);
          const updatedCalls = [...prevCalls];
          const existingCall = updatedCalls[existingCallIndex];
          
          updatedCalls[existingCallIndex] = { 
            ...existingCall,
            ...newCall,
            id: existingCall.id, // Ensure original ID is preserved
            isNew: true, // Highlight updated calls
          };
          return updatedCalls;

        } else {
          // New phone number, add a new call
          console.log(`📞 No existing call for ${newCall.user_phone}. Creating new tile.`);
          setNextId(prev => Math.max(prev, newCall.id) + 1);
          return [{ ...newCall, isNew: true }, ...prevCalls];
        }
      });
    }

    const handleCallUpdate = (callData: any) => {
      console.log('📝 Call update received:', callData)
      setCalls(prevCalls => 
        prevCalls.map(call => 
          call.user_phone === callData.user_phone ? { 
            ...call, 
            priority: callData.call_priority,
            transcript: callData.call_transcript,
            summary: callData.summary,
            riskAssessment: {
              selfHarm: callData.self_harm_percentage,
              distress: callData.distress_percentage,
              homicidal: callData.homicidal_percentage,
              psychosis: callData.psychosis_percentage
            }
          } : call
        )
      )
    }

    const handleCallEnd = (userPhone: string) => {
      console.log(' Call ended:', userPhone)
      setCalls(prevCalls => prevCalls.filter(call => call.user_phone !== userPhone))
    }

    const handleConnected = () => {
      setConnectionStatus('connected')
      console.log('✅ WebSocket connected')
    }

    const handleDisconnected = () => {
      setConnectionStatus('disconnected')
      console.log('❌ WebSocket disconnected')
    }

    const handleCallStatusUpdate = (data: any) => {
      setCalls(prevCalls => 
        prevCalls.map(call => 
          call.id === data.call_id 
            ? { ...call, status: data.status }
            : call
        )
      )
    }

    const handleRiskAssessmentUpdate = (data: any) => {
      setCalls(prevCalls => 
        prevCalls.map(call => 
          call.id === data.call_id 
            ? { 
                ...call, 
                riskAssessment: data.risk_assessment 
              }
            : call
        )
      )
    }

    const handleTranscriptUpdate = (data: any) => {
      setCalls(prevCalls => 
        prevCalls.map(call => 
          call.id === data.call_id 
            ? { ...call, transcript: data.transcript }
            : call
        )
      )
    }

    // Register event listeners
    websocketService.on('newCall', handleNewCall)
    websocketService.on('callUpdate', handleCallUpdate)
    websocketService.on('callEnd', handleCallEnd)
    websocketService.on('connected', handleConnected)
    websocketService.on('disconnected', handleDisconnected)
    websocketService.on('callStatusUpdate', handleCallStatusUpdate)
    websocketService.on('riskAssessmentUpdate', handleRiskAssessmentUpdate)
    websocketService.on('transcriptUpdate', handleTranscriptUpdate)

    // Cleanup on unmount
    return () => {
      websocketService.off('newCall', handleNewCall)
      websocketService.off('callUpdate', handleCallUpdate)
      websocketService.off('callEnd', handleCallEnd)
      websocketService.off('connected', handleConnected)
      websocketService.off('disconnected', handleDisconnected)
      websocketService.off('callStatusUpdate', handleCallStatusUpdate)
      websocketService.off('riskAssessmentUpdate', handleRiskAssessmentUpdate)
      websocketService.off('transcriptUpdate', handleTranscriptUpdate)
      websocketService.disconnect()
    }
  }, [calls, nextId])

  const removeCall = (callId: number) => {
    setCalls(prevCalls => prevCalls.filter(call => call.id !== callId))
  }

  const updateCall = (callId: number, updates: Partial<Call>) => {
    setCalls(prevCalls => 
      prevCalls.map(call => 
        call.id === callId ? { ...call, ...updates } : call
      )
    )
  }

  const addCall = (call: Call) => {
    setCalls(prevCalls => [call, ...prevCalls])
  }

  return (
    <CallContext.Provider value={{ calls, removeCall, updateCall, addCall, connectionStatus }}>
      {children}
    </CallContext.Provider>
  )
} 