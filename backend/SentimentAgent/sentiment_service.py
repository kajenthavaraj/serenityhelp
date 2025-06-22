# sentiment_service.py - Real-time Sentiment Analysis with Tonality
from uagents import Model, Field
from typing import List, Dict, Optional
import re
import time
from datetime import datetime, timedelta

class LiveTranscriptSegment(Model):
    """Individual segment of live transcription"""
    text: str = Field(description="Transcribed text segment")
    timestamp: float = Field(description="Timestamp of this segment")
    confidence: float = Field(description="Transcription confidence (0-1)")
    is_final: bool = Field(default=False, description="Whether this segment is finalized")
    speaker_id: Optional[str] = Field(default=None, description="Speaker identifier")

class TonalityData(Model):
    """Voice tonality analysis from audio processing"""
    pitch_mean: float = Field(default=0.0, description="Average pitch (Hz)")
    pitch_variance: float = Field(default=0.0, description="Pitch variance indicating stress")
    speech_rate: float = Field(default=0.0, description="Words per minute")
    volume_level: float = Field(default=0.0, description="Average volume level")
    voice_tremor: float = Field(default=0.0, description="Voice instability (0-1)")
    pause_frequency: float = Field(default=0.0, description="Frequency of pauses")
    emotional_tone: str = Field(default="neutral", description="Detected emotional tone")
    tone_confidence: float = Field(default=0.0, description="Confidence in tone detection")

class LiveSentimentRequest(Model):
    """Real-time sentiment analysis request"""
    call_id: str = Field(description="Unique call identifier")
    transcript_segments: List[LiveTranscriptSegment] = Field(description="Live transcript segments")
    tonality_data: Optional[TonalityData] = Field(default=None, description="Voice tonality analysis")
    session_duration: float = Field(description="Total session duration in seconds")
    timestamp: str = Field(description="Request timestamp")

class RealTimeSentimentResponse(Model):
    """Real-time sentiment analysis response"""
    call_id: str
    # Core risk metrics (0-100)
    crisis_risk: int = Field(description="Immediate crisis risk percentage")
    distress_level: int = Field(description="Emotional distress percentage") 
    emotional_intensity: int = Field(description="Emotional intensity percentage")
    tonality_risk: int = Field(description="Risk based on voice patterns")
    
    # Urgency and actions
    urgency: str = Field(description="Urgency level: low, medium, high, critical, emergency")
    recommendation: str = Field(description="Immediate action recommendation")
    escalation_trigger: bool = Field(description="Whether to trigger immediate escalation")
    
    # Detection details
    key_indicators: List[str] = Field(description="Detected crisis keywords")
    tone_indicators: List[str] = Field(description="Concerning voice patterns")
    risk_trend: str = Field(description="Risk trend: increasing, stable, decreasing")
    
    # Confidence and timing
    confidence: float = Field(description="Analysis confidence (0-1)")
    analysis_timestamp: str = Field(description="When analysis was performed")
    next_check_seconds: int = Field(description="Recommended seconds until next analysis")

