# sentiment_service.py - Core Functionality
from uagents import Model, Field
from typing import List, Dict
import re

class SentimentRequest(Model):
    transcript: str = Field(description="The conversation transcript from Deepgram")
    timestamp: str = Field(description="Timestamp of the conversation")
    call_id: str = Field(description="Unique identifier for the call")

class SentimentResponse(Model):
    call_id: str
    distress_level: int = Field(description="Distress percentage (0-100)")
    crisis_risk: int = Field(description="Crisis risk percentage (0-100)")
    emotional_intensity: int = Field(description="Emotional intensity percentage (0-100)")
    urgency: str = Field(description="Urgency level: low, medium, high, critical")
    recommendation: str = Field(description="Action recommendation")
    key_indicators: List[str] = Field(description="Detected concerning keywords")
    confidence: float = Field(description="Analysis confidence score")

class MentalHealthSentimentAnalyzer:
    def __init__(self):
        # Crisis indicators with severity weights
        self.crisis_keywords = {
            # Immediate danger
            "suicide": 50, "kill myself": 50, "end it all": 45, "not worth living": 40,
            "better off dead": 45, "want to die": 50, "ending my life": 50,
            "plan to": 30, "going to hurt": 35, "can't go on": 35,
            
            # Self-harm
            "hurt myself": 30, "self harm": 30, "cutting": 25, "overdose": 40,
            "pills": 20, "jump off": 35, "hang myself": 50,
            
            # Violent ideation
            "hurt someone": 35, "violence": 20, "revenge": 15
        }
        
        self.distress_keywords = {
            # Emotional states
            "hopeless": 20, "worthless": 25, "empty": 15, "numb": 15,
            "alone": 10, "trapped": 20, "burden": 25, "useless": 20,
            "depressed": 15, "anxious": 10, "overwhelmed": 15, "broken": 20,
            "lost": 15, "desperate": 25, "miserable": 20, "devastated": 25,
            
            # Cognitive indicators
            "can't think": 15, "confused": 10, "foggy": 10, "scattered": 10,
            "racing thoughts": 15, "can't focus": 10, "memory problems": 10,
            
            # Physical symptoms
            "can't sleep": 10, "exhausted": 10, "tired": 5, "headaches": 5,
            "stomach problems": 5, "chest pain": 10, "breathing": 10
        }
        
        self.intensity_keywords = {
            # Emotional intensity
            "screaming": 25, "crying": 15, "sobbing": 20, "shaking": 15,
            "panic": 25, "terrified": 20, "furious": 20, "rage": 25,
            "angry": 10, "livid": 20, "explosive": 25, "meltdown": 20,
            
            # Physical manifestations
            "heart racing": 15, "sweating": 10, "trembling": 15,
            "hyperventilating": 20, "dizzy": 10, "nauseous": 10
        }
        
        # Protective factors (reduce scores)
        self.protective_keywords = {
            "family": -5, "support": -10, "therapy": -15, "medication": -10,
            "counselor": -15, "doctor": -10, "help": -5, "better": -10,
            "improving": -15, "hope": -20, "future": -10, "goals": -10
        }
    
    def analyze_sentiment(self, request: SentimentRequest) -> SentimentResponse:
        """
        Analyze the transcript for mental health indicators
        """
        text = request.transcript.lower()
        
        # Initialize scores
        crisis_score = 0
        distress_score = 0
        intensity_score = 0
        detected_keywords = []
        
        # Analyze crisis indicators
        for keyword, weight in self.crisis_keywords.items():
            if keyword in text:
                crisis_score += weight
                detected_keywords.append(keyword)
                
                # Context-aware scoring
                if self._check_immediate_context(text, keyword):
                    crisis_score += weight * 0.5  # Boost for immediate context
        
        # Analyze distress indicators
        for keyword, weight in self.distress_keywords.items():
            if keyword in text:
                distress_score += weight
                if keyword not in detected_keywords:
                    detected_keywords.append(keyword)
        
        # Analyze emotional intensity
        for keyword, weight in self.intensity_keywords.items():
            if keyword in text:
                intensity_score += weight
                if keyword not in detected_keywords:
                    detected_keywords.append(keyword)
        
        # Apply protective factors
        for keyword, adjustment in self.protective_keywords.items():
            if keyword in text:
                crisis_score = max(0, crisis_score + adjustment)
                distress_score = max(0, distress_score + adjustment)
                intensity_score = max(0, intensity_score + adjustment)
        
        # Apply additional context analysis
        crisis_score += self._analyze_sentence_structure(text)
        distress_score += self._analyze_repetition(text)
        intensity_score += self._analyze_punctuation(text)
        
        # Normalize scores to 0-100
        crisis_risk = min(100, crisis_score)
        distress_level = min(100, distress_score)
        emotional_intensity = min(100, intensity_score)
        
        # Determine urgency and recommendations
        urgency, recommendation = self._determine_urgency(
            crisis_risk, distress_level, emotional_intensity, detected_keywords
        )
        
        # Calculate confidence based on number of indicators
        confidence = self._calculate_confidence(detected_keywords, text)
        
        return SentimentResponse(
            call_id=request.call_id,
            distress_level=distress_level,
            crisis_risk=crisis_risk,
            emotional_intensity=emotional_intensity,
            urgency=urgency,
            recommendation=recommendation,
            key_indicators=detected_keywords[:10],  # Limit to top 10
            confidence=confidence
        )
    
    def _check_immediate_context(self, text: str, keyword: str) -> bool:
        """Check for immediate context indicators like 'right now', 'today', etc."""
        immediate_indicators = ["right now", "today", "tonight", "immediately", "about to"]
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return False
        
        # Check 50 characters around the keyword
        context = text[max(0, keyword_pos-50):keyword_pos+50]
        return any(indicator in context for indicator in immediate_indicators)
    
    def _analyze_sentence_structure(self, text: str) -> int:
        """Analyze sentence patterns that might indicate crisis"""
        crisis_patterns = [
            r"i\s+(can't|cannot)\s+(take|handle|do)\s+this",
            r"nobody\s+(cares|would miss me)",
            r"nothing\s+(matters|helps)",
            r"i\s+have\s+(no|nothing)",
            r"everyone\s+would\s+be\s+better"
        ]
        
        score = 0
        for pattern in crisis_patterns:
            if re.search(pattern, text):
                score += 15
        
        return score
    
    def _analyze_repetition(self, text: str) -> int:
        """Analyze repetitive phrases that might indicate rumination"""
        words = text.split()
        if len(words) < 10:
            return 0
        
        # Look for repetitive negative patterns
        negative_words = ["can't", "won't", "never", "nothing", "nobody", "no one"]
        negative_count = sum(1 for word in words if word in negative_words)
        
        if negative_count > len(words) * 0.1:  # More than 10% negative words
            return 20
        elif negative_count > len(words) * 0.05:  # More than 5% negative words
            return 10
        
        return 0
    
    def _analyze_punctuation(self, text: str) -> int:
        """Analyze punctuation patterns for emotional intensity"""
        exclamation_count = text.count('!')
        question_count = text.count('?')
        ellipsis_count = text.count('...')
        
        score = 0
        if exclamation_count > 3:
            score += 15
        if question_count > 5:
            score += 10
        if ellipsis_count > 2:
            score += 10
        
        return score
    
    def _determine_urgency(self, crisis_risk: int, distress_level: int, 
                          emotional_intensity: int, keywords: List[str]) -> tuple:
        """Determine urgency level and recommendation"""
        
        # Critical: Immediate transfer needed
        if crisis_risk >= 50 or any(word in ["suicide", "kill myself", "end it all"] for word in keywords):
            return "critical", "IMMEDIATE TRANSFER - Crisis intervention needed. Activate emergency protocols."
        
        # High: Transfer within 2 minutes
        elif (crisis_risk >= 30 or distress_level >= 70 or emotional_intensity >= 80 or
              any(word in ["hurt myself", "not worth living", "better off dead"] for word in keywords)):
            return "high", "Transfer to human counselor within 2 minutes. Prepare crisis resources."
        
        # Medium: Monitor closely
        elif (crisis_risk >= 15 or distress_level >= 40 or emotional_intensity >= 60):
            return "medium", "Monitor closely and prepare for potential transfer. Have human counselor on standby."
        
        # Low: Continue with AI
        else:
            return "low", "Continue AI conversation with enhanced monitoring. Check-in every 5 minutes."
    
    def _calculate_confidence(self, keywords: List[str], text: str) -> float:
        """Calculate confidence score based on analysis quality"""
        base_confidence = 0.5
        
        # More keywords = higher confidence
        keyword_boost = min(0.3, len(keywords) * 0.05)
        
        # Longer text = higher confidence
        text_length_boost = min(0.15, len(text.split()) / 1000)
        
        # Specific high-confidence indicators
        high_conf_indicators = ["suicide", "kill myself", "hurt myself", "overdose"]
        high_conf_boost = 0.05 * sum(1 for word in keywords if word in high_conf_indicators)
        
        confidence = base_confidence + keyword_boost + text_length_boost + high_conf_boost
        return min(1.0, confidence)

# Initialize the analyzer
sentiment_analyzer = MentalHealthSentimentAnalyzer()