import React, { useState } from 'react'
import CallLogTile from './CallLogTile'
import CallDetailsSidebar from './CallDetailsSidebar'
import { callLogs } from '../utils/mockData'
import { BarChart2Icon, PhoneIcon, UserIcon } from 'lucide-react'

const Dashboard = () => {
  const [selectedCall, setSelectedCall] = useState(null)
  const inProgressCalls = callLogs.filter(
    (call) => call.status === 'in-progress',
  )
  // Sort calls by status (in-progress first) and then by priority
  const sortedCalls = [...callLogs].sort((a, b) => {
    // First sort by status - in-progress comes first
    if (a.status === 'in-progress' && b.status !== 'in-progress') return -1
    if (a.status !== 'in-progress' && b.status === 'in-progress') return 1
    // Then sort emergency calls (which will be connected to 911)
    if (a.priority === 'Emergency' && b.priority !== 'Emergency') return -1
    if (a.priority !== 'Emergency' && b.priority === 'Emergency') return 1
    // Then sort by priority within each status group
    const priorityOrder = {
      'High Priority': 2,
      Normal: 3,
      'Low Priority': 4,
    }
    return (priorityOrder[a.priority] || 1) - (priorityOrder[b.priority] || 1)
  })
  return (
    <div className="w-full min-h-screen bg-gray-50 p-6">
      <header className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <PhoneIcon className="text-blue-600" size={32} />
            <div className="ml-2">
              <h1 className="text-3xl font-bold text-gray-800">SerenityHelp</h1>
              <p className="text-gray-600 text-sm">AI-Powered Support Center</p>
            </div>
          </div>
          <div className="flex items-center bg-white rounded-lg shadow px-4 py-2">
            <div className="flex items-center">
              <PhoneIcon className="text-blue-500" size={18} />
              <span className="ml-2 text-gray-500 text-sm">Active Calls:</span>
              <span className="ml-2 text-xl font-bold text-blue-600">
                {inProgressCalls.length}
              </span>
            </div>
          </div>
        </div>
      </header>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-800">Live Calls</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedCalls.map((call) => (
          <CallLogTile
            key={call.id}
            call={call}
            onViewDetails={() => setSelectedCall(call)}
          />
        ))}
      </div>
      <CallDetailsSidebar
        call={selectedCall}
        onClose={() => setSelectedCall(null)}
      />
    </div>
  )
}

export default Dashboard 