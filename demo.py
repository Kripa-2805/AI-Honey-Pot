#!/usr/bin/env python3
"""
Quick Demo Script - Shows API in Action
Run this alongside the API to see live scam detection
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_banner():
    print("\n" + "="*70)
    print("🤖 AI HONEY-POT SCAM DETECTION - LIVE DEMO 🤖".center(70))
    print("="*70 + "\n")

def colored_print(text, color="white"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def demo_conversation():
    """Demonstrate a full scam conversation"""
    
    print_banner()
    colored_print("SCENARIO: Banking Scam Attack", "cyan")
    colored_print("The scammer is trying to steal your bank details...\n", "yellow")
    
    session_id = f"demo_{int(time.time())}"
    
    # Scammer messages
    scam_messages = [
        {
            "turn": 1,
            "message": "URGENT ALERT: Your SBI bank account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking: http://sbi-secure-verify.com or call our toll-free number 1800-123-4567. Failure to verify within 24 hours will result in permanent account closure.",
            "description": "Initial scam attempt - creates urgency and fear"
        },
        {
            "turn": 2,
            "message": "Sir, this is very serious matter. Your account shows unauthorized transactions of Rs. 50,000. We need to verify it's not you. Please share your account number, card details and the OTP we will send to secure your account. Time is running out!",
            "description": "Escalating pressure - requesting sensitive info"
        },
        {
            "turn": 3,
            "message": "Our customer care executive Rajesh Kumar from Mumbai Main Branch is handling your case. You can call me directly at +91-9876543210 or email at rajesh.kumar@sbi-customer-care.com. We need CVV and expiry date to reverse the fraudulent transactions immediately.",
            "description": "Providing fake credentials to appear legitimate"
        },
        {
            "turn": 4,
            "message": "Don't worry sir, we will protect your money. Just transfer Rs. 1000 to our security deposit account 12345678901234 (IFSC: SBIN0001234) as processing fee. Once verified, we will refund Rs. 51,000 including your lost amount. This is standard procedure.",
            "description": "Final trap - asking for money transfer"
        }
    ]
    
    print("-" * 70)
    
    for scam in scam_messages:
        colored_print(f"\n📱 SCAMMER MESSAGE (Turn {scam['turn']}):", "red")
        print(f"   {scam['message']}")
        print(f"\n   💡 Tactic: {scam['description']}")
        
        # Send to API
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={
                "message": scam['message'],
                "session_id": session_id
            }
        )
        
        result = response.json()
        
        # Show detection
        colored_print(f"\n🔍 AI ANALYSIS:", "cyan")
        colored_print(f"   ⚠️  Scam Detected: {'YES' if result['is_scam'] else 'NO'}", 
                     "red" if result['is_scam'] else "green")
        colored_print(f"   📊 Threat Score: {result['scam_score']*100:.1f}%", "yellow")
        colored_print(f"   🏷️  Type: {result['scam_type']}", "magenta")
        
        # Show extracted intelligence
        intel = result['extracted_intelligence']
        if any(intel.values()):
            colored_print(f"\n🎯 INTELLIGENCE EXTRACTED:", "green")
            if intel.get('phone_numbers'):
                colored_print(f"   📞 Phone: {', '.join(intel['phone_numbers'])}", "green")
            if intel.get('email_addresses'):
                colored_print(f"   📧 Email: {', '.join(intel['email_addresses'])}", "green")
            if intel.get('urls'):
                colored_print(f"   🌐 URLs: {', '.join(intel['urls'])}", "green")
            if intel.get('bank_details'):
                colored_print(f"   🏦 Bank: {', '.join(intel['bank_details'])}", "green")
            if intel.get('names'):
                colored_print(f"   👤 Names: {', '.join(intel['names'])}", "green")
        
        # Show AI response
        if result.get('response'):
            colored_print(f"\n🤖 AI HONEY-POT RESPONSE:", "blue")
            print(f"   {result['response']}")
        
        print("\n" + "-" * 70)
        time.sleep(2)  # Pause for dramatic effect
    
    # Show final report
    print("\n")
    colored_print("="*70, "cyan")
    colored_print("📊 FINAL INTELLIGENCE REPORT", "cyan")
    colored_print("="*70, "cyan")
    
    report_response = requests.get(f"{BASE_URL}/api/session/{session_id}/report")
    report = report_response.json()
    
    print(f"\n📝 Session ID: {report['session_id']}")
    print(f"🔄 Total Interactions: {report['summary']['total_interactions']}")
    print(f"⏱️  Duration: {report['summary']['duration_seconds']:.1f} seconds")
    print(f"🎯 Scam Type: {report['summary']['scam_type']}")
    
    intel = report['extracted_intelligence']
    print(f"\n🎯 TOTAL INTELLIGENCE GATHERED:")
    print(f"   📞 Phone Numbers: {len(intel.get('phone_numbers', []))}")
    print(f"   📧 Email Addresses: {len(intel.get('email_addresses', []))}")
    print(f"   🌐 URLs: {len(intel.get('urls', []))}")
    print(f"   🏦 Bank Details: {len(intel.get('bank_details', []))}")
    print(f"   👤 Names: {len(intel.get('names', []))}")
    
    print(f"\n💾 All intelligence details:")
    for key, values in intel.items():
        if values:
            colored_print(f"   {key}: {values}", "green")
    
    print("\n" + "="*70)
    colored_print("\n✅ DEMO COMPLETE - Scammer information captured successfully!", "green")
    colored_print("This data can now be reported to authorities! 🚔\n", "yellow")

def quick_test():
    """Quick test of different message types"""
    
    print_banner()
    colored_print("QUICK TEST - Different Message Types\n", "cyan")
    
    test_messages = [
        ("🎉 Lottery Scam", "Congratulations! You have won $50,000 in international lottery. Send your bank details to claim@lottery-winner.com"),
        ("💳 Banking Scam", "Your account will be blocked. Update KYC at http://bank-update.com now!"),
        ("📦 Delivery Scam", "Your package is waiting. Pay Rs. 200 fee to +91-9999888877"),
        ("✅ Normal Message", "Hey! Want to grab coffee tomorrow at 3 PM?"),
    ]
    
    for title, message in test_messages:
        colored_print(f"\n{title}", "yellow")
        colored_print(f"Message: {message}", "white")
        
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={"message": message}
        )
        
        result = response.json()
        
        if result['is_scam']:
            colored_print(f"Result: ⚠️ SCAM DETECTED ({result['scam_score']*100:.0f}% confidence)", "red")
            colored_print(f"Type: {result['scam_type']}", "red")
        else:
            colored_print(f"Result: ✅ Safe Message ({result['scam_score']*100:.0f}% threat)", "green")
        
        print("-" * 70)
        time.sleep(1)

def main():
    """Main demo function"""
    try:
        # Test if API is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            colored_print("❌ API is not responding correctly!", "red")
            return
        
        colored_print("✅ API is running!", "green")
        
        while True:
            print("\n" + "="*70)
            colored_print("CHOOSE DEMO MODE:", "cyan")
            print("1. Full Conversation Demo (Recommended)")
            print("2. Quick Test - Multiple Messages")
            print("3. Exit")
            print("="*70)
            
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == "1":
                demo_conversation()
            elif choice == "2":
                quick_test()
            elif choice == "3":
                colored_print("\n👋 Goodbye! Thanks for watching the demo!\n", "cyan")
                break
            else:
                colored_print("Invalid choice. Please enter 1, 2, or 3.", "red")
    
    except requests.exceptions.ConnectionError:
        colored_print("\n❌ ERROR: Cannot connect to API!", "red")
        colored_print("Make sure the API is running on http://localhost:5000", "yellow")
        colored_print("Start it with: python app.py\n", "yellow")
    except KeyboardInterrupt:
        colored_print("\n\n👋 Demo interrupted. Goodbye!\n", "cyan")
    except Exception as e:
        colored_print(f"\n❌ Unexpected error: {str(e)}\n", "red")

if __name__ == "__main__":
    main()