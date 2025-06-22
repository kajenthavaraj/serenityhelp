import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { ArrowLeftIcon, PhoneForwardedIcon } from 'lucide-react'
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
const CallTransfer = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const { call } = location.state
  if (!call) {
    return <div>No call data available</div>
  }
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <button
          onClick={() => navigate('/')}
          className="flex items-center text-gray-600 hover:text-gray-800 mb-6"
        >
          <ArrowLeftIcon size={20} className="mr-2" />
          Back to Dashboard
        </button>
        <h1 className="text-2xl font-bold text-green-600 mb-6">
          Connected to agent: +1 (725)-332-2559
        </h1>
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-start">
              <div>
                <h1 className="text-2xl font-bold text-gray-800">
                  {call.phoneNumber}
                </h1>
                <p className="text-lg text-gray-600 mt-1">{call.callerName}</p>
                <div className="flex flex-wrap gap-3 mt-4">
                  <span
                    className={`px-3 py-1.5 rounded-full text-sm font-medium ${statusColors[call.status]}`}
                  >
                    {statusLabels[call.status]}
                  </span>
                  <span
                    className={`px-3 py-1.5 rounded-full text-sm font-medium ${priorityColors[call.priority]}`}
                  >
                    {call.priority}
                  </span>
                  <span className="px-3 py-1.5 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                    {call.duration}
                  </span>
                </div>
                <div className="mt-6">
                  <h2 className="text-lg font-semibold text-gray-800 mb-3">
                    Risk Assessment
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-600">
                        Self Harm
                      </h3>
                      <span
                        className={`text-xl font-bold ${call.riskAssessment.selfHarm > 50 ? 'text-red-600' : 'text-gray-800'}`}
                      >
                        {call.riskAssessment.selfHarm}%
                      </span>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-600">
                        Homicidal
                      </h3>
                      <span
                        className={`text-xl font-bold ${call.riskAssessment.homicidal > 50 ? 'text-red-600' : 'text-gray-800'}`}
                      >
                        {call.riskAssessment.homicidal}%
                      </span>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-600">
                        Distress
                      </h3>
                      <span
                        className={`text-xl font-bold ${call.riskAssessment.distress > 50 ? 'text-red-600' : 'text-gray-800'}`}
                      >
                        {call.riskAssessment.distress}%
                      </span>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-sm font-medium text-gray-600">
                        Psychosis
                      </h3>
                      <span
                        className={`text-xl font-bold ${call.riskAssessment.psychosis > 50 ? 'text-red-600' : 'text-gray-800'}`}
                      >
                        {call.riskAssessment.psychosis}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-2">
                Call Summary
              </h2>
              <p className="text-gray-600">{call.summary}</p>
            </div>
          </div>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Call Transcript
            </h2>
            <div className="whitespace-pre-wrap text-gray-600 font-mono bg-gray-50 p-4 rounded-lg">
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
          <div className="p-6 bg-gray-50 border-t border-gray-200">
            <div className="max-w-md mx-auto"></div>
          </div>
        </div>
      </div>
    </div>
  )
}
export default CallTransfer 