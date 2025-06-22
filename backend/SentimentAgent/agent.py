# agent.py - Live Mental Health Sentiment Agent
from uagents import Agent, Context
from uagents.experimental.quota import QuotaProtocol, RateLimit
from chat_protocol import live_mental_health_chat, get_live_agent_status, active_sessions
from sentiment_service import live_sentiment_analyzer, LiveSentimentRequest, LiveTranscriptSegment
import asyncio
import json
from datetime import datetime

# Agent configuration for live analysis
agent = Agent(
    name="live_mental_health_agent",
    seed="live_mental_health_secret_seed_2024_v2",  # Change for production
    port=8002,
    mailbox=True  # Enable for Agentverse communication
)

# Rate limiting for live analysis (higher limits for real-time)
quota_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="LiveSentimentQuota",
    version="1.0.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=200)  # 200/hour for live
)

# Include protocols
agent.include(live_mental_health_chat, publish_manifest=True)
agent.include(quota_protocol, publish_manifest=True)

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    """Initialize the live analysis agent"""
    ctx.logger.info("🎤 Live Mental Health Analysis Agent Starting...")
    ctx.logger.info(f"Agent address: {ctx.agent.address}")
    
    # Initialize agent info
    ctx.storage.set("agent_info", {
        "name": "Live Mental Health Sentiment Analyzer",
        "version": "2.0.0",
        "type": "real_time_crisis_detector",
        "description": "Real-time analysis of live conversation transcripts with voice tonality",
        "capabilities": [
            "Live transcription analysis",
            "Voice tonality assessment",
            "Real-time crisis detection", 
            "Automatic escalation triggers",
            "Session-based trend analysis",
            "Emergency alert system"
        ],
        "supported_formats": [
            "deepgram_live_transcript",
            "segment_based_analysis",
            "tonality_integrated_analysis"
        ],
        "urgency_levels": ["low", "medium", "high", "critical", "emergency"],
        "max_concurrent_sessions": 50,
        "analysis_intervals": {
            "emergency": "5 seconds",
            "critical": "10 seconds", 
            "high": "15 seconds",
            "medium": "30 seconds",
            "low": "60 seconds"
        }
    })
    
    # Test the live analyzer
    try:
        test_segment = LiveTranscriptSegment(
            text="I'm feeling okay, just testing the system",
            timestamp=datetime.utcnow().timestamp(),
            confidence=0.9,
            is_final=True
        )
        
        test_request = LiveSentimentRequest(
            call_id="startup_test",
            transcript_segments=[test_segment],
            session_duration=0,
            timestamp=datetime.utcnow().isoformat()
        )
        
        test_result = live_sentiment_analyzer.analyze_live_sentiment(test_request)
        ctx.logger.info("✅ Live sentiment analyzer initialized successfully")
        ctx.logger.info(f"Test analysis: {test_result.urgency} urgency, {test_result.crisis_risk}% risk")
        
    except Exception as e:
        ctx.logger.error(f"❌ Error initializing live analyzer: {str(e)}")

@agent.on_interval(period=120.0)  # Every 2 minutes
async def health_check_handler(ctx: Context):
    """Enhanced health check for live analysis"""
    try:
        status = await get_live_agent_status(ctx)
        active_count = status.get("active_sessions", 0)
        total_analyses = status.get("statistics", {}).get("total_analyses", 0)
        emergency_count = status.get("statistics", {}).get("emergency_alerts", 0)
        
        ctx.logger.info(f"🔄 Health Check - Active: {active_count}, Total: {total_analyses}")
        
        if emergency_count > 0:
            ctx.logger.warning(f"🚨 Total emergency alerts: {emergency_count}")
        
        # Clean up old sessions (> 2 hours inactive)
        await cleanup_inactive_sessions(ctx)
        
    except Exception as e:
        ctx.logger.error(f"Health check failed: {str(e)}")

