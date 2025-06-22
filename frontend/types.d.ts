declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

interface Call {
  id: number;
  callerName: string;
  phoneNumber: string;
  duration: string;
  status: 'connected-to-agent' | 'connected-to-911' | 'in-progress' | 'completed';
  topic: string;
  summary: string;
  priority: 'Emergency' | 'High Priority' | 'Normal' | 'Low Priority';
  transcript: string;
  riskAssessment: {
    selfHarm: number;
    distress: number;
    homicidal: number;
    psychosis: number;
  };
  date?: string;
  time?: string;
}