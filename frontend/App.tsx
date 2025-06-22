import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import CallTransfer from './components/pages/CallTransfer'
import { CallProvider } from './contexts/CallContext'
import { websocketService } from './services/websocketService'

export function App() {
  useEffect(() => {
    // Initialize WebSocket connection when app starts
    console.log('🚀 Initializing WebSocket connection...')
    websocketService.connect()
    
    // Cleanup on unmount
    return () => {
      websocketService.disconnect()
    }
  }, [])

  return (
    <CallProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transfer" element={<CallTransfer />} />
          </Routes>
        </div>
      </BrowserRouter>
    </CallProvider>
  )
} 