@agent.on_message(model=dict)
async def handle_direct_live_message(ctx: Context, sender: str, msg: dict):
    """Handle direct API messages for live analysis integration"""
    try:
        msg_type = msg.get("type")
        
        if msg_type == "get_live_status":
            status = await get_live_agent_status(ctx)
            await ctx.send(sender, status)
            
        elif msg_type == "start_live_session":
            call_id = msg.get("call_id")
            caller_info = msg.get("caller_info", {})
            
            response = await start_live_session(ctx, call_id, caller_info)
            await ctx.send(sender, response)
            
        elif msg_type == "live_transcript_segment":
            result = await process_live_segment(ctx, msg)
            await ctx.send(sender, result)
            
        elif msg_type == "end_live_session":
            call_id = msg.get("call_id")
            summary = await end_live_session(ctx, call_id)
            await ctx.send(sender, summary)
            
        elif msg_type == "emergency_status_check":
            call_id = msg.get("call_id")
            status = await get_emergency_status(ctx, call_id)
            await ctx.send(sender, status)
            
        elif msg_type == "get_session_summary":
            call_id = msg.get("call_id")
            summary = await get_session_summary(ctx, call_id)
            await ctx.send(sender, summary)
            
        else:
            await ctx.send(sender, {
                "type": "error",
                "message": f"Unknown message type: {msg_type}",
                "supported_types": [
                    "get_live_status", "start_live_session", "live_transcript_segment",
                    "end_live_session", "emergency_status_check", "get_session_summary"
                ]
            })
            
    except Exception as e:
        ctx.logger.error(f"Error handling direct live message: {str(e)}")
        await ctx.send(sender, {
            "type": "error", 
            "message": str(e)
        })

async def start_live_session(ctx: Context, call_id: str, caller_info: dict) -> dict:
    """Start a new live analysis session"""
    if call_id in active_sessions:
        return {
            "type": "session_start_response",
            "status": "error",
            "message": f"Session {call_id} already active"
        }
    
    active_sessions[call_id] = {
        "start_time": datetime.utcnow(),
        "segments": [],
        "last_analysis": None,
        "risk_history": [],
        "escalation_triggered": False,
        "caller_info": caller_info
    }
    
    ctx.logger.info(f"🎯 Started live session: {call_id}")
    
    return {
        "type": "session_start_response",
        "status": "success",
        "call_id": call_id,
        "message": "Live mental health analysis session started",
        "monitoring_active": True
    }

async def process_live_segment(ctx: Context, msg: dict) -> dict:
    """Process a live transcript segment"""
    call_id = msg.get("call_id")
    
    if call_id not in active_sessions:
        return {
            "type": "segment_analysis_error",
            "message": f"Session {call_id} not found. Start session first."
        }
    
    # Create segment
    segment = LiveTranscriptSegment(
        text=msg.get("text", ""),
        timestamp=msg.get("timestamp", datetime.utcnow().timestamp()),
        confidence=msg.get("confidence", 0.8),
        is_final=msg.get("is_final", True),
        speaker_id=msg.get("speaker_id")
    )
    
    session = active_sessions[call_id]
    session["segments"].append(segment)
    
    # Create tonality data if provided
    tonality = None
    if "tonality" in msg:
        from sentiment_service import TonalityData
        t_data = msg["tonality"]
        tonality = TonalityData(**t_data)
    
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
    
    # Perform analysis
    analysis_result = live_sentiment_analyzer.analyze_live_sentiment(request)
    
    # Update session
    session["last_analysis"] = analysis_result
    session["risk_history"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "crisis_risk": analysis_result.crisis_risk,
        "urgency": analysis_result.urgency
    })
    
    # Check escalation
    if analysis_result.escalation_trigger and not session["escalation_triggered"]:
        session["escalation_triggered"] = True
        ctx.logger.error(f"🚨 ESCALATION triggered for {call_id}")
    
    # Store analysis
    await store_live_analysis_direct(ctx, call_id, analysis_result, session)
    
    return {
        "type": "live_analysis_result",
        "call_id": call_id,
        "analysis": analysis_result.dict(),
        "session_info": {
            "duration_seconds": duration,
            "segments_count": len(session["segments"]),
            "escalation_triggered": session["escalation_triggered"]
        }
    }

async def end_live_session(ctx: Context, call_id: str) -> dict:
    """End a live analysis session"""
    if call_id not in active_sessions:
        return {
            "type": "session_end_error",
            "message": f"Session {call_id} not found"
        }
    
    session = active_sessions[call_id]
    duration = (datetime.utcnow() - session["start_time"]).total_seconds()
    
    # Generate summary
    summary = {
        "type": "session_summary",
        "call_id": call_id,
        "duration_seconds": duration,
        "total_segments": len(session["segments"]),
        "escalation_triggered": session["escalation_triggered"],
        "final_analysis": session.get("last_analysis", {}).dict() if session.get("last_analysis") else None,
        "risk_trend": calculate_session_risk_trend(session["risk_history"]),
        "ended_at": datetime.utcnow().isoformat()
    }
    
    # Clean up
    del active_sessions[call_id]
    
    ctx.logger.info(f"📊 Ended live session: {call_id} ({duration:.1f}s)")
    
    return summary

