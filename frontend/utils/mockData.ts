export const callLogs = [
  {
    id: 1,
    callerName: 'Sarah Johnson',
    phoneNumber: '+1 (555) 123-4567',
    duration: '5m 32s',
    status: 'connected-to-agent',
    topic: 'Anxiety',
    summary:
      'Helped Sarah manage her anxiety and provided coping strategies for daily stress.',
    priority: 'Normal',
    transcript: `
Agent: Hello, thank you for calling SerenityHelp. How can I help you today?
Sarah: Hi, I've been feeling really anxious lately and need some help managing it.
Agent: I'd be happy to help you with that, Sarah. First, let's talk about what's been causing your anxiety.
Sarah: Sure, I've been feeling overwhelmed with work and personal life.
Agent: Perfect, I can understand that feeling. Let's start with some breathing exercises and then discuss coping strategies. Have you tried any relaxation techniques yet?
Sarah: No, not really. What would you recommend?
Agent: I'll guide you through a simple breathing exercise right now. While we do that, let me explain some other anxiety management techniques...
    `,
    riskAssessment: {
      selfHarm: 15,
      distress: 45,
      homicidal: 5,
      psychosis: 20,
    },
  },
  {
    id: 2,
    callerName: 'Michael Chen',
    phoneNumber: '+1 (555) 234-5678',
    date: 'Today',
    time: '9:15 AM',
    duration: '8m 47s',
    status: 'connected-to-911',
    topic: 'Panic Attack',
    summary:
      'Experiencing severe panic attack symptoms. Provided immediate intervention and emergency support.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Michael: Hi, I'm having a really bad panic attack and can't seem to calm down.
Agent: I'd be happy to help you with that. Let me guide you through some immediate calming techniques.
Michael: Thank you, I appreciate it.
Agent: Of course! Let's start with deep breathing. Can you take a slow, deep breath with me?
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 3,
    callerName: 'Emily Rodriguez',
    phoneNumber: '+1 (555) 345-6789',
    date: 'Today',
    time: '8:30 AM',
    duration: '3m 12s',
    status: 'in-progress',
    topic: 'Suicidal',
    summary:
      'Expressing suicidal thoughts and feelings. Immediate crisis intervention required.',
    priority: 'Emergency',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Emily: Hi, I've been having thoughts about ending my life and I don't know what to do.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Emily: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about these thoughts...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 4,
    callerName: 'David Thompson',
    phoneNumber: '+1 (555) 456-7890',
    date: 'Yesterday',
    time: '4:50 PM',
    duration: '12m 05s',
    status: 'completed',
    topic: 'Coping tips',
    summary:
      'Discussed various coping strategies for managing stress and difficult emotions.',
    priority: 'Low Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
David: Hi, I'm looking for some coping tips to help me manage my stress better.
Agent: I'd be happy to help you with that. Let me pull up your account information.
David: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about coping strategies...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 5,
    callerName: 'Aisha Patel',
    phoneNumber: '+1 (555) 567-8901',
    date: 'Yesterday',
    time: '2:30 PM',
    duration: '7m 18s',
    status: 'completed',
    topic: 'Mild stress',
    summary:
      'Provided guidance on managing mild stress and daily life pressures.',
    priority: 'Normal',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Aisha: Hi, I've been feeling mildly stressed lately and need some advice.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Aisha: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about mild stress...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 6,
    callerName: 'James Wilson',
    phoneNumber: '+1 (555) 678-9012',
    date: 'Yesterday',
    time: '11:20 AM',
    duration: '1m 45s',
    status: 'in-progress',
    topic: 'Addiction',
    summary:
      'Currently discussing addiction recovery and seeking support for substance use.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
James: Hi, I'm struggling with addiction and need help finding recovery resources.
Agent: I'd be happy to help you with that. Let me pull up your account information.
James: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about addiction recovery...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 7,
    callerName: 'Olivia Martinez',
    phoneNumber: '+1 (555) 789-0123',
    date: 'Oct 12, 2023',
    time: '3:15 PM',
    duration: '4m 30s',
    status: 'completed',
    topic: 'Needing someone to talk to',
    summary:
      'Provided emotional support and active listening for someone feeling isolated.',
    priority: 'Urgent',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Olivia: Hi, I just really need someone to talk to right now. I'm feeling very alone.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Olivia: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about feeling isolated...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 8,
    callerName: 'Robert Kim',
    phoneNumber: '+1 (555) 890-1234',
    date: 'Oct 12, 2023',
    time: '1:05 PM',
    duration: '6m 22s',
    status: 'completed',
    topic: 'Anxiety',
    summary:
      'Assisted with anxiety management techniques and provided ongoing support strategies.',
    priority: 'Normal',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Robert: Hi, I've been dealing with anxiety and need some help managing it.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Robert: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about anxiety management...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 9,
    callerName: 'Sophia Lee',
    phoneNumber: '+1 (555) 901-2345',
    date: 'Oct 11, 2023',
    time: '10:40 AM',
    duration: '9m 51s',
    status: 'completed',
    topic: 'Coping tips',
    summary:
      'Walked through various coping mechanisms for managing difficult emotions and situations.',
    priority: 'Low Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Sophia: Hi, I need some coping tips to help me get through a difficult time.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Sophia: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about coping strategies...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  // Additional 20 active calls
  {
    id: 10,
    callerName: 'Alex Rivera',
    phoneNumber: '+1 (555) 111-2222',
    date: 'Today',
    time: '10:15 AM',
    duration: '2m 30s',
    status: 'in-progress',
    topic: 'Panic Attack',
    summary: 'Experiencing panic attack symptoms and seeking immediate support.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Alex: Hi, I'm having a panic attack and need help calming down.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Alex: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about the panic attack...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 11,
    callerName: 'Maria Garcia',
    phoneNumber: '+1 (555) 222-3333',
    date: 'Today',
    time: '10:30 AM',
    duration: '4m 15s',
    status: 'in-progress',
    topic: 'Homicidal',
    summary: 'Expressing homicidal thoughts requiring immediate crisis intervention.',
    priority: 'Emergency',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Maria: Hi, I'm having thoughts about harming someone and I'm scared.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Maria: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about these thoughts...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 12,
    callerName: 'Kevin Zhang',
    phoneNumber: '+1 (555) 333-4444',
    date: 'Today',
    time: '10:45 AM',
    duration: '1m 55s',
    status: 'in-progress',
    topic: 'Addiction',
    summary: 'Seeking help for addiction recovery and treatment options.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Kevin: Hi, I'm struggling with addiction and need help finding treatment.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Kevin: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about addiction treatment...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 13,
    callerName: 'Lisa Thompson',
    phoneNumber: '+1 (555) 444-5555',
    date: 'Today',
    time: '11:00 AM',
    duration: '3m 20s',
    status: 'in-progress',
    topic: 'Mild stress',
    summary: 'Managing mild stress and seeking coping strategies.',
    priority: 'Normal',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Lisa: Hi, I've been feeling mildly stressed and need some help managing it.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Lisa: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about mild stress...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 14,
    callerName: 'Carlos Mendez',
    phoneNumber: '+1 (555) 555-6666',
    date: 'Today',
    time: '11:15 AM',
    duration: '5m 10s',
    status: 'in-progress',
    topic: 'Panic Attack',
    summary: 'Experiencing severe panic attack requiring immediate intervention.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Carlos: Hi, I'm having a really bad panic attack and need help right now.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Carlos: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about the panic attack...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 15,
    callerName: 'Jennifer White',
    phoneNumber: '+1 (555) 666-7777',
    date: 'Today',
    time: '11:30 AM',
    duration: '2m 45s',
    status: 'in-progress',
    topic: 'Needing someone to talk to',
    summary: 'Feeling isolated and seeking emotional support and connection.',
    priority: 'Low Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Jennifer: Hi, I just really need someone to talk to. I'm feeling very lonely.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Jennifer: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about feeling lonely...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 16,
    callerName: 'Marcus Johnson',
    phoneNumber: '+1 (555) 777-8888',
    date: 'Today',
    time: '11:45 AM',
    duration: '6m 30s',
    status: 'in-progress',
    topic: 'Psychosis',
    summary: 'Experiencing psychotic symptoms requiring immediate crisis intervention.',
    priority: 'Emergency',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Marcus: Hi, I'm experiencing some really scary thoughts and I think I might be losing touch with reality.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Marcus: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about these experiences...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 17,
    callerName: 'Amanda Foster',
    phoneNumber: '+1 (555) 888-9999',
    date: 'Today',
    time: '12:00 PM',
    duration: '3m 55s',
    status: 'in-progress',
    topic: 'Anxiety',
    summary: 'Managing anxiety symptoms and seeking coping strategies.',
    priority: 'Normal',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Amanda: Hi, I've been feeling really anxious and need help managing it.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Amanda: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about anxiety...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 18,
    callerName: 'Ryan Davis',
    phoneNumber: '+1 (555) 999-0000',
    date: 'Today',
    time: '12:15 PM',
    duration: '4m 20s',
    status: 'in-progress',
    topic: 'Addiction',
    summary: 'Seeking support for addiction recovery and relapse prevention.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Ryan: Hi, I'm in recovery but I'm worried about relapsing and need support.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Ryan: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about relapse prevention...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 19,
    callerName: 'Sofia Rodriguez',
    phoneNumber: '+1 (555) 000-1111',
    date: 'Today',
    time: '12:30 PM',
    duration: '2m 10s',
    status: 'in-progress',
    topic: 'Coping tips',
    summary: 'Seeking coping strategies for managing daily life challenges.',
    priority: 'Low Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Sofia: Hi, I need some coping tips to help me deal with my current situation.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Sofia: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about coping strategies...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 20,
    callerName: 'Daniel Brown',
    phoneNumber: '+1 (555) 111-0000',
    date: 'Today',
    time: '12:45 PM',
    duration: '5m 45s',
    status: 'in-progress',
    topic: 'Panic Attack',
    summary: 'Experiencing panic attack symptoms and seeking immediate calming techniques.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Daniel: Hi, I'm having a panic attack and can't seem to calm down.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Daniel: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about the panic attack...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 21,
    callerName: 'Emma Wilson',
    phoneNumber: '+1 (555) 222-1111',
    date: 'Today',
    time: '1:00 PM',
    duration: '3m 30s',
    status: 'in-progress',
    topic: 'Suicidal',
    summary: 'Expressing suicidal ideation requiring immediate crisis intervention.',
    priority: 'Emergency',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Emma: Hi, I've been thinking about ending my life and I don't know what to do.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Emma: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about these thoughts...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 22,
    callerName: 'Thomas Anderson',
    phoneNumber: '+1 (555) 333-2222',
    date: 'Today',
    time: '1:15 PM',
    duration: '4m 50s',
    status: 'in-progress',
    topic: 'Mild stress',
    summary: 'Managing mild stress and seeking support for daily pressures.',
    priority: 'Normal',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Thomas: Hi, I've been feeling mildly stressed and need some help managing it.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Thomas: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about mild stress...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 23,
    callerName: 'Natalie Clark',
    phoneNumber: '+1 (555) 444-3333',
    date: 'Today',
    time: '1:30 PM',
    duration: '2m 25s',
    status: 'in-progress',
    topic: 'Addiction',
    summary: 'Seeking help for addiction and recovery support.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Natalie: Hi, I'm struggling with addiction and need help finding support.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Natalie: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about addiction support...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 24,
    callerName: 'Christopher Lee',
    phoneNumber: '+1 (555) 555-4444',
    date: 'Today',
    time: '1:45 PM',
    duration: '6m 15s',
    status: 'in-progress',
    topic: 'Needing someone to talk to',
    summary: 'Feeling isolated and seeking emotional support and connection.',
    priority: 'Low Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Christopher: Hi, I just really need someone to talk to right now. I'm feeling very alone.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Christopher: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about feeling alone...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 25,
    callerName: 'Isabella Martinez',
    phoneNumber: '+1 (555) 666-5555',
    date: 'Today',
    time: '2:00 PM',
    duration: '3m 40s',
    status: 'in-progress',
    topic: 'Homicidal',
    summary: 'Expressing homicidal thoughts requiring immediate crisis intervention.',
    priority: 'Emergency',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Isabella: Hi, I'm having thoughts about harming someone and I'm really scared.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Isabella: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about these thoughts...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 26,
    callerName: 'Andrew Taylor',
    phoneNumber: '+1 (555) 777-6666',
    date: 'Today',
    time: '2:15 PM',
    duration: '4m 05s',
    status: 'in-progress',
    topic: 'Panic Attack',
    summary: 'Experiencing severe panic attack requiring immediate intervention.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Andrew: Hi, I'm having a really bad panic attack and need help calming down.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Andrew: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about the panic attack...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 27,
    callerName: 'Victoria Green',
    phoneNumber: '+1 (555) 888-7777',
    date: 'Today',
    time: '2:30 PM',
    duration: '2m 50s',
    status: 'in-progress',
    topic: 'Anxiety',
    summary: 'Managing anxiety symptoms and seeking support.',
    priority: 'Low Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Victoria: Hi, I've been feeling anxious and need some help managing it.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Victoria: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about anxiety...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 28,
    callerName: 'Joshua Hall',
    phoneNumber: '+1 (555) 999-8888',
    date: 'Today',
    time: '2:45 PM',
    duration: '5m 20s',
    status: 'in-progress',
    topic: 'Addiction',
    summary: 'Seeking help for addiction recovery and treatment options.',
    priority: 'High Priority',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Joshua: Hi, I'm struggling with addiction and need help finding treatment options.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Joshua: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about addiction treatment...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
  {
    id: 29,
    callerName: 'Mia Johnson',
    phoneNumber: '+1 (555) 000-9999',
    date: 'Today',
    time: '3:00 PM',
    duration: '3m 15s',
    status: 'in-progress',
    topic: 'Psychosis',
    summary: 'Experiencing psychotic symptoms requiring immediate crisis intervention.',
    priority: 'Emergency',
    transcript: `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
Mia: Hi, I'm experiencing some really scary thoughts and I think I might be losing touch with reality.
Agent: I'd be happy to help you with that. Let me pull up your account information.
Mia: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about these experiences...
    `,
    riskAssessment: {
      selfHarm: Math.floor(Math.random() * 100),
      distress: Math.floor(Math.random() * 100),
      homicidal: Math.floor(Math.random() * 100),
      psychosis: Math.floor(Math.random() * 100),
    },
  },
].map((call) => ({
  ...call,
  // Ensure priority is one of the allowed values
  priority: call.priority === 'Urgent' ? 'High Priority' : call.priority,
  riskAssessment: call.riskAssessment || {
    selfHarm: Math.floor(Math.random() * 100),
    distress: Math.floor(Math.random() * 100),
    homicidal: Math.floor(Math.random() * 100),
    psychosis: Math.floor(Math.random() * 100),
  },
  status:
    call.priority === 'Emergency'
      ? 'connected-to-911'
      : call.status === 'in-progress'
        ? 'in-progress'
        : 'connected-to-agent',
  transcript:
    call.transcript ||
    `
Agent: Thank you for calling SerenityHelp. How may I assist you today?
${call.callerName}: Hi, I'm calling about ${call.topic.toLowerCase()}.
Agent: I'd be happy to help you with that. Let me pull up your account information.
${call.callerName}: Thank you, I appreciate it.
Agent: Of course! Now, let's address your concerns about ${call.topic.toLowerCase()}...
  `,
})) 