
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from datetime import datetime
import json
import logging
import requests
from typing import Dict, List, Any
import uuid

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key for authentication (flexible - works with or without)
API_KEY = os.environ.get('API_KEY', 'hackathon_2024_ai_honeypot_secure_key')

# GUVI Callback endpoint
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# ==================== SCAM DETECTION ENGINE ====================

class ScamDetector:
    """Advanced scam message detection using pattern matching"""
    
    SCAM_PATTERNS = {
        'urgency': [
            r'urgent', r'immediately', r'right now', r'asap', r'limited time',
            r'act now', r'expires', r'hurry', r'last chance', r'time sensitive', 
            r'today', r'now', r'quick'
        ],
        'threats': [
            r'blocked', r'suspended', r'deactivated', r'terminated', r'cancelled',
            r'legal action', r'arrest', r'lawsuit', r'fraud', r'unauthorized',
            r'suspicious activity', r'security alert', r'freeze', r'close',
            r'locked', r'disabled', r'restricted'
        ],
        'financial': [
            r'won', r'prize', r'lottery', r'jackpot', r'reward', r'refund',
            r'tax refund', r'inheritance', r'compensation', r'claim',
            r'transfer', r'payment', r'credit', r'deposit', r'wire', r'upi',
            r'rupees', r'rs\.', r'₹', r'dollars', r'\$', r'amount', r'pay'
        ],
        'personal_info': [
            r'verify', r'confirm', r'update', r'validate', r'authenticate',
            r'click here', r'link', r'account details', r'password', r'pin',
            r'otp', r'cvv', r'card number', r'social security', r'aadhar', 
            r'share', r'provide', r'send', r'submit'
        ],
        'too_good': [
            r'free', r'guaranteed', r'no risk', r'100%', r'amazing offer',
            r'exclusive', r'selected', r'chosen', r'congratulations',
            r'winner', r'lucky'
        ],
        'impersonation': [
            r'bank', r'government', r'irs', r'income tax', r'police',
            r'court', r'customs', r'delivery', r'fedex', r'dhl',
            r'amazon', r'flipkart', r'paytm', r'phonepe', r'google pay',
            r'sbi', r'hdfc', r'icici', r'axis'
        ]
    }
    
    def calculate_scam_score(self, message: str) -> float:
        """Calculate scam probability score (0-1)"""
        if not message:
            return 0.0
            
        message_lower = message.lower()
        total_score = 0.0
        max_score = 0.0
        
        category_weights = {
            'urgency': 0.15,
            'threats': 0.25,
            'financial': 0.20,
            'personal_info': 0.20,
            'too_good': 0.10,
            'impersonation': 0.10
        }
        
        for category, patterns in self.SCAM_PATTERNS.items():
            weight = category_weights.get(category, 0.1)
            max_score += weight
            
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    total_score += weight
                    break
        
        score = total_score / max_score if max_score > 0 else 0.0
        
        # Bonus checks
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message):
            score += 0.15
        
        if re.search(r'\+?\d{10,}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', message):
            score += 0.05
        
        return min(score, 1.0)
    
    def is_scam(self, message: str, threshold: float = 0.25) -> bool:
        """Determine if message is a scam"""
        score = self.calculate_scam_score(message)
        return score >= threshold
    
    def extract_suspicious_keywords(self, message: str) -> List[str]:
        """Extract suspicious keywords found in message"""
        if not message:
            return []
            
        keywords = []
        message_lower = message.lower()
        
        for category, patterns in self.SCAM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    # Clean up the pattern for display
                    clean_pattern = pattern.replace(r'\b', '').replace(r'\\', '').replace(r'\.', '.')
                    keywords.append(clean_pattern)
        
        return list(set(keywords))[:15]  # Return unique, max 15


# ==================== HONEY-POT CONVERSATION ENGINE ====================