async def get_emergency_status(ctx: Context, call_id: str) -> dict:
    """Get emergency status for a call"""
    if call_id not in active_sessions:
        return {
            "type": "emergency_status",
            "call_id": call_id,
            "status": "session_not_found"
        }
    
    session = active_sessions[call_id]
    last_analysis = session.get("last_analysis")
    
    if not last_analysis:
        return {
            "type": "emergency_status",
            "call_id": call_id,
            "status": "no_analysis_available"
        }
    
    return {
        "type": "emergency_status",
        "call_id": call_id,
        "current_crisis_risk": last_analysis.crisis_risk,
        "urgency_level": last_analysis.urgency,
        "escalation_triggered": session["escalation_triggered"],
        "immediate_action_required": last_analysis.escalation_trigger,
        "recommendation": last_analysis.recommendation,
        "last_analysis_time": last_analysis.analysis_timestamp
    }

async def get_session_summary(ctx: Context, call_id: str) -> dict:
    """Get detailed session summary"""
    if call_id not in active_sessions:
        # Try to get from storage
        stored_summary = ctx.storage.get(f"session_summary_{call_id}")
        if stored_summary:
            return stored_summary
        else:
            return {
                "type": "session_summary_error",
                "message": f"Session {call_id} not found in active or stored sessions"
            }
    
    session = active_sessions[call_id]
    duration = (datetime.utcnow() - session["start_time"]).total_seconds()
    
    # Calculate statistics
    risk_history = session["risk_history"]
    if risk_history:
        risks = [r["crisis_risk"] for r in risk_history]
        max_risk = max(risks)
        avg_risk = sum(risks) / len(risks)
        current_risk = risks[-1]
    else:
        max_risk = avg_risk = current_risk = 0
    
    return {
        "type": "detailed_session_summary",
        "call_id": call_id,
        "session_active": True,
        "duration_seconds": duration,
        "start_time": session["start_time"].isoformat(),
        "total_segments": len(session["segments"]),
        "total_risk_checks": len(risk_history),
        "max_crisis_risk": max_risk,
        "average_crisis_risk": avg_risk,
        "current_crisis_risk": current_risk,
        "escalation_triggered": session["escalation_triggered"],
        "caller_info": session.get("caller_info", {}),
        "last_analysis": session.get("last_analysis", {}).dict() if session.get("last_analysis") else None
    }

async def cleanup_inactive_sessions(ctx: Context):
    """Clean up sessions inactive for more than 2 hours"""
    cutoff_time = datetime.utcnow().timestamp() - 7200  # 2 hours
    
    inactive_sessions = []
    for call_id, session in active_sessions.items():
        if session["start_time"].timestamp() < cutoff_time:
            inactive_sessions.append(call_id)
    
    for call_id in inactive_sessions:
        ctx.logger.info(f"🧹 Cleaning up inactive session: {call_id}")
        del active_sessions[call_id]
    
    if inactive_sessions:
        ctx.logger.info(f"Cleaned up {len(inactive_sessions)} inactive sessions")

async def store_live_analysis_direct(ctx: Context, call_id: str, analysis, session: dict):
    """Store live analysis (helper function)"""
    from chat_protocol import store_live_analysis
    await store_live_analysis(ctx, call_id, analysis, session)

