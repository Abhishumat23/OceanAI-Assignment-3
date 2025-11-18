# AI-Assisted Document Authoring and Generation Platform

A full-stack, AI-powered web application that allows authenticated users to generate, refine, and export structured business documents using the Google Gemini AI API.

## 🚀 Features

- **User Authentication**: Secure JWT-based registration and login system
- **Project Management**: Create, view, edit, and delete document projects
- **Document Types**: Support for both Microsoft Word (.docx) and PowerPoint (.pptx)
- **AI-Powered Content Generation**: Automatic content generation using Google Gemini API
- **Interactive Refinement**: 
  - Refine content with natural language prompts
  - Like/Dislike feedback system
  - Comment and note-taking on sections
  - Refinement history tracking
- **Document Export**: Download completed documents in .docx or .pptx format
- **Responsive UI**: Clean, modern interface that works on desktop and mobile

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.8+
- **Database**: SQLite (easily replaceable with PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Integration**: Google Gemini API for content generation
- **Document Generation**: python-docx and python-pptx libraries

### Frontend (React)
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **State Management**: React Context API for authentication
- **HTTP Client**: Axios for API calls
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd OceanAi
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Database
DATABASE_URL=sqlite:///./docgen.db

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini API
GEMINI_API_KEY=your-gemini-api-key-here
```

**Important**: 
- Replace `SECRET_KEY` with a strong random string (use `openssl rand -hex 32` to generate one)
- Replace `GEMINI_API_KEY` with your actual Google Gemini API key

#### Initialize the Database

The database will be automatically created when you first run the application. Tables are created using SQLAlchemy models.

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd ../frontend
npm install
```

The frontend is pre-configured to proxy API requests to `http://localhost:8000`.

## 🚀 Running the Application

### Start the Backend Server

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### Start the Frontend Development Server

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

## 📖 Usage Guide

### 1. User Registration & Login

1. Navigate to `http://localhost:3000`
2. Click "Register here" to create a new account
3. Fill in email, username, and password
4. After registration, login with your credentials

### 2. Creating a Project

1. Click "New Project" on the dashboard
2. **Step 1**: Configure basic information
   - Enter a project title
   - Select document type (Word or PowerPoint)
   - Describe the main topic/prompt
3. **Step 2**: Define structure
   - Add section titles (for Word) or slide titles (for PowerPoint)
   - Reorder or remove sections as needed
4. Click "Create Project"

### 3. Generating Content

1. Open a project from the dashboard
2. Click "Generate Content" to have AI create content for all sections
3. Wait for the AI to generate content (may take 30-60 seconds)

### 4. Refining Content

For each section/slide, you can:

- **Refine with AI**: Enter a prompt like:
  - "Make this more formal"
  - "Shorten to 100 words"
  - "Add more technical details"
  - "Convert to bullet points"
  
- **Provide Feedback**:
  - 👍 Like button - mark content as good
  - 👎 Dislike button - mark content as needing improvement
  - 💬 Add Comment - add notes or feedback

- **View History**: All refinements are tracked and stored

### 5. Exporting Documents

1. Once content is generated, click "Export Document"
2. The file will download in the appropriate format (.docx or .pptx)
3. Open with Microsoft Word or PowerPoint

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive JWT token
- `GET /api/auth/me` - Get current user info

### Projects
- `GET /api/projects` - List all user projects
- `POST /api/projects` - Create new project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `POST /api/projects/{id}/generate` - Generate AI content

### Sections
- `PUT /api/sections/{id}` - Update section
- `POST /api/sections/{id}/refine` - Refine content with AI
- `POST /api/sections/{id}/feedback` - Add feedback
- `GET /api/sections/{id}/refinements` - Get refinement history

### Export
- `GET /api/export/{project_id}` - Export document

## 📁 Project Structure

```
OceanAi/
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── projects.py      # Project management
│   │   ├── sections.py      # Section editing & refinement
│   │   └── export.py        # Document export
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── ai_service.py        # Gemini AI integration
│   ├── document_service.py  # Document generation
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CreateProjectModal.jsx
│   │   │   ├── Editor.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── App.jsx          # Main app component
│   │   ├── App.css          # Styles
│   │   ├── main.jsx         # Entry point
│   │   ├── api.js           # API client
│   │   └── AuthContext.jsx  # Auth state management
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🗄️ Database Schema

### Users
- id, email, username, hashed_password, created_at

### Projects
- id, title, document_type, main_topic, user_id, created_at, updated_at

### DocumentSections
- id, project_id, title, content, order, created_at, updated_at

### Refinements
- id, section_id, prompt, previous_content, new_content, created_at

### Feedback
- id, section_id, is_liked, comment, created_at

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Input validation with Pydantic
- User isolation (users can only access their own projects)

## 🚀 Deployment

### Backend Deployment (e.g., Railway, Heroku, AWS)

1. Update `DATABASE_URL` in production to use PostgreSQL:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

2. Set secure `SECRET_KEY` in production environment

3. Configure CORS origins in `main.py` to match your frontend URL

4. Deploy using:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### Frontend Deployment (e.g., Vercel, Netlify)

1. Update API base URL in `frontend/src/api.js`:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.com';
   ```

2. Build the production bundle:
   ```bash
   npm run build
   ```

3. Deploy the `dist` folder

## 🧪 Testing

### Backend Testing

```bash
cd backend
pytest  # After installing pytest
```

### Frontend Testing

```bash
cd frontend
npm test  # After configuring test setup
```

## 🐛 Troubleshooting

### Backend Issues

**Database errors**: Delete `docgen.db` and restart the server to recreate

**Gemini API errors**: 
- Verify your API key is correct
- Check API quota limits
- Ensure internet connectivity

**Import errors**: Reinstall dependencies with `pip install -r requirements.txt`

### Frontend Issues

**Connection refused**: Ensure backend is running on port 8000

**Login fails**: Check browser console for errors, verify backend is accessible

**Build errors**: Delete `node_modules` and run `npm install` again

## 📝 Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | `sqlite:///./docgen.db` |
| SECRET_KEY | JWT secret key | `your-secret-key-here` |
| ALGORITHM | JWT algorithm | `HS256` |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time | `30` |
| GEMINI_API_KEY | Google Gemini API key | `your-api-key` |

## 🎯 Future Enhancements

- [ ] Real-time collaborative editing
- [ ] Document templates library
- [ ] Multi-language support
- [ ] Advanced formatting options
- [ ] Version control for documents
- [ ] Team/workspace management
- [ ] Export to additional formats (PDF, Markdown)
- [ ] Integration with Google Drive/Dropbox

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Development

### Code Style

- Backend: Follow PEP 8 guidelines
- Frontend: Use ESLint with React recommended rules

### Git Workflow

```bash
git checkout -b feature/your-feature-name
git commit -m "Add: description of changes"
git push origin feature/your-feature-name
```

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Review backend logs for API errors

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI framework
- React and Vite
- python-docx and python-pptx libraries

---

**Built with ❤️ using FastAPI and React**
