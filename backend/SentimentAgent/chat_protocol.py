# chat_protocol.py - Real-time Chat Protocol with Live Transcription Support
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement, 
    ChatMessage, 
    TextContent,
    chat_protocol_spec
)
from sentiment_service import (
    LiveSentimentRequest, RealTimeSentimentResponse, LiveTranscriptSegment, 
    TonalityData, live_sentiment_analyzer
)
import json
import uuid
from datetime import datetime
from typing import Dict, List

# Create the real-time chat protocol
live_mental_health_chat = Protocol(spec=chat_protocol_spec)

# Session management for live calls
active_sessions: Dict[str, Dict] = {}

@live_mental_health_chat.on_message(ChatMessage)
async def handle_live_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle real-time chat messages with live transcription support
    """
    try:
        # Extract text content
        text_content = ""
        for item in msg.content:
            if isinstance(item, TextContent):
                text_content += item.text + " "
        
        text_content = text_content.strip()
        
        if not text_content:
            await send_acknowledgment(ctx, sender, msg.msg_id)
        error_response = {"type": "error", "message": f"Session {call_id} not found"}
        await send_analysis_response(ctx, sender, json.dumps(error_response), msg.conversation_id)

async def handle_emergency_check(ctx: Context, sender: str, data: Dict, msg: ChatMessage):
    """Handle emergency status check"""
    call_id = data.get("call_id")
    
    if call_id in active_sessions:
        session = active_sessions[call_id]
        last_analysis = session.get("last_analysis")
        
        if last_analysis:
            emergency_status = {
                "type": "emergency_status",
                "call_id": call_id,
                "current_risk": last_analysis.crisis_risk,
                "urgency": last_analysis.urgency,
                "escalation_triggered": session["escalation_triggered"],
                "recommendation": last_analysis.recommendation,
                "immediate_action_required": last_analysis.escalation_trigger
            }
        else:
            emergency_status = {
                "type": "emergency_status", 
                "call_id": call_id,
                "status": "no_analysis_available"
            }
    else:
        emergency_status = {
            "type": "emergency_status",
            "call_id": call_id,
            "status": "session_not_found"
        }
    
    await send_acknowledgment(ctx, sender, msg.msg_id)
    await send_analysis_response(ctx, sender, json.dumps(emergency_status, indent=2), msg.conversation_id)

async def handle_single_transcript_analysis(ctx: Context, sender: str, text: str, msg: ChatMessage):
    """Handle single transcript analysis (fallback mode)"""
    call_id = str(uuid.uuid4())
    
    # Create single segment
    segment = LiveTranscriptSegment(
        text=text,
        timestamp=datetime.utcnow().timestamp(),
        confidence=0.9,
        is_final=True
    )
    
    # Create request
    request = LiveSentimentRequest(
        call_id=call_id,
        transcript_segments=[segment],
        tonality_data=None,
        session_duration=0,
        timestamp=datetime.utcnow().isoformat()
    )
    
    # Analyze
    analysis_result = live_sentiment_analyzer.analyze_live_sentiment(request)
    
    # Create response
    response_text = create_single_analysis_response(analysis_result)
    
    await send_acknowledgment(ctx, sender, msg.msg_id)
    await send_analysis_response(ctx, sender, response_text, msg.conversation_id)
    
    # Store analysis
    await store_single_analysis(ctx, analysis_result)

async def trigger_escalation_alert(ctx: Context, sender: str, analysis: RealTimeSentimentResponse):
    """Trigger immediate escalation alert"""
    alert = {
        "type": "escalation_alert",
        "call_id": analysis.call_id,
        "urgency": analysis.urgency,
        "crisis_risk": analysis.crisis_risk,
        "recommendation": analysis.recommendation,
        "key_indicators": analysis.key_indicators,
        "timestamp": analysis.analysis_timestamp,
        "immediate_action": True
    }
    
    alert_text = f"""
🚨 **ESCALATION ALERT** 🚨

**Call ID:** {analysis.call_id}
**Urgency Level:** {analysis.urgency.upper()}
**Crisis Risk:** {analysis.crisis_risk}%