class HoneyPotAgent:
    """Intelligent agent that engages scammers and extracts information"""
    
    def extract_intelligence(self, message: str) -> Dict[str, List[str]]:
        """Extract all valuable information from scammer's message"""
        if not message:
            return {
                'phoneNumbers': [],
                'upiIds': [],
                'phishingLinks': [],
                'bankAccounts': [],
                'suspiciousKeywords': []
            }
            
        intel = {
            'phoneNumbers': [],
            'upiIds': [],
            'phishingLinks': [],
            'bankAccounts': [],
            'suspiciousKeywords': []
        }
        
        # Extract phone numbers (various formats)
        phones = re.findall(r'\+?\d[\d\s\-\.]{8,}\d', message)
        phones += re.findall(r'\b\d{10}\b', message)
        if phones:
            intel['phoneNumbers'] = list(set([p.replace(' ', '').replace('-', '').replace('.', '') for p in phones]))
        
        # Extract UPI IDs
        upi_ids = re.findall(r'\b[a-zA-Z0-9._-]+@[a-zA-Z]+\b', message)
        if upi_ids:
            intel['upiIds'] = list(set(upi_ids))
        
        # Extract URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        urls += re.findall(r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', message)
        if urls:
            intel['phishingLinks'] = list(set(urls))
        
        # Extract bank account numbers (9-18 digits)
        bank_accounts = re.findall(r'\b\d{9,18}\b', message)
        # Extract IFSC codes
        ifsc = re.findall(r'\b[A-Z]{4}0[A-Z0-9]{6}\b', message)
        if bank_accounts or ifsc:
            intel['bankAccounts'] = list(set(bank_accounts + ifsc))
        
        return intel
    
    def generate_response(self, message: str, turn_number: int, history: List[Dict]) -> str:
        """Generate realistic victim response to keep scammer engaged"""
        
        if not message:
            return "Hello, can you please explain what this is about?"
            
        message_lower = message.lower()
        
        # Turn 1: Show interest and concern
        if turn_number == 1:
            if any(word in message_lower for word in ['block', 'suspend', 'deactivate', 'freeze']):
                return "Why will my account be blocked?"
            elif any(word in message_lower for word in ['won', 'prize', 'lottery', 'congratulations']):
                return "Really? How do I claim it?"
            elif any(word in message_lower for word in ['verify', 'confirm', 'update']):
                return "How do I verify this? What information do you need?"
            elif any(word in message_lower for word in ['payment', 'refund', 'tax']):
                return "A refund? Can you tell me more about this?"
            else:
                return "Can you please explain what this is about?"
        
        # Turn 2: Ask for specifics to extract info
        elif turn_number == 2:
            if any(word in message_lower for word in ['click', 'link', 'website', 'url']):
                return "I'm worried about clicking links. Can you give me more details first? What's the website address?"
            elif any(word in message_lower for word in ['call', 'contact', 'phone']):
                return "What number should I call? What's your name and employee ID?"
            elif any(word in message_lower for word in ['upi', 'payment', 'send', 'transfer']):
                return "Where should I send the payment? What's your UPI ID or account number?"
            elif any(word in message_lower for word in ['share', 'provide', 'submit']):
                return "What exactly do I need to share? Can you provide your official details first?"
            else:
                return "Can you give me your official contact information?"
        
        # Turn 3: Pretend to be cautious but willing
        elif turn_number == 3:
            if any(word in message_lower for word in ['account', 'bank', 'number']):
                return "I want to help but I'm nervous. What's your company name, employee ID, and callback number?"
            else:
                return "Can you provide your supervisor's name and direct phone number for verification?"
        
        # Turn 4: Ask about payment/process
        elif turn_number == 4:
            if any(word in message_lower for word in ['pay', 'fee', 'charge', 'amount', 'rs', 'rupees']):
                return "How much do I need to pay? What's your bank account or UPI ID? Is there a reference number?"
            else:
                return "What's the next step? How long will this take? Can you send me written confirmation?"
        
        # Turn 5+: Stall for more intelligence
        else:
            responses = [
                "Can you send me an official email with all the details? What's your email address?",
                "My family wants everything in writing. What's your office address and company registration number?",
                "I need to verify this with your supervisor. What's their name and direct contact?",
                "Which branch or office are you calling from? What's the customer service number I can verify?",
                "Before I proceed, can you provide the official website and helpline number?"
            ]
            idx = min(turn_number - 5, len(responses) - 1)
            return responses[idx]


