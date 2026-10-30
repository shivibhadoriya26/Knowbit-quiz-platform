# Knowbit – Technical Quiz Application

A Python-based interactive quiz application developed using Streamlit. The application provides subject-wise technical quizzes, user authentication, automatic evaluation, answer review, and quiz performance tracking.

## 1. Project Overview

Knowbit is designed to provide a structured way to practise technical subjects through multiple-choice questions.

Users can register, log in, select a subject, attempt quizzes, view their scores, review answers, and track their previous quiz attempts.

## 2. Features and Functionality

### User Authentication
- New user registration
- Existing user login
- Password hashing using PBKDF2
- User-specific quiz history

### Subject-wise Quizzes

The application contains six technical subjects:

| Subject | Questions |
|---|---:|
| Data Structures and Algorithms (DSA) | 20 |
| Database Management Systems (DBMS) | 20 |
| Python Programming | 20 |
| System Design | 20 |
| Java Programming | 20 |
| C++ Programming | 20 |
| **Total** | **120** |

### Quiz Management
- Multiple-choice questions
- Answer selection
- Quiz submission
- Automatic score calculation
- Accuracy calculation

### Result and Performance Tracking
- Display of quiz scores
- Correct and incorrect answer review
- Quiz retry functionality
- Total quiz attempts
- Average accuracy
- Best-performing subject
- Recent quiz attempt history

## 3. Technologies and Tools

| Technology | Usage |
|---|---|
| Python | Application logic and functionality |
| Streamlit | User interface and application framework |
| HTML | Custom interface elements |
| CSS | Styling and layout |
| Hashlib | Password hashing |
| Git | Version control |
| GitHub | Source code repository |

## 4. Application Workflow

1. User opens the application.
2. User registers or logs into an account.
3. The dashboard displays the available quiz categories.
4. User selects a subject.
5. The application displays 20 multiple-choice questions.
6. User submits the completed quiz.
7. The application calculates the score and accuracy.
8. Results and answer review are displayed.
9. Quiz performance is saved for progress tracking.

## 5. Project Structure

```text
Knowbit-quiz-platform/
│
├── app.py
├── Quiz_application_file.py
├── requirements.txt
├── README.md
└── .gitignore
```

The application also creates a `data/` directory at runtime for storing registration details, login records, and quiz results. These local data files are excluded from Git using `.gitignore`.

## 6. Installation and Execution

**Step 1: Clone the repository**

```bash
git clone https://github.com/shivibhadoriya26/Knowbit-quiz-platform.git
```

**Step 2: Navigate to the project directory**

```bash
cd Knowbit-quiz-platform
```

**Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Run the application**

```bash
python -m streamlit run app.py
```

## 7. Author

**Shivi Bhadoriya**

B.Tech Student

GitHub Profile: [github.com/shivibhadoriya26](https://github.com/shivibhadoriya26)

Project Repository: [Knowbit – Technical Quiz Application](https://github.com/shivibhadoriya26/Knowbit-quiz-platform)