**IMMEDIATE ACTION REQUIRED:**
{analysis.recommendation}

**Detected Indicators:**
{', '.join(analysis.key_indicators)}

**Alert Time:** {analysis.analysis_timestamp}
"""
    
    # Send alert via chat
    await send_analysis_response(ctx, sender, alert_text, None)
    
    # Store alert in context storage
    ctx.storage.set(f"escalation_alert_{analysis.call_id}", alert)
    
    ctx.logger.error(f"🚨 ESCALATION ALERT triggered for call {analysis.call_id}")

def create_live_analysis_response(analysis: RealTimeSentimentResponse, session: Dict) -> str:
    """Create formatted response for live analysis"""
    urgency_emoji = {
        "low": "🟢", "medium": "🟡", "high": "🟠", 
        "critical": "🔴", "emergency": "🚨"
    }
    
    # Calculate session stats
    duration_mins = session.get("last_analysis", {}).get("session_duration", 0) // 60
    total_segments = len(session.get("segments", []))
    
    response = f"""
🧠 **Live Mental Health Analysis**

**Session Info:**
• Call ID: {analysis.call_id}
• Duration: {duration_mins:.1f} minutes  
• Segments analyzed: {total_segments}
• Status: {urgency_emoji.get(analysis.urgency, '⚪')} {analysis.urgency.upper()}

**Current Risk Assessment:**
• Crisis Risk: {analysis.crisis_risk}% {get_trend_indicator(analysis.risk_trend)}
• Distress Level: {analysis.distress_level}%
• Emotional Intensity: {analysis.emotional_intensity}%
• Voice Pattern Risk: {analysis.tonality_risk}%
• Confidence: {analysis.confidence:.1%}

**Recommendation:** {analysis.recommendation}
**Next Check:** {analysis.next_check_seconds} seconds
"""

    if analysis.key_indicators:
        response += f"\n**Speech Indicators:** {', '.join(analysis.key_indicators)}"
    
    if analysis.tone_indicators:
        response += f"\n**Voice Indicators:** {', '.join(analysis.tone_indicators)}"
    
    if analysis.escalation_trigger:
        response += f"\n\n⚠️ **ESCALATION TRIGGERED**: {analysis.recommendation}"
    
    # Add JSON for system integration
    response += f"""

**System Data:**
```json
{json.dumps({
    "call_id": analysis.call_id,
    "crisis_risk": analysis.crisis_risk,
    "urgency": analysis.urgency,
    "escalation_trigger": analysis.escalation_trigger,
    "next_check_seconds": analysis.next_check_seconds,
    "recommendation": analysis.recommendation
}, indent=2)}
```
"""
    
    return response

def create_single_analysis_response(analysis: RealTimeSentimentResponse) -> str:
    """Create response for single transcript analysis"""
    urgency_emoji = {
        "low": "🟢", "medium": "🟡", "high": "🟠", 
        "critical": "🔴", "emergency": "🚨"
    }
    
    response = f"""
🧠 **Mental Health Sentiment Analysis**

**Analysis ID:** {analysis.call_id}
**Urgency:** {urgency_emoji.get(analysis.urgency, '⚪')} {analysis.urgency.upper()}

**Risk Metrics:**
• Crisis Risk: {analysis.crisis_risk}%
• Distress Level: {analysis.distress_level}%
• Emotional Intensity: {analysis.emotional_intensity}%
• Analysis Confidence: {analysis.confidence:.1%}

**Recommendation:** {analysis.recommendation}
"""

    if analysis.key_indicators:
        response += f"\n**Detected Indicators:** {', '.join(analysis.key_indicators)}"
    
    if analysis.escalation_trigger:
        response += f"\n\n🚨 **IMMEDIATE ACTION REQUIRED**"
    
    return response

def generate_session_summary(call_id: str, session: Dict) -> str:
    """Generate comprehensive session summary"""
    duration = (datetime.utcnow() - session["start_time"]).total_seconds()
    duration_mins = duration / 60
    
    # Calculate session statistics
    risk_history = session.get("risk_history", [])
    if risk_history:
        max_risk = max(r["crisis_risk"] for r in risk_history)
        avg_risk = sum(r["crisis_risk"] for r in risk_history) / len(risk_history)
        final_risk = risk_history[-1]["crisis_risk"]
        
        # Count urgency levels
        urgency_counts = {}
        for r in risk_history:
            urgency = r["urgency"]
            urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
    else:
        max_risk = avg_risk = final_risk = 0
        urgency_counts = {}
    
    summary = f"""