# ==================== INITIALIZE SERVICES ====================

scam_detector = ScamDetector()
honeypot_agent = HoneyPotAgent()

# Store conversation sessions
conversation_sessions = {}


# ==================== HELPER FUNCTIONS ====================

def send_final_result_to_guvi(session_data: Dict):
    """Send final intelligence report to GUVI evaluation endpoint"""
    try:
        session_id = session_data['session_id']
        
        # Aggregate all extracted intelligence
        all_intel = {
            'phoneNumbers': list(session_data['extracted_intel']['phoneNumbers']),
            'upiIds': list(session_data['extracted_intel']['upiIds']),
            'phishingLinks': list(session_data['extracted_intel']['phishingLinks']),
            'bankAccounts': list(session_data['extracted_intel']['bankAccounts']),
            'suspiciousKeywords': list(session_data['extracted_intel']['suspiciousKeywords'])
        }
        
        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": session_data['turn_number'],
            "extractedIntelligence": all_intel,
            "agentNotes": session_data.get('agent_notes', 'Scam detected and intelligence extracted successfully')
        }
        
        logger.info(f"Sending final result to GUVI for session {session_id}")
        
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
        
        logger.info(f"GUVI callback response: {response.status_code}")
        
    except Exception as e:
        logger.error(f"Error sending to GUVI: {str(e)}")


