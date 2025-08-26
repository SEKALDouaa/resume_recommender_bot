
```markdown
# Resume Recommender Bot

This project is a **chatbot system** designed to retrieve the most relevant resumes from a database based on user queries. It leverages **LangChain**, **ChromaDB** for vector storage, **SQLite** for relational data, and **Marshmallow** for serialization. The system combines a **Flask backend** and an **Angular frontend** to provide an interactive user experience.

---

## 🚀 Features
- Upload resumes and store them in a structured way.
- Query the chatbot to retrieve the most relevant resumes.
- Uses embeddings and RAG (Retrieval-Augmented Generation) via **LangChain**.
- REST API powered by Flask.
- Interactive Angular frontend.
- Secure authentication with JWT.

---

## 📂 Project Structure

```
RESUME_RECOMMENDER_BOT/
├── app/                     # Flask backend application
├── chroma_db/               # ChromaDB vector database
├── data/                    # Data folder (resumes, etc.)
├── frontend/                # Angular frontend
├── instance/                # SQLite relational database
├── .env                     # Environment variables
├── config.py                # App configuration
├── requirements.txt         # Python dependencies
├── run.py                   # Backend entry point
└── README.md                # Documentation
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=sqlite:///instance/resumes.db
JWT_SECRET_KEY=your_secret_key
```

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/resume_recommender_bot.git
cd resume_recommender_bot
```

### 2. Backend Setup (Flask)
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python run.py
```

The backend will run by default at:  
👉 `http://127.0.0.1:5000`

---

### 3. Frontend Setup (Angular)
```bash
cd frontend
npm install
ng serve
```

The frontend will run by default at:  
👉 `http://localhost:4200`

---

## 💡 Usage

1. Upload resumes through the frontend interface.  
2. Interact with the chatbot to ask for the most relevant resumes.  
3. The chatbot queries the **vector database (ChromaDB)** and **relational database (SQLite)** to return ranked resumes.  

---

## 🔮 Future Improvements
- Add support for multiple file formats (DOCX, LinkedIn exports, etc.).
- Enhance ranking algorithms with hybrid retrieval.
- Improve UI/UX of the chatbot interface.
- Add user management and role-based access.