📊 **Session Summary Report**

**Session Details:**
• Call ID: {call_id}
• Total Duration: {duration_mins:.1f} minutes
• Total Segments: {len(session.get("segments", []))}
• Escalation Triggered: {"Yes" if session.get("escalation_triggered") else "No"}

**Risk Analysis:**
• Maximum Risk: {max_risk}%
• Average Risk: {avg_risk:.1f}%
• Final Risk: {final_risk}%

**Urgency Distribution:**
"""
    
    for urgency, count in urgency_counts.items():
        summary += f"• {urgency.title()}: {count} occurrences\n"
    
    if session.get("last_analysis"):
        last = session["last_analysis"]
        summary += f"""
**Final Assessment:**
• Final Urgency: {last.urgency.upper()}
• Key Indicators: {', '.join(last.key_indicators)}
• Final Recommendation: {last.recommendation}
"""
    
    summary += f"""
**Session Ended:** {datetime.utcnow().isoformat()}
"""
    
    return summary

def get_trend_indicator(trend: str) -> str:
    """Get emoji indicator for risk trend"""
    trends = {
        "increasing": "📈",
        "decreasing": "📉", 
        "stable": "➡️",
        "insufficient_data": "❓"
    }
    return trends.get(trend, "")

async def send_acknowledgment(ctx: Context, sender: str, msg_id: str):
    """Send message acknowledgment"""
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow().isoformat(),
            acknowledged_msg_id=msg_id
        )
    )

async def send_analysis_response(ctx: Context, sender: str, content: str, conversation_id: str):
    """Send analysis response message"""
    await ctx.send(
        sender,
        ChatMessage(
            msg_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            content=[TextContent(text=content)],
            conversation_id=conversation_id
        )
    )

async def store_live_analysis(ctx: Context, call_id: str, analysis: RealTimeSentimentResponse, session: Dict):
    """Store live analysis results for dashboard integration"""
    try:
        # Store latest analysis
        ctx.storage.set(f"live_analysis_{call_id}", {
            "analysis": analysis.dict(),
            "session_info": {
                "start_time": session["start_time"].isoformat(),
                "segments_count": len(session["segments"]),
                "escalation_triggered": session["escalation_triggered"]
            },
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Update global statistics
        await update_live_statistics(ctx, analysis)
        
        # Store in call history
        history_key = "live_call_history"
        history = ctx.storage.get(history_key) or []
        
        history.append({
            "call_id": call_id,
            "timestamp": datetime.utcnow().isoformat(),
            "max_risk": analysis.crisis_risk,
            "urgency": analysis.urgency,
            "escalated": analysis.escalation_trigger
        })
        
        # Keep last 200 calls
        if len(history) > 200:
            history = history[-200:]
        
        ctx.storage.set(history_key, history)
        
    except Exception as e:
        ctx.logger.error(f"Error storing live analysis: {str(e)}")

async def store_single_analysis(ctx: Context, analysis: RealTimeSentimentResponse):
    """Store single analysis result"""
    try:
        # Store in single analysis history
        history_key = "single_analysis_history"
        history = ctx.storage.get(history_key) or []
        
        history.append({
            "call_id": analysis.call_id,
            "timestamp": analysis.analysis_timestamp,
            "analysis": analysis.dict()
        })
        
        # Keep last 100 analyses
        if len(history) > 100:
            history = history[-100:]
        
        ctx.storage.set(history_key, history)
        
        # Update statistics
        await update_live_statistics(ctx, analysis)
        
    except Exception as e:
        ctx.logger.error(f"Error storing single analysis: {str(e)}")

async def update_live_statistics(ctx: Context, analysis: RealTimeSentimentResponse):
    """Update running statistics for live analysis"""
    try:
        stats = ctx.storage.get("live_statistics") or {
            "total_analyses": 0,
            "emergency_alerts": 0,
            "critical_alerts": 0,
            "high_priority": 0,
            "escalations_triggered": 0,
            "average_crisis_risk": 0,
            "average_confidence": 0,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Update counts
        stats["total_analyses"] += 1
        
        if analysis.urgency == "emergency":
            stats["emergency_alerts"] += 1
        elif analysis.urgency == "critical":
            stats["critical_alerts"] += 1
        elif analysis.urgency == "high":
            stats["high_priority"] += 1
        
        if analysis.escalation_trigger:
            stats["escalations_triggered"] += 1
        
        # Update running averages
        total = stats["total_analyses"]
        stats["average_crisis_risk"] = (
            (stats["average_crisis_risk"] * (total - 1) + analysis.crisis_risk) / total
        )
        stats["average_confidence"] = (
            (stats["average_confidence"] * (total - 1) + analysis.confidence) / total
        )
        
        stats["last_updated"] = datetime.utcnow().isoformat()
        
        ctx.storage.set("live_statistics", stats)
        
    except Exception as e:
        ctx.logger.error(f"Error updating live statistics: {str(e)}")

# Health check function for live analysis
async def get_live_agent_status(ctx: Context) -> dict:
    """Get current live agent status and statistics"""
    stats = ctx.storage.get("live_statistics") or {}
    active_session_count = len(active_sessions)
    
    # Get recent escalations
    recent_escalations = []
    for call_id in list(ctx.storage._storage.keys()):
        if call_id.startswith("escalation_alert_"):
            alert = ctx.storage.get(call_id)
            if alert:
                recent_escalations.append(alert)
    
    return {
        "status": "healthy",
        "agent_type": "live_mental_health_analyzer",
        "active_sessions": active_session_count,
        "statistics": stats,
        "recent_escalations": recent_escalations[-10:],  # Last 10
        "capabilities": [
            "real_time_transcription_analysis",
            "voice_tonality_assessment", 
            "live_crisis_detection",
            "automatic_escalation_triggers",
            "session_trend_analysis"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }, msg.msg_id)
            return
        
        # Parse message type (support different real-time formats)
        message_data = await parse_live_message(text_content)
        
        if message_data["type"] == "live_transcript":
            await handle_live_transcript(ctx, sender, message_data, msg)
        elif message_data["type"] == "session_start":
            await handle_session_start(ctx, sender, message_data, msg)
        elif message_data["type"] == "session_end":
            await handle_session_end(ctx, sender, message_data, msg)
        elif message_data["type"] == "emergency_check":
            await handle_emergency_check(ctx, sender, message_data, msg)
        else:
            # Fallback: treat as single transcript analysis
            await handle_single_transcript_analysis(ctx, sender, text_content, msg)
            
    except Exception as e:
        ctx.logger.error(f"Error processing live chat message: {str(e)}")
        await send_acknowledgment(ctx, sender, msg.msg_id)

async def parse_live_message(text_content: str) -> Dict:
    """Parse incoming message to determine type and extract data"""
    try:
        # Try to parse as JSON first
        data = json.loads(text_content)
        return data
    except json.JSONDecodeError:
        # Fallback: treat as plain transcript
        return {
            "type": "single_transcript",
            "transcript": text_content,
            "call_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }

async def handle_live_transcript(ctx: Context, sender: str, data: Dict, msg: ChatMessage):
    """Handle live streaming transcript data"""
    call_id = data.get("call_id")
    
    # Initialize session if not exists
    if call_id not in active_sessions:
        active_sessions[call_id] = {
            "start_time": datetime.utcnow(),
            "segments": [],
            "last_analysis": None,
            "risk_history": [],
            "escalation_triggered": False
        }
    
    session = active_sessions[call_id]
    
    # Create transcript segment
    segment = LiveTranscriptSegment(
        text=data.get("text", ""),
        timestamp=data.get("timestamp", datetime.utcnow().timestamp()),
        confidence=data.get("confidence", 0.8),
        is_final=data.get("is_final", True),
        speaker_id=data.get("speaker_id")
    )
    
    session["segments"].append(segment)
    
    # Create tonality data if provided
    tonality = None
    if "tonality" in data:
        t_data = data["tonality"]
        tonality = TonalityData(
            pitch_mean=t_data.get("pitch_mean", 0.0),
            pitch_variance=t_data.get("pitch_variance", 0.0),
            speech_rate=t_data.get("speech_rate", 0.0),
            volume_level=t_data.get("volume_level", 0.0),
            voice_tremor=t_data.get("voice_tremor", 0.0),
            pause_frequency=t_data.get("pause_frequency", 0.0),
            emotional_tone=t_data.get("emotional_tone", "neutral"),
            tone_confidence=t_data.get("tone_confidence", 0.0)
        )
    
    # Calculate session duration
    duration = (datetime.utcnow() - session["start_time"]).total_seconds()
    
    # Create analysis request
    request = LiveSentimentRequest(
        call_id=call_id,
        transcript_segments=session["segments"],
        tonality_data=tonality,
        session_duration=duration,
        timestamp=datetime.utcnow().isoformat()
    )
    
    # Perform real-time analysis
    analysis_result = live_sentiment_analyzer.analyze_live_sentiment(request)
    session["last_analysis"] = analysis_result
    session["risk_history"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "crisis_risk": analysis_result.crisis_risk,
        "urgency": analysis_result.urgency
    })
    
    # Check for escalation triggers
    if analysis_result.escalation_trigger and not session["escalation_triggered"]:
        session["escalation_triggered"] = True
        await trigger_escalation_alert(ctx, sender, analysis_result)
    
    # Send analysis response
    response_text = create_live_analysis_response(analysis_result, session)
    
    await send_acknowledgment(ctx, sender, msg.msg_id)
    await send_analysis_response(ctx, sender, response_text, msg.conversation_id)
    
    # Store for dashboard
    await store_live_analysis(ctx, call_id, analysis_result, session)
    
    # Log critical events
    if analysis_result.urgency in ["critical", "emergency"]:
        ctx.logger.warning(f"🚨 {analysis_result.urgency.upper()} alert for call {call_id}")
        ctx.logger.warning(f"Crisis risk: {analysis_result.crisis_risk}%, Recommendation: {analysis_result.recommendation}")

async def handle_session_start(ctx: Context, sender: str, data: Dict, msg: ChatMessage):
    """Handle session start event"""
    call_id = data.get("call_id")
    
    active_sessions[call_id] = {
        "start_time": datetime.utcnow(),
        "segments": [],
        "last_analysis": None,
        "risk_history": [],
        "escalation_triggered": False,
        "caller_info": data.get("caller_info", {})
    }
    
    ctx.logger.info(f"🎯 Started live analysis session for call {call_id}")
    
    response = {
        "type": "session_started",
        "call_id": call_id,
        "status": "monitoring_active",
        "message": "Real-time mental health analysis activated"
    }
    
    await send_acknowledgment(ctx, sender, msg.msg_id)
    await send_analysis_response(ctx, sender, json.dumps(response, indent=2), msg.conversation_id)

async def handle_session_end(ctx: Context, sender: str, data: Dict, msg: ChatMessage):
    """Handle session end event"""
    call_id = data.get("call_id")
    
    if call_id in active_sessions:
        session = active_sessions[call_id]
        
        # Generate session summary
        summary = generate_session_summary(call_id, session)
        
        # Clean up session
        del active_sessions[call_id]
        
        ctx.logger.info(f"📊 Ended analysis session for call {call_id}")
        
        await send_acknowledgment(ctx, sender, msg.msg_id)
        await send_analysis_response(ctx, sender, summary, msg.conversation_id)
    else:
        await send_acknowledgment(ctx, sender