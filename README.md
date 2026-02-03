# 📚 Library Management System

A comprehensive library management system built with Python and Streamlit that supports multiple copies of books, automated return date tracking, and user account management.

## Features

✅ **User Authentication** - Secure login system  
✅ **Book Inventory Management** - Track multiple copies of each book  
✅ **Issue Books** - Borrow books with automatic 15-day return deadline  
✅ **Return Books** - Easy return process with transaction tracking  
✅ **Dashboard** - View your borrowed books and days remaining  
✅ **View Available Books** - Browse all books and their availability  
✅ **View All Issued Books** - Admin view of all issued books with user info and return dates  
✅ **Overdue Tracking** - Automatically identifies and highlights overdue books  
✅ **Data Persistence** - All data saved in JSON format  

## Project Structure

```
LMS/
├── code.py              # Backend library management classes
├── app.py              # Streamlit web UI
├── requirements.txt    # Python dependencies
├── venv/               # Virtual environment (created during setup)
├── library_data.json   # Data storage (created on first run)
└── README.md           # This file
```

## Setup Instructions

### 1. Navigate to the Project Directory
```bash
cd "c:\Users\kulka\DS_certification\Data_science\deployment\LMS"
```

### 2. Activate the Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Demo Credentials

Use these credentials to login:

| Username | Password |
|----------|----------|
| admin    | admin123 |
| user1    | pass123  |
| user2    | pass123  |

## How to Use

### For Regular Users

1. **Login** - Enter your username and password
2. **View Available Books** - Browse books available for borrowing
3. **Issue a Book** - Select a book and click "Issue This Book"
4. **View My Borrowed Books** - See all your borrowed books with due dates
5. **Return a Book** - Click return to return any borrowed book
6. **Dashboard** - Get a quick overview of your borrowed books

### For Admin Users

1. **Login as admin** (username: admin, password: admin123)
2. Access **Add New Book (Admin)** option
3. Add new books with specified number of copies
4. View all books in the library inventory

## System Details

- **Maximum Borrow Period**: 15 days
- **Tracking**: All issues and returns are tracked with timestamps
- **Overdue Management**: System automatically calculates and highlights overdue books
- **Data Storage**: Uses JSON file for persistent data storage

## Features Explanation

### Dashboard
- Shows total books, available copies, and issued books count
- Displays your borrowed books with days remaining
- Highlights overdue books with warning

### View Available Books
- Shows all books currently available for borrowing
- Displays total and available copies for each book
- Shows number of copies currently issued

### Issue Book
- Select from available books
- Automatic calculation of due date (15 days from issue)
- Transaction ID generated for tracking

### My Borrowed Books
- Lists all books you've borrowed
- Shows issue date and due date
- Displays days remaining or overdue status
- One-click return option

### Return Book
- Shows all your borrowed books
- Easy selection and return process
- Confirmation message after successful return

### View All Issued Books
- Admin view of all issued books
- Filter by user name
- Filter to show only overdue books
- Shows who borrowed what and when they need to return

### Add New Book (Admin Only)
- Admin can add new books to library
- Specify number of copies
- View current library inventory

## Data Persistence

All data is automatically saved in `library_data.json` which includes:
- Book inventory with copy counts
- All issued books with user information
- Issue dates and due dates
- Transaction tracking

## Troubleshooting

### Virtual Environment Not Activating
Make sure you're in the correct directory and use the full path if needed.

### Streamlit Not Found
Ensure the virtual environment is activated before running the app.

### Port Already in Use
Streamlit runs on port 8501 by default. You can change it with:
```bash
streamlit run app.py --server.port 8502
```

### Library Data Reset
Delete `library_data.json` and restart the app to reset to default data.

## Future Enhancements

- Email notifications for upcoming due dates
- Fine system for overdue books
- Book reviews and ratings
- Search functionality
- Renewals without return
- Hold/Reserve system
- Database integration instead of JSON

## Author Notes

This system is designed for educational purposes and demonstrates:
- Object-oriented programming in Python
- Streamlit web framework
- JSON data persistence
- User authentication
- Date/time calculations
- Data filtering and display

---

**Version**: 1.0  
**Last Updated**: February 2026