class RealTimeMentalHealthAnalyzer:
    def __init__(self):
        # Enhanced crisis indicators with real-time weights
        self.crisis_keywords = {
            # Immediate suicide risk
            "suicide": 60, "kill myself": 60, "end it all": 50, "take my life": 55,
            "want to die": 55, "better off dead": 50, "not worth living": 45,
            "end my life": 55, "don't want to live": 50,
            
            # Active planning
            "have a plan": 40, "going to": 30, "tonight": 25, "right now": 35,
            "about to": 40, "ready to": 35, "decided to": 40,
            
            # Methods and means
            "pills": 25, "rope": 35, "gun": 40, "bridge": 30, "jump": 30,
            "overdose": 35, "hang": 40, "cut": 20, "bleed": 25,
            
            # Self-harm
            "hurt myself": 35, "harm myself": 35, "cut myself": 30,
            "burn myself": 35, "punish myself": 25,
            
            # Despair expressions
            "hopeless": 25, "worthless": 30, "useless": 25, "burden": 30,
            "trapped": 25, "can't escape": 30, "no way out": 35,
            "pointless": 20, "meaningless": 20
        }
        
        self.distress_keywords = {
            # Emotional states
            "depressed": 20, "overwhelmed": 25, "devastated": 30, "broken": 25,
            "empty": 20, "numb": 20, "lost": 20, "alone": 15, "lonely": 15,
            "scared": 15, "terrified": 25, "panicked": 30, "anxious": 15,
            
            # Cognitive symptoms  
            "can't think": 20, "confused": 15, "foggy": 15, "lost focus": 15,
            "memory problems": 15, "can't concentrate": 20, "scattered": 15,
            
            # Physical symptoms
            "can't sleep": 15, "insomnia": 20, "exhausted": 15, "tired": 10,
            "headaches": 10, "stomach pain": 10, "chest tight": 15,
            "can't breathe": 20, "heart racing": 15
        }
        
        # Voice tonality risk indicators
        self.tonality_patterns = {
            "monotone": 20,        # Flat affect
            "trembling": 30,       # Voice instability
            "rapid_speech": 25,    # Manic or anxious
            "slow_speech": 20,     # Depression indicator
            "high_pitch": 15,      # Stress/anxiety
            "breaking_voice": 25,  # Emotional breakdown
            "whispering": 15,      # Withdrawal/shame
            "shouting": 20,        # Agitation/anger
            "frequent_pauses": 20, # Difficulty expressing
            "breathless": 25       # Panic/distress
        }
        
        # Protective factors
        self.protective_keywords = {
            "therapy": -15, "counselor": -15, "medication": -10, "doctor": -10,
            "family": -10, "support": -15, "friends": -10, "help": -5,
            "better": -15, "improving": -20, "hope": -25, "future": -15,
            "treatment": -15, "recovery": -20, "healing": -15
        }
        
        # Session tracking for trend analysis
        self.session_history = {}
        
    def analyze_live_sentiment(self, request: LiveSentimentRequest) -> RealTimeSentimentResponse:
        """
        Analyze real-time transcript and tonality for crisis indicators
        """
        # Combine all transcript text
        full_text = " ".join([seg.text for seg in request.transcript_segments if seg.is_final])
        recent_text = " ".join([seg.text for seg in request.transcript_segments[-3:]])  # Last 3 segments
        
        # Initialize scores
        crisis_score = 0
        distress_score = 0
        tonality_score = 0
        detected_keywords = []
        tone_indicators = []
        
        # Analyze text content
        crisis_score, detected_keywords = self._analyze_crisis_indicators(full_text, recent_text)
        distress_score = self._analyze_distress_level(full_text, recent_text)
        
        # Analyze tonality if available
        if request.tonality_data:
            tonality_score, tone_indicators = self._analyze_tonality(request.tonality_data)
        
        # Real-time pattern analysis
        pattern_score = self._analyze_real_time_patterns(request.transcript_segments)
        repetition_score = self._analyze_repetition_patterns(full_text)
        urgency_score = self._analyze_urgency_cues(recent_text)
        
        # Apply protective factors
        protection_adjustment = self._calculate_protective_factors(full_text)
        
        # Combine scores with weighted importance
        final_crisis_risk = min(100, max(0, 
            crisis_score + (pattern_score * 0.3) + (urgency_score * 0.5) + protection_adjustment
        ))
        final_distress = min(100, max(0, 
            distress_score + (repetition_score * 0.2) + protection_adjustment
        ))
        final_tonality_risk = min(100, tonality_score)
        
        # Calculate emotional intensity from combination
        emotional_intensity = min(100, int(
            (final_crisis_risk * 0.4) + (final_distress * 0.3) + (final_tonality_risk * 0.3)
        ))
        
        # Determine urgency and escalation
        urgency, recommendation, escalation_trigger = self._determine_real_time_urgency(
            final_crisis_risk, final_distress, final_tonality_risk, 
            detected_keywords, tone_indicators, request.session_duration
        )
        
        # Analyze trends
        risk_trend = self._analyze_risk_trend(request.call_id, final_crisis_risk)
        
        # Calculate confidence
        confidence = self._calculate_real_time_confidence(
            request.transcript_segments, request.tonality_data, detected_keywords
        )
        
        # Determine next check interval
        next_check = self._calculate_next_check_interval(urgency, final_crisis_risk)
        
        return RealTimeSentimentResponse(
            call_id=request.call_id,
            crisis_risk=int(final_crisis_risk),
            distress_level=int(final_distress), 
            emotional_intensity=emotional_intensity,
            tonality_risk=int(final_tonality_risk),
            urgency=urgency,
            recommendation=recommendation,
            escalation_trigger=escalation_trigger,
            key_indicators=detected_keywords[:10],
            tone_indicators=tone_indicators[:5],
            risk_trend=risk_trend,
            confidence=confidence,
            analysis_timestamp=datetime.utcnow().isoformat(),
            next_check_seconds=next_check
        )
    
    def _analyze_crisis_indicators(self, full_text: str, recent_text: str) -> tuple:
        """Analyze crisis keywords with recency weighting"""
        text = full_text.lower()
        recent = recent_text.lower()
        score = 0
        keywords = []
        
        for keyword, weight in self.crisis_keywords.items():
            if keyword in text:
                score += weight
                keywords.append(keyword)
                
                # Boost score if mentioned recently
                if keyword in recent:
                    score += weight * 0.5
                    
                # Check for immediate context
                if self._check_immediate_context(text, keyword):
                    score += weight * 0.3
        
        return score, keywords
    
    def _analyze_distress_level(self, full_text: str, recent_text: str) -> int:
        """Analyze emotional distress indicators"""
        text = full_text.lower()
        recent = recent_text.lower()
        score = 0
        
        for keyword, weight in self.distress_keywords.items():
            if keyword in text:
                score += weight
                if keyword in recent:
                    score += weight * 0.3
        
        return score
    
    def _analyze_tonality(self, tonality: TonalityData) -> tuple:
        """Analyze voice tonality for crisis indicators"""
        score = 0
        indicators = []
        
        # Pitch analysis
        if tonality.pitch_variance > 50:  # High pitch variance = stress
            score += 25
            indicators.append("voice_instability")
        
        if tonality.pitch_mean > 300:  # Very high pitch = anxiety/panic
            score += 20
            indicators.append("high_stress_pitch")
        
        # Speech rate analysis
        if tonality.speech_rate > 200:  # Very fast = mania/anxiety
            score += 20
            indicators.append("rapid_speech")
        elif tonality.speech_rate < 80:  # Very slow = depression
            score += 15
            indicators.append("slow_speech")
        
        # Voice tremor
        if tonality.voice_tremor > 0.3:
            score += int(tonality.voice_tremor * 50)
            indicators.append("trembling_voice")
        
        # Pause frequency
        if tonality.pause_frequency > 0.4:  # Many pauses = difficulty
            score += 20
            indicators.append("frequent_pauses")
        
        # Volume analysis
        if tonality.volume_level < 0.2:  # Very quiet = withdrawal
            score += 15
            indicators.append("withdrawn_voice")
        elif tonality.volume_level > 0.8:  # Very loud = agitation
            score += 10
            indicators.append("agitated_voice")
        
        # Emotional tone
        tone_risks = {
            "distressed": 30, "panicked": 40, "depressed": 25,
            "angry": 20, "fearful": 25, "hopeless": 35
        }
        
        if tonality.emotional_tone in tone_risks:
            tone_score = tone_risks[tonality.emotional_tone]
            score += int(tone_score * tonality.tone_confidence)
            indicators.append(f"tone_{tonality.emotional_tone}")
        
        return score, indicators
    
    def _analyze_real_time_patterns(self, segments: List[LiveTranscriptSegment]) -> int:
        """Analyze patterns in real-time speech"""
        if len(segments) < 3:
            return 0
        
        score = 0
        
        # Check for escalating language
        recent_segments = segments[-3:]
        crisis_mentions = 0
        
        for segment in recent_segments:
            for keyword in self.crisis_keywords.keys():
                if keyword in segment.text.lower():
                    crisis_mentions += 1
        
        if crisis_mentions >= 2:  # Multiple crisis mentions recently
            score += 30
        
        # Check for repetitive distress
        recent_text = " ".join([seg.text for seg in recent_segments])
        if self._check_repetitive_distress(recent_text):
            score += 20
        
        # Check for deteriorating coherence
        if self._check_coherence_decline(segments):
            score += 15
        
        return score
    
    def _analyze_repetition_patterns(self, text: str) -> int:
        """Analyze repetitive speech patterns"""
        words = text.lower().split()
        if len(words) < 20:
            return 0
        
        # Count negative word repetition
        negative_words = ["can't", "won't", "never", "nothing", "nobody", "no", "not"]
        negative_count = sum(1 for word in words if word in negative_words)
        
        score = 0
        negative_ratio = negative_count / len(words)
        
        if negative_ratio > 0.15:  # >15% negative words
            score += 25
        elif negative_ratio > 0.10:  # >10% negative words  
            score += 15
        
        return score
    
    def _analyze_urgency_cues(self, recent_text: str) -> int:
        """Analyze urgency indicators in recent speech"""
        text = recent_text.lower()
        urgency_phrases = [
            "right now", "immediately", "can't wait", "have to", "need to",
            "tonight", "today", "this minute", "urgent", "emergency"
        ]
        
        score = 0
        for phrase in urgency_phrases:
            if phrase in text:
                score += 20
        
        return min(60, score)  # Cap urgency boost
    
    def _calculate_protective_factors(self, text: str) -> int:
        """Calculate protective factor adjustments"""
        adjustment = 0
        text_lower = text.lower()
        
        for keyword, value in self.protective_keywords.items():
            if keyword in text_lower:
                adjustment += value
        
        return adjustment
    
    def _determine_real_time_urgency(self, crisis_risk: int, distress: int, tonality_risk: int,
                                   keywords: List[str], tone_indicators: List[str], 
                                   duration: float) -> tuple:
        """Determine urgency level for real-time response"""
        
        # Emergency: Immediate suicide intent
        emergency_keywords = ["kill myself", "suicide", "end it all", "going to die", "about to"]
        if (crisis_risk >= 60 or 
            any(word in emergency_keywords for word in keywords) or
            ("voice_instability" in tone_indicators and crisis_risk >= 40)):
            return ("emergency", 
                   "🚨 EMERGENCY: Immediate crisis intervention required. Contact emergency services.",
                   True)
        
        # Critical: High immediate risk
        if (crisis_risk >= 45 or 
            (crisis_risk >= 30 and tonality_risk >= 40) or
            any(word in ["hurt myself", "have a plan", "ready to"] for word in keywords)):
            return ("critical",
                   "🔴 CRITICAL: Transfer to crisis specialist immediately. Escalate within 30 seconds.",
                   True)
        
        # High: Significant concern
        if (crisis_risk >= 30 or distress >= 60 or tonality_risk >= 50 or
            (crisis_risk >= 20 and len(keywords) >= 3)):
            return ("high",
                   "🟠 HIGH PRIORITY: Transfer to human counselor within 1-2 minutes.",
                   False)
        
        # Medium: Monitor closely
        if (crisis_risk >= 15 or distress >= 40 or tonality_risk >= 30):
            return ("medium",
                   "🟡 MONITOR: Prepare for potential escalation. Human backup ready.",
                   False)
        
        # Low: Continue monitoring
        return ("low",
               "🟢 CONTINUE: AI conversation with enhanced monitoring.",
               False)
    
    def _analyze_risk_trend(self, call_id: str, current_risk: int) -> str:
        """Analyze risk trend over time"""
        if call_id not in self.session_history:
            self.session_history[call_id] = []
        
        history = self.session_history[call_id]
        history.append({
            "risk": current_risk,
            "timestamp": time.time()
        })
        
        # Keep last 10 measurements
        if len(history) > 10:
            history = history[-10:]
            self.session_history[call_id] = history
        
        if len(history) < 3:
            return "insufficient_data"
        
        # Calculate trend
        recent = [h["risk"] for h in history[-3:]]
        if recent[-1] > recent[0] + 10:
            return "increasing"
        elif recent[-1] < recent[0] - 10:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_real_time_confidence(self, segments: List[LiveTranscriptSegment], 
                                      tonality: Optional[TonalityData], 
                                      keywords: List[str]) -> float:
        """Calculate confidence in real-time analysis"""
        confidence = 0.4  # Base confidence
        
        # More final segments = higher confidence
        final_segments = sum(1 for seg in segments if seg.is_final)
        if final_segments > 5:
            confidence += 0.2
        
        # High transcription confidence
        avg_transcription_confidence = sum(seg.confidence for seg in segments) / len(segments)
        confidence += avg_transcription_confidence * 0.2
        
        # Tonality data available
        if tonality and tonality.tone_confidence > 0.5:
            confidence += 0.15
        
        # Strong keyword indicators
        if len(keywords) >= 3:
            confidence += 0.15
        
        return min(1.0, confidence)
    
    def _calculate_next_check_interval(self, urgency: str, crisis_risk: int) -> int:
        """Calculate when to perform next analysis"""
        intervals = {
            "emergency": 5,    # Every 5 seconds
            "critical": 10,    # Every 10 seconds
            "high": 15,        # Every 15 seconds
            "medium": 30,      # Every 30 seconds
            "low": 60          # Every minute
        }
        
        base_interval = intervals.get(urgency, 60)
        
        # Adjust based on risk level
        if crisis_risk > 50:
            return min(base_interval, 10)
        elif crisis_risk > 30:
            return min(base_interval, 20)
        
        return base_interval
    
    def _check_immediate_context(self, text: str, keyword: str) -> bool:
        """Check for immediate threat context"""
        immediate_indicators = ["right now", "today", "tonight", "immediately", "about to", "going to"]
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return False
        
        context = text[max(0, keyword_pos-50):keyword_pos+50]
        return any(indicator in context for indicator in immediate_indicators)
    
    def _check_repetitive_distress(self, text: str) -> bool:
        """Check for repetitive distress expressions"""
        distress_words = ["can't", "won't", "never", "hopeless", "worthless"]
        count = sum(text.lower().count(word) for word in distress_words)
        return count >= 3
    
    def _check_coherence_decline(self, segments: List[LiveTranscriptSegment]) -> bool:
        """Check if speech coherence is declining"""
        if len(segments) < 5:
            return False
        
        # Simple heuristic: recent segments getting shorter and less confident
        recent = segments[-3:]
        earlier = segments[-6:-3] if len(segments) >= 6 else segments[:3]
        
        recent_avg_length = sum(len(seg.text.split()) for seg in recent) / len(recent)
        earlier_avg_length = sum(len(seg.text.split()) for seg in earlier) / len(earlier)
        
        recent_avg_confidence = sum(seg.confidence for seg in recent) / len(recent)
        earlier_avg_confidence = sum(seg.confidence for seg in earlier) / len(earlier)
        
        return (recent_avg_length < earlier_avg_length * 0.7 and 
                recent_avg_confidence < earlier_avg_confidence * 0.8)

# Initialize the real-time analyzer
live_sentiment_analyzer = RealTimeMentalHealthAnalyzer()