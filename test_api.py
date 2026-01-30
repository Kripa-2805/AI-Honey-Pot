"""
Test Suite for AI Honey-Pot API
Run this file to test all functionality
"""

import requests
import json
import time

# API Base URL - Change this to your deployed URL
BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print(f"{'='*60}\n")

def test_health_check():
    """Test 1: Health Check"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_scam_detection_account_block():
    """Test 2: Scam Detection - Account Block Threat"""
    data = {
        "message": "URGENT: Your bank account has been blocked due to suspicious activity. Click here immediately to verify your identity or we will permanently close your account.",
        "session_id": "test_session_1"
    }
    response = requests.post(f"{BASE_URL}/api/analyze", json=data)
    print_response("Scam Detection - Account Block", response)
    return response.status_code == 200

def test_scam_detection_lottery():
    """Test 3: Scam Detection - Lottery Scam"""
    data = {
        "message": "Congratulations! You have won $50,000 in the international lottery. To claim your prize, please send your bank details to winnerprizes@lucky-lottery.com or call +1-800-555-0123",
        "session_id": "test_session_2"
    }
    response = requests.post(f"{BASE_URL}/api/analyze", json=data)
    print_response("Scam Detection - Lottery Scam", response)
    return response.status_code == 200

def test_legitimate_message():
    """Test 4: Legitimate Message"""
    data = {
        "message": "Hey, are we still meeting for lunch tomorrow at 2 PM? Let me know if you need to reschedule.",
        "session_id": "test_session_3"
    }
    response = requests.post(f"{BASE_URL}/api/analyze", json=data)
    print_response("Legitimate Message Detection", response)
    return response.status_code == 200

def test_conversation_flow():
    """Test 5: Multi-turn Conversation Flow"""
    session_id = f"test_conversation_{int(time.time())}"
    
    messages = [
        "Your account has been suspended. Verify immediately by clicking this link: http://fake-bank-verify.com",
        "This is urgent. You need to verify within 24 hours or your account will be permanently closed.",
        "Please call our support team at +91-9876543210 or email us at support@scambank.com with your card details.",
        "Send your card number, CVV, and OTP to verify. Our agent name is Rahul Kumar from Mumbai branch."
    ]
    
    print(f"\n{'='*60}")
    print(f"TEST: Multi-turn Conversation Flow (Session: {session_id})")
    print(f"{'='*60}\n")
    
    for i, msg in enumerate(messages, 1):
        print(f"\n--- Turn {i} ---")
        print(f"Scammer: {msg}")
        
        data = {
            "message": msg,
            "session_id": session_id
        }
        
        response = requests.post(f"{BASE_URL}/api/analyze", json=data)
        result = response.json()
        
        print(f"Is Scam: {result['is_scam']}")
        print(f"Scam Score: {result['scam_score']}")
        print(f"Agent Response: {result['response']}")
        print(f"Extracted Intel: {result['extracted_intelligence']}")
        
        time.sleep(0.5)  # Small delay between messages
    
    # Get session report
    print(f"\n--- Final Session Report ---")
    response = requests.get(f"{BASE_URL}/api/session/{session_id}/report")
    print_response("Session Intelligence Report", response)
    
    return response.status_code == 200

def test_session_retrieval():
    """Test 6: Session Retrieval"""
    # First create a session
    session_id = "test_retrieval_session"
    data = {
        "message": "Your package is waiting. Pay delivery fee of Rs. 500 to 9876543210 or visit http://fake-delivery.com",
        "session_id": session_id
    }
    requests.post(f"{BASE_URL}/api/analyze", json=data)
    
    # Now retrieve it
    response = requests.get(f"{BASE_URL}/api/session/{session_id}")
    print_response("Session Retrieval", response)
    return response.status_code == 200

def test_stats():
    """Test 7: Statistics Endpoint"""
    response = requests.get(f"{BASE_URL}/api/stats")
    print_response("Overall Statistics", response)
    return response.status_code == 200

def run_all_tests():
    """Run all test cases"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  AI HONEY-POT API - COMPREHENSIVE TEST SUITE  ".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Scam Detection - Account Block", test_scam_detection_account_block),
        ("Scam Detection - Lottery", test_scam_detection_lottery),
        ("Legitimate Message", test_legitimate_message),
        ("Multi-turn Conversation", test_conversation_flow),
        ("Session Retrieval", test_session_retrieval),
        ("Statistics", test_stats)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n")
    print("=" * 60)
    print("TEST SUMMARY".center(60))
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your API is working perfectly! 🎉")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    print("\nMake sure your API is running on http://localhost:5000")
    print("Start the API with: python app.py")
    input("\nPress Enter when your API is ready...")
    
    run_all_tests()