# ==================== API ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Honey-Pot Scam Detection API',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_message():
    """
    Main endpoint for scam detection and honey-pot conversation
    Following GUVI hackathon requirements
    
    Request format:
    {
        "sessionId": "unique-session-id",
        "message": {
            "sender": "scammer",
            "text": "Message content",
            "timestamp": "2026-01-21T10:15:30Z"
        },
        "conversationHistory": [],
        "metadata": {...}
    }
    
    Response format:
    {
        "status": "success",
        "reply": "Agent's response"
    }
    """
    try:
        # FLEXIBLE API key authentication - works with or without
        api_key = request.headers.get('x-api-key')
        # Only reject if key is provided but WRONG
        if api_key and api_key != API_KEY:
            logger.warning(f"Invalid API key provided: {api_key}")
            return jsonify({
                'status': 'error',
                'message': 'Invalid API key'
            }), 401
        
        # Get request data - FLEXIBLE validation
        data = request.get_json()
        
        if not data:
            logger.error("Empty request body")
            return jsonify({
                'status': 'error',
                'message': 'Request body is required'
            }), 400
        
        # Extract fields with DEFAULTS for missing values
        session_id = data.get('sessionId')
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:12]}"
            logger.info(f"Generated session ID: {session_id}")
        
        message_obj = data.get('message', {})
        conversation_history = data.get('conversationHistory', [])
        metadata = data.get('metadata', {})
        
        # Extract message text - THIS is the only required field
        message_text = message_obj.get('text', '')
        
        if not message_text:
            logger.error("Missing message.text")
            return jsonify({
                'status': 'error',
                'message': 'message.text is required'
            }), 400
        
        # Get other message fields with defaults
        sender = message_obj.get('sender', 'scammer')
        timestamp = message_obj.get('timestamp', datetime.utcnow().isoformat())
        
        logger.info(f"Processing session {session_id}: {message_text[:100]}")
        
        # Detect if message is a scam
        is_scam = scam_detector.is_scam(message_text)
        scam_score = scam_detector.calculate_scam_score(message_text)
        
        logger.info(f"Scam detection: {is_scam} (score: {scam_score:.3f})")
        
        # Get or create session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = {
                'session_id': session_id,
                'messages': [],
                'extracted_intel': {
                    'phoneNumbers': set(),
                    'upiIds': set(),
                    'phishingLinks': set(),
                    'bankAccounts': set(),
                    'suspiciousKeywords': set()
                },
                'turn_number': 0,
                'is_scam': False,
                'agent_notes': ''
            }
        
        session = conversation_sessions[session_id]
        
        # If scam detected OR session already flagged as scam, activate agent
        if is_scam or session['is_scam']:
            session['is_scam'] = True
            
            # Store scammer message
            session['messages'].append({
                'sender': sender,
                'text': message_text,
                'timestamp': timestamp
            })
            session['turn_number'] += 1
            
            # Extract intelligence from this message
            intel = honeypot_agent.extract_intelligence(message_text)
            
            # Merge with existing intelligence
            for key, values in intel.items():
                if key in session['extracted_intel'] and values:
                    session['extracted_intel'][key].update(values)
            
            # Extract suspicious keywords
            keywords = scam_detector.extract_suspicious_keywords(message_text)
            if keywords:
                session['extracted_intel']['suspiciousKeywords'].update(keywords)
            
            # Generate agent response
            agent_reply = honeypot_agent.generate_response(
                message_text,
                session['turn_number'],
                conversation_history
            )
            
            # Store agent response
            session['messages'].append({
                'sender': 'user',
                'text': agent_reply,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Update agent notes with intelligence summary
            intel_summary = []
            if session['extracted_intel']['phoneNumbers']:
                intel_summary.append(f"{len(session['extracted_intel']['phoneNumbers'])} phone numbers")
            if session['extracted_intel']['upiIds']:
                intel_summary.append(f"{len(session['extracted_intel']['upiIds'])} UPI IDs")
            if session['extracted_intel']['phishingLinks']:
                intel_summary.append(f"{len(session['extracted_intel']['phishingLinks'])} phishing links")
            if session['extracted_intel']['bankAccounts']:
                intel_summary.append(f"{len(session['extracted_intel']['bankAccounts'])} bank accounts")
            
            session['agent_notes'] = f"Engaged scammer for {session['turn_number']} turns. Extracted: {', '.join(intel_summary) if intel_summary else 'gathering intelligence'}. Using urgency-based engagement tactics."
            
            # Send final result to GUVI after 3+ turns
            if session['turn_number'] >= 3:
                logger.info(f"Sending final callback to GUVI (turn {session['turn_number']})")
                send_final_result_to_guvi(session)
            
            logger.info(f"Scam engaged - Turn {session['turn_number']}, Reply: {agent_reply[:50]}...")
            
            # Return response in hackathon format
            return jsonify({
                'status': 'success',
                'reply': agent_reply
            }), 200
        
        else:
            # Not a scam - neutral response
            logger.info("No scam detected - neutral response")
            return jsonify({
                'status': 'success',
                'reply': 'Thank you for your message.'
            }), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get full conversation history for a session (for debugging)"""
    if session_id not in conversation_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    session = conversation_sessions[session_id]
    
    return jsonify({
        'session_id': session_id,
        'messages': session['messages'],
        'extracted_intelligence': {
            k: list(v) for k, v in session['extracted_intel'].items()
        },
        'total_turns': session['turn_number'],
        'is_scam': session['is_scam'],
        'agent_notes': session['agent_notes']
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics (for monitoring)"""
    total_sessions = len(conversation_sessions)
    scam_sessions = sum(1 for s in conversation_sessions.values() if s['is_scam'])
    
    return jsonify({
        'total_sessions': total_sessions,
        'scam_sessions_detected': scam_sessions,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting AI Honey-Pot API on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
