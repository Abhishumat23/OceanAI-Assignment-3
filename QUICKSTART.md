# Quick Start Guide

## 5-Minute Setup

### 1. Get Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the API key

### 2. Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
- Set `SECRET_KEY` to a random string (run `openssl rand -hex 32` to generate)
- Set `GEMINI_API_KEY` to your Gemini API key from step 1

### 3. Start Backend (Terminal 1)

```bash
cd backend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start on http://localhost:8000

### 4. Start Frontend (Terminal 2)

```bash
cd frontend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd frontend
npm install
npm run dev
```

Frontend will start on http://localhost:3000

### 5. Use the Application

1. Open http://localhost:3000
2. Click "Register here" to create an account
3. Login with your credentials
4. Click "New Project" to create your first document
5. Follow the wizard to configure and generate content
6. Refine content with AI prompts
7. Export your document!

## Demo Workflow

### Creating a Word Document

1. **New Project**
   - Title: "Q4 Marketing Strategy"
   - Type: Microsoft Word
   - Topic: "Marketing strategy for Q4 2025 focusing on digital channels"

2. **Add Sections**
   - Executive Summary
   - Market Analysis
   - Strategy Overview
   - Digital Channels
   - Budget Allocation
   - Timeline and Milestones
   - Conclusion

3. **Generate Content** - AI creates content for all sections

4. **Refine Content**
   - For "Strategy Overview": "Make this more data-driven"
   - For "Budget Allocation": "Add specific dollar amounts"
   - Add 👍 to sections you like
   - Add 💬 comments for notes

5. **Export** - Download as .docx

### Creating a PowerPoint Presentation

1. **New Project**
   - Title: "AI Technology Trends 2025"
   - Type: Microsoft PowerPoint
   - Topic: "Latest trends in artificial intelligence and machine learning"

2. **Add Slides**
   - Introduction to AI in 2025
   - Generative AI Revolution
   - Enterprise AI Adoption
   - Ethical AI Considerations
   - Future Predictions
   - Call to Action

3. **Generate Content** - AI creates bullet points for each slide

4. **Refine Content**
   - For any slide: "Add more technical details"
   - For any slide: "Make it more concise"
   - Provide feedback and comments

5. **Export** - Download as .pptx

## Troubleshooting

### Backend won't start
- Check if Python 3.8+ is installed: `python3 --version`
- Ensure .env file has valid GEMINI_API_KEY
- Check if port 8000 is available

### Frontend won't start
- Check if Node.js 16+ is installed: `node --version`
- Try deleting node_modules and running `npm install` again
- Check if port 3000 is available

### Can't login
- Check browser console (F12) for errors
- Verify backend is running on http://localhost:8000
- Try registering a new account

### Content generation fails
- Verify your Gemini API key is correct
- Check your API quota/limits
- Look at backend terminal for error messages

### Export doesn't work
- Ensure all sections have generated content
- Check browser console for errors
- Verify backend has write permissions

## API Documentation

Once the backend is running, view interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

- Explore the refinement features
- Try different types of documents
- Experiment with various AI prompts
- Check the README.md for advanced features

## Support

For issues:
1. Check this guide first
2. Review the main README.md
3. Check the API docs at /docs
4. Look at browser and terminal logs
