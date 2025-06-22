import React from 'react'
import { PhoneForwardedIcon, XIcon } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
const priorityColors = {
  Emergency: 'bg-red-100 text-red-800 border-red-200',
  'High Priority': 'bg-orange-100 text-orange-800 border-orange-200',
  Normal: 'bg-blue-100 text-blue-800 border-blue-200',
  'Low Priority': 'bg-gray-100 text-gray-800 border-gray-200',
}
const statusColors = {
  'connected-to-agent': 'bg-green-100 text-green-800',
  'connected-to-911': 'bg-red-100 text-red-800',
  'in-progress': 'bg-blue-100 text-blue-800',
}
const statusLabels = {
  'connected-to-agent': 'Connected to Human',
  'connected-to-911': 'Connected to 911',
  'in-progress': 'In Progress',
}
const getRiskColor = (percentage) => {
  if (percentage >= 70) return 'bg-red-100 text-red-800'
  if (percentage >= 30) return 'bg-orange-100 text-orange-800'
  return 'bg-green-100 text-green-800'
}
const CallDetailsSidebar = ({ call, onClose }) => {
  const navigate = useNavigate()
  if (!call) return null
  const handleConnect = () => {
    navigate('/transfer', {
      state: {
        call,
      },
    })
  }
  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-white shadow-lg transform transition-transform duration-300 ease-in-out z-50">
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-xl font-semibold text-gray-800">
                {call.phoneNumber}
              </h2>
              <p className="text-sm text-gray-600 mt-1">{call.callerName}</p>
              <div className="flex flex-wrap gap-2 mt-3">
                <span
                  className={`px-2.5 py-1 rounded-full text-xs font-medium ${statusColors[call.status]}`}
                >
                  {statusLabels[call.status]}
                </span>
                <span
                  className={`px-2.5 py-1 rounded-full text-xs font-medium ${priorityColors[call.priority]}`}
                >
                  {call.priority}
                </span>
                <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  {call.duration}
                </span>
              </div>
              <div className="mt-3 text-sm grid grid-cols-2 gap-2">
                <div>
                  Self Harm:{' '}
                  <span
                    className={
                      call.riskAssessment.selfHarm > 50
                        ? 'text-red-600 font-medium'
                        : ''
                    }
                  >
                    {call.riskAssessment.selfHarm}%
                  </span>
                </div>
                <div>
                  Homicidal:{' '}
                  <span
                    className={
                      call.riskAssessment.homicidal > 50
                        ? 'text-red-600 font-medium'
                        : ''
                    }
                  >
                    {call.riskAssessment.homicidal}%
                  </span>
                </div>
                <div>
                  Distress:{' '}
                  <span
                    className={
                      call.riskAssessment.distress > 50
                        ? 'text-red-600 font-medium'
                        : ''
                    }
                  >
                    {call.riskAssessment.distress}%
                  </span>
                </div>
                <div>
                  Psychosis:{' '}
                  <span
                    className={
                      call.riskAssessment.psychosis > 50
                        ? 'text-red-600 font-medium'
                        : ''
                    }
                  >
                    {call.riskAssessment.psychosis}%
                  </span>
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700"
            >
              <XIcon size={20} />
            </button>
          </div>
          <div className="mt-4">
            <h4 className="font-medium text-gray-800 mb-2">Summary</h4>
            <p className="text-gray-600 text-sm">{call.summary}</p>
          </div>
        </div>
        <div className="flex-1 overflow-auto p-6">
          <h4 className="font-medium text-gray-800 mb-2">Call Transcript</h4>
          <div className="whitespace-pre-wrap text-sm text-gray-600 font-mono">
            {call.transcript.split('\n').map(
              (line, index) =>
                line.trim() && (
                  <div
                    key={index}
                    className={`py-1 px-2 ${line.startsWith('Agent:') ? 'bg-blue-100' : ''}`}
                  >
                    {line}
                  </div>
                ),
            )}
          </div>
        </div>
        {call.status === 'in-progress' && (
          <div className="p-6 border-t border-gray-200">
            <button
              onClick={handleConnect}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white rounded-lg py-3 px-4 flex items-center justify-center transition-colors"
            >
              <PhoneForwardedIcon size={18} className="mr-2" />
              Connect
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
export default CallDetailsSidebar 