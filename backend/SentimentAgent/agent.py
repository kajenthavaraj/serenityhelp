# agent.py - Main Agent Configuration
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