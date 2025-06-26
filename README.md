# SerenityHelp

## Inspiration
Last year, a friend of mine was going through a mental health crisis. We called our school-sponsored helpline only to be left on hold for 20 minutes before we decided to hang up.

Researching the issue, we found that helplines can take up to 15 minutes to connect calls during peak hours.

## What it does
You can call our helpline yourself at (765) 245-8252

We wanted to build a tool to allow helplines to let AI voice agent handle calls during peak traffic where human reps aren't available. Instead of being left on hold, callers can talk to a voice AI agent that can triage the call's urgency, allowing human agents to be more quickly connected to high-risk callers while having the AI voice agent give callers someone to talk to while they wait; potentially de-escalating a fatal crisis.

## How we built it
We used the Vapi framework to process calls and embed agentic tools to display on our frontend dashboard.
-Vapi hosts 4 tools
       - Deepgram(which converts voice to text
       - Fetch.ai(our sentiment analysis agent that takes in both the audio recording and text transcript and creates a sentiment analysis in 4 categories to be used to update profiles on the dashboard
        -Groq is used for its fast speeds needed to process and respond to text input from the user to power our Live AI Phone call Voice Agent 
         -LMNT takes the script Groq has written and converts from text to speech to communicate the message back the user 

## Challenges we ran into
- Needed to create a custom multimodal sentiment analysis model to triage our helpline's calls.
- We initially struggled with a complex backend setup and infrastructure issues while hosting our model. To streamline deployment, we turned to Fetch.ai—hosting the model there and integrating it into our app via a simple API call.

## Accomplishments that we're proud of
- Be able to detect sentiment over the audio call to be able to quantify self-harm, homicidal, psychosis, and distress ratings
-  Live display of each call with transcript, distress ratings, recording, and user information

## What we learned
- How to use Vapi to host voice AI calls
- Deploying a model for sentiment analysis
- Using Fetch.ai to host multimodal agents

## What's next for SerenityHelp
- Create a login auth to allow call center agents to sign up automatically

## Vapi
Vapi was the backbone of our voice AI infrastructure. It enabled us to easily manage real-time, bidirectional audio conversations between callers and our AI agent. Through Vapi, we connected four core tools into one cohesive pipeline:

Deepgram for speech-to-text transcription of live calls

Groq to rapidly process transcripts and generate empathetic, context-aware responses using LLMs

LMNT to convert Groq's outputs into humanlike speech, enabling natural voice interactions

Fetch.ai to run our custom multimodal sentiment analysis agent, which takes in both text and audio to assess crisis indicators in real time

Vapi made it possible to stitch all of these components together seamlessly, handling call flow logic and latency requirements while giving us the flexibility to plug in specialized tools at each step. Without Vapi, building a fully functional AI voice agent in under 12 hours wouldn’t have been feasible.

## Fetch AI
We used Fetch.ai to deploy and host our custom sentiment analysis agent, which plays a critical role in triaging mental health crisis calls. The agent ingests both the audio recording and text transcript of each call and returns a real-time analysis across four key emotional dimensions: self-harm, homicidal ideation, psychosis, and distress.

Initially, we struggled with complex infrastructure when trying to host this model ourselves. Fetch.ai’s Agentverse platform made it easy to deploy the agent and expose it via a simple API call, dramatically simplifying our backend.

Fetch.ai also allowed us to build a multimodal pipeline, enabling richer, context-aware insights by analyzing both voice tone and spoken content. These insights update our frontend dashboard live, helping human agents prioritize and respond faster to the most urgent calls.

## Groq
Groq was essential to powering the real-time intelligence behind our AI voice agent. We used Groq to run our LLM-based reasoning system that generates empathetic, context-aware responses to the caller’s input during live phone conversations.

What set Groq apart was its blazing-fast inference speed—crucial for maintaining a natural, uninterrupted dialogue between the caller and the AI. In a crisis setting, even a few seconds of delay can feel like forever. Groq’s ultra-low latency allowed us to process speech-to-text inputs and return meaningful responses in real time, without awkward pauses or delays.

Thanks to Groq, we were able to maintain fluid, high-quality conversations that feel responsive and human-like—an essential part of building trust and de-escalating crises through voice AI.
