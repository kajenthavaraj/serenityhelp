import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { callLogs as initialCallLogs } from '../utils/mockData'
import { websocketService, CallEvent } from '../services/websocketService'

interface Call {
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
  const [calls, setCalls] = useState<Call[]>(initialCallLogs)

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

  return (
    <CallContext.Provider value={{ calls, removeCall, updateCall }}>
      {children}
    </CallContext.Provider>
  )
} 