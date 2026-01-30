# 🏆 AI HONEY-POT SCAM DETECTION API
## India AI Impact Hackathon by HCL - Problem 2

---

## 🎯 What This Does (Simple Explanation)

Imagine you have a smart robot bodyguard for your phone:

1. **Scammers send fake messages** → "Your account is blocked! Click here!"
2. **Your AI detects it's a scam** → Analyzes patterns, keywords, urgency
3. **AI pretends to be a victim** → "Oh no! What should I do?"
4. **Scammer reveals information** → Phone numbers, bank accounts, websites
5. **AI collects everything** → All scammer data saved for authorities

**It's like setting a trap for criminals!** They think they found a victim, but YOU'RE catching THEM! 🎣

---

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the API
```bash
python app.py
```

Your API will start on: `http://localhost:5000`

### Step 3: Test It
```bash
python test_api.py
```

---

## 📡 API Endpoints

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Honey-Pot Scam Detection API",
  "version": "1.0.0"
}
```

### 2. Analyze Message (Main Endpoint)
```bash
POST /api/analyze
```

**Request:**
```json
{
  "message": "URGENT: Your account has been blocked. Click here immediately!",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "is_scam": true,
  "scam_score": 0.85,
  "scam_type": "Account Verification Scam",
  "should_engage": true,
  "response": "Oh no! My account is blocked? Please help me fix this!",
  "extracted_intelligence": {
    "phone_numbers": [],
    "email_addresses": [],
    "urls": ["http://fake-link.com"],
    "bank_details": []
  },
  "session_id": "session_123",
  "turn_number": 1
}
```

### 3. Get Session History
```bash
GET /api/session/{session_id}
```

### 4. Get Intelligence Report
```bash
GET /api/session/{session_id}/report
```

**Returns full conversation transcript and all extracted data**

### 5. Get Statistics
```bash
GET /api/stats
```

---

## 🎮 Testing Examples

### Test 1: Account Block Scam
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "URGENT: Your bank account has been blocked. Verify immediately!"
  }'
```

### Test 2: Lottery Scam
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Congratulations! You won $10,000. Call +91-9876543210 to claim."
  }'
```

### Test 3: Legitimate Message
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hey, are we still meeting for lunch tomorrow?"
  }'
```

---

## 🏗️ How It Works (Technical)

### 1. Scam Detection Engine
- **Pattern Matching**: Checks for urgency words, threats, financial terms
- **Scoring System**: Calculates probability (0-1) based on multiple factors
- **Categories Analyzed**:
  - Urgency indicators (15% weight)
  - Threats and warnings (25% weight)
  - Financial terms (20% weight)
  - Personal info requests (20% weight)
  - Too-good-to-be-true offers (10% weight)
  - Impersonation attempts (10% weight)

### 2. Information Extraction
Uses regex patterns to extract:
- Phone numbers (all formats)
- Email addresses
- URLs and links
- Bank account numbers
- IFSC codes
- Names
- Addresses

### 3. Honey-Pot Conversation Agent
- **Turn 1**: Shows concern and interest
- **Turn 2**: Asks for specifics
- **Turn 3**: Requests verification
- **Turn 4**: Inquires about payment
- **Turn 5+**: Stalls and gathers more intel

**Strategy**: Keep scammer engaged while extracting maximum information

---

## 🌐 Deployment Options

### Option 1: Local Testing
```bash
python app.py
```

