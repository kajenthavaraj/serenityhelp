# chat_protocol.py - Natural Language Interface
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement, 
    ChatMessage, 
    TextContent,
    chat_protocol_spec
)
from sentiment_service import SentimentRequest, SentimentResponse, sentiment_analyzer
import json
import uuid
from datetime import datetime

# Create the chat protocol
mental_health_chat = Protocol(spec=chat_protocol_spec)

@mental_health_chat.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle incoming chat messages and perform sentiment analysis
    """
    try:
        # Extract text content from the message
        text_content = ""
        for item in msg.content:
            if isinstance(item, TextContent):
                text_content += item.text + " "
        
        text_content = text_content.strip()
        
        if not text_content:
            await ctx.send(
                sender,
                ChatAcknowledgement(
                    timestamp=datetime.utcnow().isoformat(),
                    acknowledged_msg_id=msg.msg_id
                )
            )
            return
        
        # Log the received message
        ctx.logger.info(f"Analyzing transcript: {text_content[:100]}...")
        
        # Create sentiment analysis request
        request = SentimentRequest(
            transcript=text_content,
            timestamp=datetime.utcnow().isoformat(),
            call_id=str(uuid.uuid4())
        )
        
        # Perform sentiment analysis
        analysis_result = sentiment_analyzer.analyze_sentiment(request)
        
        # Create response message
        response_text = create_analysis_response(analysis_result)
        
        # Send acknowledgment
        await ctx.send(
            sender,
            ChatAcknowledgement(
                timestamp=datetime.utcnow().isoformat(),
                acknowledged_msg_id=msg.msg_id
            )
        )
        
        # Send analysis result
        await ctx.send(
            sender,
            ChatMessage(
                msg_id=str(uuid.uuid4()),
                timestamp=datetime.utcnow().isoformat(),
                content=[TextContent(text=response_text)],
                conversation_id=msg.conversation_id
            )
        )
        
        # Log results for monitoring
        ctx.logger.info(f"Analysis completed for call {analysis_result.call_id}")
        ctx.logger.info(f"Urgency: {analysis_result.urgency}, Crisis Risk: {analysis_result.crisis_risk}%")
        
        # Store in agent storage for dashboard integration
        await store_analysis_result(ctx, analysis_result)
        
    except Exception as e:
        ctx.logger.error(f"Error processing chat message: {str(e)}")
        
        # Send error acknowledgment
        await ctx.send(
            sender,
            ChatAcknowledgement(
                timestamp=datetime.utcnow().isoformat(),
                acknowledged_msg_id=msg.msg_id
            )
        )

def create_analysis_response(result: SentimentResponse) -> str:
    """
    Create a formatted response for the analysis
    """
    # Create urgency indicator
    urgency_emoji = {
        "low": "🟢",
        "medium": "🟡", 
        "high": "🟠",
        "critical": "🔴"
    }
    
    response = f"""
🧠 **Mental Health Sentiment Analysis Report**

**Call ID:** {result.call_id}
**Urgency Level:** {urgency_emoji.get(result.urgency, '⚪')} {result.urgency.upper()}

**Risk Assessment:**
• Crisis Risk: {result.crisis_risk}%
• Distress Level: {result.distress_level}%  
• Emotional Intensity: {result.emotional_intensity}%
• Confidence: {result.confidence:.1%}

**Recommendation:**
{result.recommendation}
"""

    if result.key_indicators:
        response += f"\n**Detected Indicators:**\n"
        for indicator in result.key_indicators:
            response += f"• {indicator}\n"
    
    if result.urgency == "critical":
        response += "\n⚠️ **CRITICAL ALERT**: Immediate human intervention required!"
    elif result.urgency == "high":
        response += "\n⚠️ **HIGH PRIORITY**: Transfer to counselor recommended"
    
    response += f"\n**JSON Data for Integration:**\n```json\n{json.dumps(result.dict(), indent=2)}\n```"
    
    return response

async def store_analysis_result(ctx: Context, result: SentimentResponse):
    """
    Store analysis results for dashboard integration
    """
    try:
        # Store the latest analysis
        ctx.storage.set("latest_analysis", result.dict())
        
        # Store in history (keep last 100 analyses)
        history_key = "analysis_history"
        history = ctx.storage.get(history_key) or []
        
        history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "result": result.dict()
        })
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        ctx.storage.set(history_key, history)
        
        # Update statistics
        update_statistics(ctx, result)
        
    except Exception as e:
        ctx.logger.error(f"Error storing analysis result: {str(e)}")

def update_statistics(ctx: Context, result: SentimentResponse):
    """
    Update running statistics for monitoring
    """
    try:
        stats = ctx.storage.get("statistics") or {
            "total_analyses": 0,
            "critical_alerts": 0,
            "high_priority": 0,
            "average_crisis_risk": 0,
            "average_distress": 0
        }
        
        # Update counts
        stats["total_analyses"] += 1
        if result.urgency == "critical":
            stats["critical_alerts"] += 1
        elif result.urgency == "high":
            stats["high_priority"] += 1
        
        # Update running averages
        total = stats["total_analyses"]
        stats["average_crisis_risk"] = (
            (stats["average_crisis_risk"] * (total - 1) + result.crisis_risk) / total
        )
        stats["average_distress"] = (
            (stats["average_distress"] * (total - 1) + result.distress_level) / total
        )
        
        ctx.storage.set("statistics", stats)
        
    except Exception as e:
        ctx.logger.error(f"Error updating statistics: {str(e)}")

# Health check endpoint for monitoring
async def get_agent_status(ctx: Context) -> dict:
    """
    Get current agent status and statistics
    """
    stats = ctx.storage.get("statistics") or {}
    latest = ctx.storage.get("latest_analysis")
    
    return {
        "status": "healthy",
        "statistics": stats,
        "latest_analysis": latest,
        "timestamp": datetime.utcnow().isoformat()
    }