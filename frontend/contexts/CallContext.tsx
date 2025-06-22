import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode
} from 'react';
import { callLogs as initialCallLogs } from '../utils/mockData';
import { websocketService } from '../services/websocketService';

interface TranscriptChunk {
  role: string;
  message: string;
  time?: number;
}

interface Call {
  id: number;
  user_phone: string;
  user_name: string;
  call_duration: string;
  status: string;
  topic: string;
  summary: string;
  priority: string | number;
  transcript: string;
  transcriptChunks?: TranscriptChunk[];
  riskAssessment: {
    selfHarm: number;
    distress: number;
    homicidal: number;
    psychosis: number;
  };
  date?: string;
  time?: string;
  isNew?: boolean;
}

interface CallContextType {
  calls: Call[];
  removeCall: (callId: number) => void;
  updateCall: (callId: number, updates: Partial<Call>) => void;
  addCall: (call: Call) => void;
  connectionStatus: 'connected' | 'disconnected' | 'connecting';
}

const CallContext = createContext<CallContextType | undefined>(undefined);

export const useCallContext = () => {
  const context = useContext(CallContext);
  if (!context) throw new Error('useCallContext must be used within a CallProvider');
  return context;
};

interface CallProviderProps {
  children: ReactNode;
}

export const CallProvider: React.FC<CallProviderProps> = ({ children }) => {
  const convertedInitialCalls: Call[] = initialCallLogs.map((call) => ({
    id: call.id,
    user_phone: call.phoneNumber,
    user_name: call.callerName,
    call_duration: call.duration,
    status: call.status,
    topic: call.topic,
    summary: call.summary,
    priority: call.priority,
    transcript: call.transcript,
    transcriptChunks: [],
    riskAssessment: call.riskAssessment,
    date: call.date,
    time: call.time
  }));

  const [calls, setCalls] = useState<Call[]>(convertedInitialCalls);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected');
  const [nextId, setNextId] = useState(1000);

  useEffect(() => {
    setConnectionStatus('connecting');
    websocketService.connect();

    const handleNewCall = (callData: any) => {
      console.log('🆕 New call received in context:', callData);
      const uniqueId = callData.id || nextId;
      const newCall: Call = {
        id: uniqueId,
        user_phone: callData.user_phone,
        user_name: callData.user_name || 'Unknown',
        call_duration: callData.call_duration || '0.0',
        status: 'in-progress',
        topic: callData.summary?.split(' ')[0] || 'General',
        summary: callData.summary || 'Call in progress...',
        priority: callData.call_priority || 'Normal',
        transcript: callData.call_transcript || '',
        transcriptChunks: [],
        riskAssessment: {
          selfHarm: callData.self_harm_percentage || 0,
          distress: callData.distress_percentage || 0,
          homicidal: callData.homicidal_percentage || 0,
          psychosis: callData.psychosis_percentage || 0
        },
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString(),
        isNew: true
      };

      setCalls(prev => [newCall, ...prev]);
      // bump nextId if needed
      setNextId(prev => (uniqueId >= prev ? uniqueId + 1 : prev + 1));
    };

    const handleCallUpdate = (callData: any) => {
      console.log('📝 Call update received:', callData);
      setCalls(prev =>
        prev.map(call =>
          call.user_phone === callData.user_phone
            ? {
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
              }
            : call
        )
      );
    };

    const handleCallEnd = (userPhone: string) => {
      console.log('📴 Call ended:', userPhone);
      setCalls(prev => prev.filter(call => call.user_phone !== userPhone));
    };

    const handleConnected = () => {
      setConnectionStatus('connected');
      console.log('✅ WebSocket connected');
    };

    const handleDisconnected = () => {
      setConnectionStatus('disconnected');
      console.log('❌ WebSocket disconnected');
    };

    const handleCallStatusUpdate = (data: any) => {
      setCalls(prev =>
        prev.map(call =>
          call.id === data.call_id ? { ...call, status: data.status } : call
        )
      );
    };

    const handleRiskAssessmentUpdate = (data: any) => {
      setCalls(prev =>
        prev.map(call =>
          call.id === data.call_id
            ? { ...call, riskAssessment: data.risk_assessment }
            : call
        )
      );
    };

    const handleTranscriptUpdate = (data: any) => {
      setCalls(prev =>
        prev.map(call =>
          call.id === data.call_id
            ? { ...call, transcript: data.transcript }
            : call
        )
      );
    };

    const handleLiveTranscriptUpdate = (msg: {
      call_id: string;
      role: string;
      message: string;
      timestamp: number;
      user_phone: string;
    }) => {
      console.log('🟢 Live transcript update in context:', msg);
      setCalls(prev =>
        prev.map(call =>
          call.user_phone === msg.user_phone
            ? {
                ...call,
                transcriptChunks: [
                  ...(call.transcriptChunks || []),
                  { role: msg.role, message: msg.message, time: msg.timestamp }
                ]
              }
            : call
        )
      );
    };

    websocketService.on('newCall', handleNewCall);
    websocketService.on('callUpdate', handleCallUpdate);
    websocketService.on('callEnd', handleCallEnd);
    websocketService.on('connected', handleConnected);
    websocketService.on('disconnected', handleDisconnected);
    websocketService.on('callStatusUpdate', handleCallStatusUpdate);
    websocketService.on('riskAssessmentUpdate', handleRiskAssessmentUpdate);
    websocketService.on('transcriptUpdate', handleTranscriptUpdate);
    websocketService.on('liveTranscriptUpdate', handleLiveTranscriptUpdate);

    return () => {
      websocketService.off('newCall', handleNewCall);
      websocketService.off('callUpdate', handleCallUpdate);
      websocketService.off('callEnd', handleCallEnd);
      websocketService.off('connected', handleConnected);
      websocketService.off('disconnected', handleDisconnected);
      websocketService.off('callStatusUpdate', handleCallStatusUpdate);
      websocketService.off('riskAssessmentUpdate', handleRiskAssessmentUpdate);
      websocketService.off('transcriptUpdate', handleTranscriptUpdate);
      websocketService.off('liveTranscriptUpdate', handleLiveTranscriptUpdate);
      websocketService.disconnect();
    };
  }, []);

  const removeCall = (callId: number) => {
    setCalls(prev => prev.filter(call => call.id !== callId));
  };

  const updateCall = (callId: number, updates: Partial<Call>) => {
    setCalls(prev =>
      prev.map(call => (call.id === callId ? { ...call, ...updates } : call))
    );
  };

  const addCall = (call: Call) => {
    setCalls(prev => [call, ...prev]);
  };

  return (
    <CallContext.Provider
      value={{ calls, removeCall, updateCall, addCall, connectionStatus }}
    >
      {children}
    </CallContext.Provider>
  );
};