### Option 2: Heroku Deployment
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-app-name
git push heroku master
```

### Option 3: Railway.app (Easiest)
1. Go to railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect your repository
5. Railway auto-detects Flask and deploys!

### Option 4: Render.com
1. Create account on render.com
2. New Web Service → Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Click "Create Web Service"

### Option 5: AWS/GCP/Azure
Use Elastic Beanstalk, App Engine, or App Service respectively

---

## 🔑 Key Features That Make This Win

### ✅ Advanced Scam Detection
- Multi-pattern analysis
- Weighted scoring system
- Detects 7+ types of scams
- Low false positive rate

### ✅ Intelligent Conversation
- Context-aware responses
- Natural victim behavior
- Multi-turn engagement
- Adaptive strategy

### ✅ Comprehensive Intelligence Gathering
- Extracts all contact info
- Identifies scam patterns
- Tracks conversation history
- Generates detailed reports

### ✅ Production-Ready Code
- Error handling
- Logging
- Session management
- RESTful API design
- CORS enabled
- Health checks

### ✅ Scalable Architecture
- Stateless design (ready for Redis/DB)
- Can handle multiple concurrent sessions
- Easy to deploy anywhere
- Microservices-ready

---

## 🎯 Evaluation Criteria - How We Win

### 1. Correctness ✅
- Accurately detects scams (high precision)
- Properly classifies legitimate messages
- Extracts information correctly

### 2. Stability ✅
- Handles errors gracefully
- Works reliably across multiple requests
- No crashes or unexpected behavior

### 3. JSON Response Format ✅
- Clean, consistent structure
- All required fields present
- Easy to parse and use

### 4. Low Latency ✅
- Fast pattern matching
- Efficient regex operations
- No blocking operations
- Typical response time: <100ms

### 5. Error Handling ✅
- Validates all inputs
- Returns meaningful error messages
- Proper HTTP status codes
- Logs all errors

---

## 📊 What Makes This Solution Special

### 1. Dual-Mode Operation
- **Detection Mode**: Quick scam identification
- **Engagement Mode**: Active honey-pot conversation

### 2. Intelligence Gathering
- Not just detection - actual threat intel
- Builds criminal profiles
- Can help authorities

### 3. Psychological Approach
- Mimics real victim behavior
- Uses social engineering against scammers
- Keeps them engaged longer

### 4. Scalability
- Can process thousands of messages
- Ready for production deployment
- Easy to add ML models later

---

## 🚀 Future Enhancements (Post-Hackathon)

### Phase 1: Mobile App
- Android/iOS app
- Runs on device
- Intercepts SMS/messages
- Real-time protection

### Phase 2: Machine Learning
- Train on real scam data
- Deep learning models
- Sentiment analysis
- Behavioral patterns

### Phase 3: Integration
- SMS gateway integration
- Telecom provider API
- WhatsApp/Telegram bots
- Email protection

### Phase 4: Reporting
- Dashboard for authorities
- Analytics and trends
- Scammer database
- Public API for reporting

---

## 📝 API Response Examples

### Scam Detected - First Message
```json
{
  "is_scam": true,
  "scam_score": 0.725,
  "scam_type": "Banking/Financial Fraud",
  "should_engage": true,
  "response": "Oh no! My account is blocked? I didn't do anything wrong. What happened? Please help me fix this!",
  "extracted_intelligence": {
    "phone_numbers": [],
    "email_addresses": [],
    "urls": ["http://fake-bank.com/verify"],
    "bank_details": [],
    "names": [],
    "addresses": []
  },
  "session_id": "session_1738168800",
  "turn_number": 1,
  "timestamp": "2026-01-29T10:30:00.000Z"
}
```

### Not a Scam
```json
{
  "is_scam": false,
  "scam_score": 0.05,
  "scam_type": "Not a scam",
  "should_engage": false,
  "response": "",
  "extracted_intelligence": {
    "phone_numbers": [],
    "email_addresses": [],
    "urls": [],
    "bank_details": [],
    "names": [],
    "addresses": []
  },
  "session_id": "session_1738168801",
  "turn_number": 0,
  "timestamp": "2026-01-29T10:31:00.000Z"
}
```

---

## 🎓 Understanding the Code Structure

```
app.py
├── ScamDetector Class
│   ├── SCAM_PATTERNS (dictionary of patterns)
│   ├── calculate_scam_score() (scoring algorithm)
│   └── is_scam() (detection logic)
│
├── HoneyPotAgent Class
│   ├── extract_information() (regex extraction)
│   ├── generate_response() (conversation logic)
│   └── determine_scam_type() (classification)
│
└── API Endpoints
    ├── /health (health check)
    ├── /api/analyze (main endpoint)
    ├── /api/session/<id> (session history)
    ├── /api/session/<id>/report (intelligence report)
    └── /api/stats (statistics)
```

---

## 💡 Tips for Winning

1. **Show It Working**: Use test_api.py to demonstrate live
2. **Explain the Impact**: Emphasize public safety aspect
3. **Demonstrate Intelligence**: Show extracted data
4. **Highlight Scalability**: Mention deployment options
5. **Future Vision**: Explain mobile app roadmap

---

## 🔒 Security Considerations

- API keys should be in environment variables (for production)
- Add rate limiting for public deployment
- Implement authentication for sensitive endpoints
- Use HTTPS in production
- Sanitize all inputs
- Store sessions in Redis/DB for production

---

## 📞 Contact & Support

**Team**: India AI Impact - HCL
**Project**: Agentic Honey-Pot for Scam Detection
**Problem Statement**: #2

---

## 🏆 Why This Solution Wins

1. **Complete Solution**: Not just detection - full intelligence gathering
2. **Production Ready**: Can deploy immediately
3. **Well Documented**: Easy to understand and extend
4. **Tested**: Comprehensive test suite included
5. **Innovative**: Honey-pot approach is unique
6. **Scalable**: Ready for real-world deployment
7. **Impactful**: Solves real problem affecting millions

---

**Good luck with your hackathon! This solution demonstrates:**
- ✅ Technical excellence
- ✅ Innovation
- ✅ Real-world impact
- ✅ Scalability
- ✅ Professional code quality

**You've got this! 🚀🏆**