def calculate_session_risk_trend(risk_history: list) -> str:
    """Calculate overall risk trend for the session"""
    if len(risk_history) < 3:
        return "insufficient_data"
    
    risks = [r["crisis_risk"] for r in risk_history]
    
    # Compare first third to last third
    first_third = risks[:len(risks)//3]
    last_third = risks[-len(risks)//3:]
    
    avg_early = sum(first_third) / len(first_third)
    avg_late = sum(last_third) / len(last_third)
    
    if avg_late > avg_early + 15:
        return "significantly_increasing"
    elif avg_late > avg_early + 5:
        return "increasing"
    elif avg_late < avg_early - 15:
        return "significantly_decreasing"
    elif avg_late < avg_early - 5:
        return "decreasing"
    else:
        return "stable"

def agent_is_healthy() -> bool:
    """Check if the live agent is functioning properly"""
    try:
        # Test core functionality
        from sentiment_service import LiveSentimentRequest, LiveTranscriptSegment
        
        test_segment = LiveTranscriptSegment(
            text="test message for health check",
            timestamp=datetime.utcnow().timestamp(),
            confidence=0.9,
            is_final=True
        )
        
        test_request = LiveSentimentRequest(
            call_id="health_check",
            transcript_segments=[test_segment],
            session_duration=0,
            timestamp=datetime.utcnow().isoformat()
        )
        
        live_sentiment_analyzer.analyze_live_sentiment(test_request)
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

@agent.on_message(model=dict)
async def handle_health_check_message(ctx: Context, sender: str, msg: dict):
    """Handle health check requests for live agent"""
    if msg.get("type") == "health_check":
        is_healthy = agent_is_healthy()
        active_session_count = len(active_sessions)
        
        health_response = {
            "type": "health_response",
            "status": "HEALTHY" if is_healthy else "UNHEALTHY",
            "agent_name": "live_mental_health_agent",
            "agent_type": "real_time_crisis_detector",
            "active_sessions": active_session_count,
            "max_concurrent_sessions": 50,
            "core_functionality": "operational" if is_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await ctx.send(sender, health_response)

# Example integration patterns for your dashboard
@agent.on_message(model=dict)  
async def handle_deepgram_integration(ctx: Context, sender: str, msg: dict):
    """Handle Deepgram-style live transcript integration"""
    if msg.get("type") == "deepgram_live":
        # Process Deepgram live transcript format
        try:
            call_id = msg.get("call_id") or str(uuid.uuid4())
            
            # Extract Deepgram data
            transcript_data = msg.get("channel", {}).get("alternatives", [{}])[0]
            text = transcript_data.get("transcript", "")
            confidence = transcript_data.get("confidence", 0.8)
            is_final = msg.get("is_final", False)
            
            if not text.strip():
                return  # Skip empty transcripts
            
            # Start session if new
            if call_id not in active_sessions:
                await start_live_session(ctx, call_id, {
                    "source": "deepgram",
                    "channel": msg.get("channel", {})
                })
            
            # Process the segment
            segment_msg = {
                "type": "live_transcript_segment",
                "call_id": call_id,
                "text": text,
                "confidence": confidence,
                "is_final": is_final,
                "timestamp": datetime.utcnow().timestamp()
            }
            
            # Add tonality data if provided
            if "tonality" in msg:
                segment_msg["tonality"] = msg["tonality"]
            
            result = await process_live_segment(ctx, segment_msg)
            
            # Send back analysis
            await ctx.send(sender, {
                "type": "deepgram_analysis_response",
                "call_id": call_id,
                "original_message_id": msg.get("message_id"),
                "analysis": result.get("analysis", {}),
                "urgent_action_required": result.get("analysis", {}).get("escalation_trigger", False)
            })
            
        except Exception as e:
            ctx.logger.error(f"Error processing Deepgram message: {str(e)}")
            await ctx.send(sender, {
                "type": "deepgram_error",
                "message": str(e)
            })

if __name__ == "__main__":
    print("🚀 Starting Live Mental Health Sentiment Analysis Agent...")
    print(f"🔗 Agent Address: {agent.address}")
    print("🎤 Real-time transcript analysis ready")
    print("🧠 Voice tonality integration enabled")
    print("🚨 Emergency escalation system active")
    print("📊 Live dashboard integration ready")
    print("⚡ Processing live conversations for crisis detection")
    print("\n📋 Supported Message Types:")
    print("  • start_live_session - Begin monitoring a call")
    print("  • live_transcript_segment - Process transcript chunk")
    print("  • end_live_session - End call monitoring")  
    print("  • emergency_status_check - Get crisis status")
    print("  • deepgram_live - Direct Deepgram integration")
    print("  • get_live_status - Agent health and statistics")
    
    agent.run()# agent.py - Main Agent Configuration
from uagents import Agent, Context
from uagents.experimental.quota import QuotaProtocol, RateLimit
from chat_protocol import mental_health_chat, get_agent_status
from sentiment_service import sentiment_analyzer
import asyncio

# Agent configuration
agent = Agent(
    name="mental_health_sentiment_agent",
    seed="mental_health_sentiment_secret_seed_2024",  # Change this for production
    port=8001,
    mailbox=True  # Enable mailbox for Agentverse communication
)

# Rate limiting to prevent abuse (30 requests per hour per sender)
quota_protocol = QuotaProtocol(
    storage_reference=agent.storage,
    name="SentimentAnalysisQuota",
    version="1.0.0", 
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30)
)

# Include protocols
agent.include(mental_health_chat, publish_manifest=True)
agent.include(quota_protocol, publish_manifest=True)

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    """
    Initialize the agent on startup
    """
    ctx.logger.info("🧠 Mental Health Sentiment Analysis Agent Starting...")
    ctx.logger.info(f"Agent address: {ctx.agent.address}")
    
    # Initialize storage
    ctx.storage.set("agent_info", {
        "name": "Mental Health Sentiment Analyzer",
        "version": "1.0.0",
        "description": "AI agent for analyzing mental health crisis indicators in conversation transcripts",
        "capabilities": [
            "Crisis risk assessment",
            "Distress level analysis", 
            "Emotional intensity measurement",
            "Urgency classification",
            "Real-time recommendations"
        ],
        "created_at": ctx.logger.info.__name__
    })
    
    # Test the sentiment analyzer
    try:
        from sentiment_service import SentimentRequest
        test_request = SentimentRequest(
            transcript="I'm feeling okay today, just checking the system",
            timestamp="2024-01-01T00:00:00Z",
            call_id="test"
        )
        test_result = sentiment_analyzer.analyze_sentiment(test_request)
        ctx.logger.info("✅ Sentiment analyzer initialized successfully")
        ctx.logger.info(f"Test analysis completed with {test_result.urgency} urgency")
    except Exception as e:
        ctx.logger.error(f"❌ Error initializing sentiment analyzer: {str(e)}")

@agent.on_interval(period=300.0)  # Every 5 minutes
async def health_check_handler(ctx: Context):
    """
    Periodic health check and logging
    """
    try:
        status = await get_agent_status(ctx)
        ctx.logger.info(f"🔄 Health Check - Total analyses: {status.get('statistics', {}).get('total_analyses', 0)}")
        
        # Log critical alerts if any
        critical_count = status.get('statistics', {}).get('critical_alerts', 0)
        if critical_count > 0:
            ctx.logger.warning(f"⚠️ Total critical alerts detected: {critical_count}")
            
    except Exception as e:
        ctx.logger.error(f"Health check failed: {str(e)}")

@agent.on_message(model=dict)
async def handle_direct_message(ctx: Context, sender: str, msg: dict):
    """
    Handle direct API-style messages for dashboard integration
    """
    try:
        if msg.get("type") == "get_status":
            status = await get_agent_status(ctx)
            await ctx.send(sender, status)
            
        elif msg.get("type") == "analyze_transcript":
            from sentiment_service import SentimentRequest
            
            # Create analysis request
            request = SentimentRequest(
                transcript=msg.get("transcript", ""),
                timestamp=msg.get("timestamp", ""),
                call_id=msg.get("call_id", "")
            )
            
            # Perform analysis
            result = sentiment_analyzer.analyze_sentiment(request)
            
            # Store result
            await store_analysis_result(ctx, result)
            
            # Send back the analysis
            await ctx.send(sender, {
                "type": "analysis_result",
                "data": result.dict()
            })
            
            ctx.logger.info(f"Direct analysis completed for call {result.call_id}")
            
    except Exception as e:
        ctx.logger.error(f"Error handling direct message: {str(e)}")
        await ctx.send(sender, {
            "type": "error",
            "message": str(e)
        })

# Additional utility functions for dashboard integration
async def store_analysis_result(ctx: Context, result):
    """Store analysis results (imported from chat_protocol)"""
    from chat_protocol import store_analysis_result as store_func
    await store_func(ctx, result)

def agent_is_healthy() -> bool:
    """
    Check if your agent is functioning properly
    """
    try:
        # Test core functionality
        from sentiment_service import SentimentRequest
        test_request = SentimentRequest(
            transcript="test message",
            timestamp="2024-01-01T00:00:00Z", 
            call_id="health_check"
        )
        sentiment_analyzer.analyze_sentiment(test_request)
        return True
    except:
        return False

# Health monitoring protocol
@agent.on_message(model=dict)
async def handle_health_check(ctx: Context, sender: str, msg: dict):
    """Handle health check requests"""
    if msg.get("type") == "health_check":
        is_healthy = agent_is_healthy()
        status = "HEALTHY" if is_healthy else "UNHEALTHY"
        
        await ctx.send(sender, {
            "type": "health_response",
            "status": status,
            "agent_name": "mental_health_sentiment_agent",
            "timestamp": ctx.logger.info.__name__
        })

if __name__ == "__main__":
    print("🚀 Starting Mental Health Sentiment Analysis Agent...")
    print(f"Agent Address: {agent.address}")
    print("🔗 Ready to connect to Agentverse and process mental health conversations")
    print("📊 Dashboard integration ready via direct messaging")
    print("⚡ Real-time sentiment analysis for crisis detection")
    
    agent.run()