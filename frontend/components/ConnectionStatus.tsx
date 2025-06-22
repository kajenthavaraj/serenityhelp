import React from 'react'
import { useCallContext } from '../contexts/CallContext'
import { WifiIcon, WifiOffIcon, ClockIcon } from 'lucide-react'

const ConnectionStatus: React.FC = () => {
  const { connectionStatus } = useCallContext()

  const getStatusConfig = () => {
    switch (connectionStatus) {
      case 'connected':
        return {
          icon: WifiIcon,
          color: 'text-green-600',
          bgColor: 'bg-green-100',
          text: 'Live Updates'
        }
      case 'connecting':
        return {
          icon: ClockIcon,
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
          text: 'Connecting...'
        }
      case 'disconnected':
        return {
          icon: WifiOffIcon,
          color: 'text-red-600',
          bgColor: 'bg-red-100',
          text: 'Offline'
        }
    }
  }

  const config = getStatusConfig()
  const IconComponent = config.icon

  return (
    <div className={`flex items-center px-3 py-1 rounded-full text-sm font-medium ${config.bgColor} ${config.color}`}>
      <IconComponent size={16} className="mr-2" />
      {config.text}
    </div>
  )
}

export default ConnectionStatus 