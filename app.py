"""
AI Honey-Pot Scam Detection API
India AI Impact Hackathon by HCL
Problem 2: Agentic Honey-Pot

This API detects scam messages and engages with scammers to extract intelligence.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from datetime import datetime
import json
import logging
from typing import Dict, List, Any

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== SCAM DETECTION ENGINE ====================

class ScamDetector:
    """Advanced scam message detection using pattern matching and ML techniques"""
    
    # Scam keywords and patterns
    SCAM_PATTERNS = {
        'urgency': [
            r'urgent', r'immediately', r'right now', r'asap', r'limited time',
            r'act now', r'expires', r'hurry', r'last chance', r'time sensitive'
        ],
        'threats': [
            r'blocked', r'suspended', r'deactivated', r'terminated', r'cancelled',
            r'legal action', r'arrest', r'lawsuit', r'fraud', r'unauthorized',
            r'suspicious activity', r'security alert'
        ],
        'financial': [
            r'won', r'prize', r'lottery', r'jackpot', r'reward', r'refund',
            r'tax refund', r'inheritance', r'compensation', r'claim',
            r'transfer', r'payment', r'credit', r'deposit', r'wire'
        ],
        'personal_info': [
            r'verify', r'confirm', r'update', r'validate', r'authenticate',
            r'click here', r'link', r'account details', r'password', r'pin',
            r'otp', r'cvv', r'card number', r'social security', r'aadhar'
        ],
        'too_good': [
            r'free', r'guaranteed', r'no risk', r'100%', r'amazing offer',
            r'exclusive', r'selected', r'chosen', r'congratulations'
        ],
        'impersonation': [
            r'bank', r'government', r'irs', r'income tax', r'police',
            r'court', r'customs', r'delivery', r'fedex', r'dhl',
            r'amazon', r'flipkart', r'paytm', r'phonepe', r'google pay'
        ]
    }
    
    def calculate_scam_score(self, message: str) -> float:
        """Calculate scam probability score (0-1)"""
        message_lower = message.lower()
        total_score = 0.0
        max_score = 0.0
        
        # Check each category
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
                    break  # Count each category only once
        
        # Normalize score
        score = total_score / max_score if max_score > 0 else 0.0
        
        # Bonus checks
        # Check for URLs
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message):
            score += 0.15
        
        # Check for phone numbers
        if re.search(r'\+?\d{10,}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', message):
            score += 0.05
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def is_scam(self, message: str, threshold: float = 0.3) -> bool:
        """Determine if message is a scam"""
        score = self.calculate_scam_score(message)
        return score >= threshold


# ==================== HONEY-POT CONVERSATION ENGINE ====================

class HoneyPotAgent:
    """Intelligent agent that engages scammers and extracts information"""
    
    def __init__(self):
        self.conversation_history = []
        self.extracted_info = {
            'phone_numbers': [],
            'email_addresses': [],
            'bank_details': [],
            'urls': [],
            'names': [],
            'addresses': [],
            'scam_type': '',
            'timestamps': []
        }
    
    def extract_information(self, message: str) -> Dict[str, List[str]]:
        """Extract all valuable information from scammer's message"""
        info = {}
        
        # Extract phone numbers
        phones = re.findall(r'\+?\d{10,}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', message)
        if phones:
            info['phone_numbers'] = phones
        
        # Extract email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        if emails:
            info['email_addresses'] = emails
        
        # Extract URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        if urls:
            info['urls'] = urls
        
        # Extract bank account numbers (generic pattern)
        bank_accounts = re.findall(r'\b\d{9,18}\b', message)
        if bank_accounts:
            info['bank_details'] = bank_accounts
        
        # Extract IFSC codes
        ifsc = re.findall(r'\b[A-Z]{4}0[A-Z0-9]{6}\b', message)
        if ifsc:
            if 'bank_details' not in info:
                info['bank_details'] = []
            info['bank_details'].extend(ifsc)
        
        # Extract potential names (capitalized words)
        names = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', message)
        if names:
            info['names'] = names
        
        return info
    
    def generate_response(self, scammer_message: str, turn_number: int) -> str:
        """Generate realistic victim response to keep scammer engaged"""
        
        message_lower = scammer_message.lower()
        
        # Turn 1: Show interest and concern
        if turn_number == 1:
            if any(word in message_lower for word in ['block', 'suspend', 'deactivate']):
                return "Oh no! My account is blocked? I didn't do anything wrong. What happened? Please help me fix this!"
            elif any(word in message_lower for word in ['won', 'prize', 'lottery']):
                return "Really? I won something? That's amazing! What did I win? How do I claim it?"
            elif any(word in message_lower for word in ['refund', 'payment']):
                return "A refund? I wasn't expecting any refund. Can you tell me more details about this?"
            else:
                return "I received your message. Can you please explain what this is about? I want to make sure I understand correctly."
        
        # Turn 2: Ask for specifics (to get more info)
        elif turn_number == 2:
            if any(word in message_lower for word in ['click', 'link', 'website']):
                return "I'm a bit worried about clicking random links. Can you tell me what website this is? Is it official? Can you give me more details first?"
            elif any(word in message_lower for word in ['call', 'contact', 'reach']):
                return "Yes, I can call. What number should I call? And what's your name? I want to make note of who I spoke with."
            else:
                return "Okay, I understand some of it. But can you give me more specific information? Like your official contact details and your full name?"
        
        # Turn 3: Pretend to be cautious but willing
        elif turn_number == 3:
            return "I want to cooperate but I'm a bit nervous. Can you provide your official company details, employee ID, and a callback number? My friend told me to always verify these things."
        
        # Turn 4: Ask about payment/process
        elif turn_number == 4:
            if any(word in message_lower for word in ['pay', 'fee', 'charge', 'send']):
                return "You want me to pay a fee? How much? And where should I send it? What bank account or payment method do you accept?"
            else:
                return "What's the next step? Do I need to provide any information? And how long will this take to resolve?"
        
        # Turn 5+: Stall and gather more info
        else:
            responses = [
                "I'm still a bit confused. Can you send me an official email or document with all the details? What's your email address?",
                "My family member is asking me to get everything in writing. Can you provide your office address and official contact information?",
                "I want to verify this is legitimate. What's your supervisor's name and contact number?",
                "Before I proceed, can you tell me which branch or office you're calling from? And what's the complaint or reference number?",
                "I need to discuss this with my bank first. What exact information do you need from me? And can you send it via official email?"
            ]
            return responses[min(turn_number - 5, len(responses) - 1)]
    
    def determine_scam_type(self, message: str) -> str:
        """Identify the type of scam"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['bank', 'account', 'card', 'atm']):
            return "Banking/Financial Fraud"
        elif any(word in message_lower for word in ['won', 'lottery', 'prize']):
            return "Lottery/Prize Scam"
        elif any(word in message_lower for word in ['tax', 'refund', 'irs', 'income tax']):
            return "Tax Refund Scam"
        elif any(word in message_lower for word in ['delivery', 'package', 'courier']):
            return "Delivery/Package Scam"
        elif any(word in message_lower for word in ['suspended', 'blocked', 'verify', 'otp']):
            return "Account Verification Scam"
        elif any(word in message_lower for word in ['job', 'work from home', 'earn']):
            return "Job/Employment Scam"
        elif any(word in message_lower for word in ['investment', 'crypto', 'trading']):
            return "Investment Scam"
        else:
            return "General Phishing/Scam"


# ==================== INITIALIZE SERVICES ====================

scam_detector = ScamDetector()
honeypot_agent = HoneyPotAgent()

# Store conversation sessions (in production, use Redis or database)
conversation_sessions = {}


# ==================== API ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Honey-Pot Scam Detection API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_message():
    """
    Main endpoint for scam detection and honey-pot conversation
    
    Request format:
    {
        "message": "Your account has been suspended. Click here to verify",
        "session_id": "optional_session_id",
        "conversation_history": []  // optional
    }
    
    Response format:
    {
        "is_scam": true/false,
        "scam_score": 0.85,
        "scam_type": "Account Verification Scam",
        "should_engage": true/false,
        "response": "Agent's response to scammer",
        "extracted_intelligence": {
            "phone_numbers": [],
            "emails": [],
            "urls": [],
            "bank_details": []
        }
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Message field is required'
            }), 400
        
        message = data['message']
        session_id = data.get('session_id', f"session_{datetime.utcnow().timestamp()}")
        conversation_history = data.get('conversation_history', [])
        
        # Log the request
        logger.info(f"Analyzing message from session {session_id}: {message[:100]}")
        
        # Step 1: Detect if message is a scam
        scam_score = scam_detector.calculate_scam_score(message)
        is_scam = scam_detector.is_scam(message)
        
        # Step 2: Extract information
        extracted_info = honeypot_agent.extract_information(message)
        
        # Step 3: Determine scam type
        scam_type = honeypot_agent.determine_scam_type(message) if is_scam else "Not a scam"
        
        # Step 4: Generate response if it's a scam
        response = ""
        should_engage = is_scam
        
        if is_scam:
            # Get or create session
            if session_id not in conversation_sessions:
                conversation_sessions[session_id] = {
                    'messages': [],
                    'extracted_info': {
                        'phone_numbers': set(),
                        'email_addresses': set(),
                        'bank_details': set(),
                        'urls': set(),
                        'names': set(),
                        'addresses': set()
                    },
                    'turn_number': 0
                }
            
            session = conversation_sessions[session_id]
            session['messages'].append({
                'role': 'scammer',
                'content': message,
                'timestamp': datetime.utcnow().isoformat()
            })
            session['turn_number'] += 1
            
            # Update extracted info
            for key, values in extracted_info.items():
                if key in session['extracted_info']:
                    session['extracted_info'][key].update(values)
            
            # Generate engaging response
            response = honeypot_agent.generate_response(message, session['turn_number'])
            
            session['messages'].append({
                'role': 'agent',
                'content': response,
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Step 5: Prepare response
        result = {
            'is_scam': is_scam,
            'scam_score': round(scam_score, 3),
            'scam_type': scam_type,
            'should_engage': should_engage,
            'response': response,
            'extracted_intelligence': {
                k: list(v) if isinstance(v, set) else v 
                for k, v in (conversation_sessions[session_id]['extracted_info'].items() 
                            if session_id in conversation_sessions 
                            else extracted_info.items())
            },
            'session_id': session_id,
            'turn_number': conversation_sessions[session_id]['turn_number'] if session_id in conversation_sessions else 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Analysis complete: is_scam={is_scam}, score={scam_score:.3f}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get full conversation history for a session"""
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
            k: list(v) for k, v in session['extracted_info'].items()
        },
        'total_turns': session['turn_number']
    }), 200


@app.route('/api/session/<session_id>/report', methods=['GET'])
def get_session_report(session_id):
    """Generate comprehensive intelligence report for a session"""
    if session_id not in conversation_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    session = conversation_sessions[session_id]
    
    # Compile full transcript
    transcript = "\n".join([
        f"[{msg['role'].upper()}]: {msg['content']}"
        for msg in session['messages']
    ])
    
    report = {
        'session_id': session_id,
        'summary': {
            'total_interactions': session['turn_number'],
            'scam_type': honeypot_agent.determine_scam_type(session['messages'][0]['content'] if session['messages'] else ""),
            'duration_seconds': (
                datetime.fromisoformat(session['messages'][-1]['timestamp']) - 
                datetime.fromisoformat(session['messages'][0]['timestamp'])
            ).total_seconds() if len(session['messages']) > 1 else 0
        },
        'extracted_intelligence': {
            k: list(v) for k, v in session['extracted_info'].items()
        },
        'full_transcript': transcript,
        'generated_at': datetime.utcnow().isoformat()
    }
    
    return jsonify(report), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    total_sessions = len(conversation_sessions)
    total_scams_detected = sum(1 for s in conversation_sessions.values() if s['turn_number'] > 0)
    
    all_intel = {
        'phone_numbers': set(),
        'email_addresses': set(),
        'urls': set(),
        'bank_details': set()
    }
    
    for session in conversation_sessions.values():
        for key in all_intel.keys():
            if key in session['extracted_info']:
                all_intel[key].update(session['extracted_info'][key])
    
    return jsonify({
        'total_sessions': total_sessions,
        'total_scams_detected': total_scams_detected,
        'total_intelligence_gathered': {
            k: len(v) for k, v in all_intel.items()
        },
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Set to False in production
    )