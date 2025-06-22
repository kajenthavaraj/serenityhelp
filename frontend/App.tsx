import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import CallTransfer from './components/pages/CallTransfer'

export function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/transfer" element={<CallTransfer />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
} 