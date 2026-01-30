#!/bin/bash

# AI Honey-Pot Deployment Script
# Quick setup and deployment helper

echo "=================================="
echo "🤖 AI HONEY-POT DEPLOYMENT WIZARD"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 found:${NC} $(python3 --version)"
else
    echo -e "${RED}✗ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check pip
echo "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${RED}✗ pip3 not found. Please install pip3${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo "Choose deployment option:"
echo "=================================="
echo "1. Local Development (Recommended for hackathon demo)"
echo "2. Heroku Deployment"
echo "3. Railway.app Deployment"
echo "4. Manual Setup Only"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}Setting up for local development...${NC}"
        echo ""
        
        # Install dependencies
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
        else
            echo -e "${RED}✗ Failed to install dependencies${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}✓ Setup complete!${NC}"
        echo ""
        echo "=================================="
        echo "🚀 READY TO LAUNCH"
        echo "=================================="
        echo ""
        echo "To start the API:"
        echo -e "${YELLOW}  python3 app.py${NC}"
        echo ""
        echo "To run tests:"
        echo -e "${YELLOW}  python3 test_api.py${NC}"
        echo ""
        echo "To see live demo:"
        echo -e "${YELLOW}  python3 demo.py${NC}"
        echo ""
        echo "API will be available at:"
        echo -e "${GREEN}  http://localhost:5000${NC}"
        echo ""
        
        read -p "Start the API now? (y/n): " start_now
        if [ "$start_now" = "y" ] || [ "$start_now" = "Y" ]; then
            echo ""
            echo "Starting API..."
            python3 app.py
        fi
        ;;
        
    2)
        echo ""
        echo -e "${YELLOW}Setting up for Heroku deployment...${NC}"
        echo ""
        
        # Check Heroku CLI
        if ! command -v heroku &> /dev/null; then
            echo -e "${RED}✗ Heroku CLI not found${NC}"
            echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        echo -e "${GREEN}✓ Heroku CLI found${NC}"
        echo ""
        
        # Heroku setup
        read -p "Enter your Heroku app name: " app_name
        
        echo "Logging into Heroku..."
        heroku login
        
        echo "Creating Heroku app..."
        heroku create $app_name
        
        echo "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit - AI Honey-Pot"
        
        echo "Deploying to Heroku..."
        git push heroku master
        
        echo ""
        echo -e "${GREEN}✓ Deployed successfully!${NC}"
        echo ""
        echo "Your API is available at:"
        echo -e "${GREEN}  https://$app_name.herokuapp.com${NC}"
        echo ""
        echo "To view logs:"
        echo -e "${YELLOW}  heroku logs --tail${NC}"
        ;;
        
    3)
        echo ""
        echo -e "${YELLOW}Railway.app Deployment Instructions${NC}"
        echo ""
        echo "1. Go to https://railway.app"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New Project'"
        echo "4. Select 'Deploy from GitHub repo'"
        echo "5. Choose this repository"
        echo "6. Railway will auto-detect Flask and deploy!"
        echo ""
        echo "That's it! Railway handles everything automatically."
        echo ""
        ;;
        
    4)
        echo ""
        echo -e "${YELLOW}Manual setup mode...${NC}"
        echo ""
        echo "Installing dependencies only..."
        pip3 install -r requirements.txt
        
        echo ""
        echo -e "${GREEN}✓ Dependencies installed${NC}"
        echo ""
        echo "Manual steps:"
        echo "1. Start API: python3 app.py"
        echo "2. Test API: python3 test_api.py"
        echo "3. Demo: python3 demo.py"
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "📚 HELPFUL COMMANDS"
echo "=================================="
echo ""
echo "Start API:"
echo "  python3 app.py"
echo ""
echo "Run tests:"
echo "  python3 test_api.py"
echo ""
echo "Live demo:"
echo "  python3 demo.py"
echo ""
echo "Test endpoint manually:"
echo '  curl -X POST http://localhost:5000/api/analyze \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{"message": "Your account is blocked!"}'"'"
echo ""
echo "=================================="
echo ""
echo -e "${GREEN}Good luck with your hackathon! 🏆${NC}"
echo ""