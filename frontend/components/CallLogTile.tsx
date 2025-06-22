import React, { useEffect, useState } from 'react'
import {
  PhoneIcon,
  PhoneIncomingIcon,
  ClockIcon,
  PhoneForwardedIcon,
  AlertTriangleIcon,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
const statusColors = {
  'connected-to-agent': 'bg-green-100 text-green-800',
  'connected-to-911': 'bg-red-100 text-red-800',
  'in-progress': 'bg-blue-100 text-blue-800',
}
const statusIcons = {
  'connected-to-agent': <PhoneIcon size={16} className="text-green-600" />,
  'connected-to-911': <AlertTriangleIcon size={16} className="text-red-600" />,
  'in-progress': <PhoneIncomingIcon size={16} className="text-blue-600" />,
}
const statusLabels = {
  'connected-to-agent': 'Connected to Human',
  'connected-to-911': 'Connected to 911',
  'in-progress': 'In Progress',
}
const priorityColors = {
  Emergency: 'bg-red-100 text-red-800 border-red-200',
  'High Priority': 'bg-orange-100 text-orange-800 border-orange-200',
  Normal: 'bg-blue-100 text-blue-800 border-blue-200',
  'Low Priority': 'bg-gray-100 text-gray-800 border-gray-200',
}
const CallLogTile = ({ call, onViewDetails }) => {
  const navigate = useNavigate()
  const [highlight, setHighlight] = useState(call.isNew)

  useEffect(() => {
    if (call.isNew) {
      setHighlight(true)
      const timer = setTimeout(() => {
        setHighlight(false)
        // Optionally, you might want to remove the `isNew` flag from the context state
        // to prevent re-highlighting on re-renders, but that requires a function passed from the context.
        // For now, this local state will handle the visual effect.
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [call.id, call.isNew]) // Depend on call.id to re-trigger for updates to the same call

  const handleConnect = (e) => {
    e.stopPropagation()
    navigate('/transfer', {
      state: {
        call,
      },
    })
  }

  const highlightClass = highlight ? 'highlight-new' : ''

  return (
    <div
      className={`bg-white rounded-lg shadow overflow-hidden hover:shadow-md transition-shadow relative ${highlightClass}`}
    >
      {call.status === 'in-progress' && (
        <button
          onClick={handleConnect}
          className="absolute top-4 right-4 bg-blue-500 hover:bg-blue-600 text-white rounded-full p-2 transition-colors flex items-center"
          title="Connect Call"
        >
          <PhoneForwardedIcon size={16} />
          <span className="ml-1 mr-1 text-sm">Connect</span>
        </button>
      )}
      <div className="p-5 border-b border-gray-100">
        <div className="flex items-start mb-3">
          <span
            className={`px-2.5 py-1 rounded-md text-xs font-medium border ${priorityColors[call.priority]}`}
          >
            {call.priority}
          </span>
        </div>
        <h3 className="text-lg font-semibold text-gray-800">
          {call.user_phone}
        </h3>
        <p className="text-sm text-gray-600 mt-1">{call.user_name}</p>
      </div>
      <div className="px-5 py-4">
        <div className="flex justify-between items-center mb-3">
          <span
            className={`px-2.5 py-0.5 rounded-full text-xs font-medium flex items-center ${statusColors[call.status]}`}
          >
            {statusIcons[call.status]}
            <span className="ml-1">{statusLabels[call.status]}</span>
          </span>
          <span className="text-gray-500 text-sm">{call.duration}</span>
        </div>
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {call.summary}
        </p>
        <div className="flex items-center text-xs text-gray-500">
          <span className="mr-3">
            Topic: <span className="font-medium">{call.topic}</span>
          </span>
        </div>
      </div>
      <div className="bg-gray-50 px-5 py-3 flex justify-end">
        <button
          onClick={() => onViewDetails(call)}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          View Details
        </button>
      </div>
    </div>
  )
}
export default CallLogTile 