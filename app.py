import streamlit as st
from code import Library, User
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(page_title="Library Management System", layout="wide", initial_sidebar_state="expanded")

# Add custom CSS for background and styling
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            background-attachment: fixed;
         }}
         
         /* Custom styling for containers */
         .stForm, [data-testid="stVerticalBlock"] > [style*="flex-direction"] > [data-testid="stVerticalBlock"] {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
         }}
         
         /* Sidebar styling */
         [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            color: white;
         }}
         
         [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: white;
         }}
         
         /* Title styling */
         h1 {{
            color: #2c3e50;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            font-weight: 700;
         }}
         
         h2, h3 {{
            color: #34495e;
         }}
         
         /* Button styling */
         .stButton > button {{
            background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
            color: white;
            border-radius: 5px;
            font-weight: 600;
            padding: 10px 20px;
            border: none;
         }}
         
         .stButton > button:hover {{
            background: linear-gradient(90deg, #2980b9 0%, #1f618d 100%);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
         }}
         
         /* Container styling */
         [data-testid="stContainer"] {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 15px;
         }}
         
         /* Metric styling */
         [data-testid="stMetricContainer"] {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            padding: 15px;
            color: white;
         }}
         </style>
         """,
         unsafe_allow_html=True
    )

add_bg_from_url()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Simple authentication
def authenticate(username, password):
    """Simple authentication - hardcoded for demo"""
    users = {
        'admin': 'admin123',
        'user1': 'pass123',
        'user2': 'pass123'
    }
    return username in users and users[username] == password

# Sidebar for navigation
if not st.session_state.logged_in:
    st.title("📚 Library Management System")
    st.write("Please login to access the library system")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
else:
    # Main app after login
    st.sidebar.title(f"👤 {st.session_state.username}")
    
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Navigation menu
    page = st.sidebar.radio("Navigation", 
                           ["Dashboard", 
                            "View Available Books", 
                            "Issue Book",
                            "My Borrowed Books",
                            "Return Book",
                            "View All Issued Books",
                            "Add New Book (Admin)"])
    
    # Initialize library
    library = Library()
    
    # ==================== DASHBOARD ====================
    if page == "Dashboard":
        st.title("📊 Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_books = sum(book['total_copies'] for book in library.data['books'].values())
            st.metric("Total Books", total_books)
        
        with col2:
            available_books = sum(book['available_copies'] for book in library.data['books'].values())
            st.metric("Available Copies", available_books)
        
        with col3:
            issued_books = len(library.data['issued_books'])
            st.metric("Issued Books", issued_books)
        
        st.divider()
        
        # User's borrowed books summary
        user_books = library.get_user_borrowed_books(st.session_state.username)
        
        st.subheader(f"Your Borrowed Books ({len(user_books)})")
        if user_books:
            for book in user_books:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"📖 {book['book']}")
                with col2:
                    st.write(f"Due: {book['due_date']}")
                with col3:
                    if book['is_overdue']:
                        st.error(f"⚠️ {book['days_remaining']} days overdue")
                    else:
                        st.info(f"✅ {book['days_remaining']} days left")
                with col4:
                    st.write(f"ID: {book['transaction_id'][:20]}...")
        else:
            st.info("You haven't borrowed any books yet.")
    
    # ==================== VIEW AVAILABLE BOOKS ====================
    elif page == "View Available Books":
        st.title("📚 Available Books")
        
        available_books = library.get_available_books()
        
        if available_books:
            # Create a dataframe for better display
            books_data = []
            for book_name, info in available_books.items():
                books_data.append({
                    'Book Name': book_name,
                    'Total Copies': info['total_copies'],
                    'Available': info['available_copies'],
                    'Issued': info['total_copies'] - info['available_copies']
                })
            
            df = pd.DataFrame(books_data)
            df.index = df.index + 1
            st.dataframe(df, use_container_width=True)
            
            st.success(f"Total {len(available_books)} books available for issue")
        else:
            st.warning("No books available at the moment.")
    
    # ==================== ISSUE BOOK ====================
    elif page == "Issue Book":
        st.title("📖 Issue a Book")
        
        available_books = library.get_available_books()
        
        if available_books:
            book_names = list(available_books.keys())
            selected_book = st.selectbox("Select a book to issue:", book_names)
            
            if selected_book:
                book_info = available_books[selected_book]
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Copies", book_info['total_copies'])
                with col2:
                    st.metric("Available", book_info['available_copies'])
                
                st.info(f"📅 Return within {library.max_borrow_days} days")
                
                if st.button("Issue This Book", key="issue_btn"):
                    success, message = library.issue_book(st.session_state.username, selected_book)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.error("No books available for issue at the moment.")
    
    # ==================== MY BORROWED BOOKS ====================
    elif page == "My Borrowed Books":
        st.title("📚 My Borrowed Books")
        
        user_books = library.get_user_borrowed_books(st.session_state.username)
        
        if user_books:
            for idx, book in enumerate(user_books):
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Book:** {book['book']}")
                        st.write(f"**Issued:** {book['issue_date']}")
                    
                    with col2:
                        st.write(f"**Due Date:** {book['due_date']}")
                        if book['is_overdue']:
                            st.error(f"⚠️ OVERDUE by {abs(book['days_remaining'])} days")
                        else:
                            st.info(f"✅ {book['days_remaining']} days remaining")
                    
                    with col3:
                        if st.button("Return", key=f"return_btn_{idx}"):
                            success, message = library.return_book(book['transaction_id'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
        else:
            st.info("You haven't borrowed any books yet.")
    
    # ==================== RETURN BOOK ====================
    elif page == "Return Book":
        st.title("🔄 Return a Book")
        
        user_books = library.get_user_borrowed_books(st.session_state.username)
        
        if user_books:
            st.write("Select a book to return:")
            
            for idx, book in enumerate(user_books):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    status = "⚠️ OVERDUE" if book['is_overdue'] else "✅ ON TIME"
                    st.write(f"{book['book']} - Due: {book['due_date']} ({status})")
                
                with col2:
                    if st.button("Return", key=f"return_quick_{idx}"):
                        success, message = library.return_book(book['transaction_id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("You have no books to return.")
    
    # ==================== VIEW ALL ISSUED BOOKS ====================
    elif page == "View All Issued Books":
        st.title("📋 All Issued Books")
        
        issued_books = library.get_issued_books()
        
        if issued_books:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_user = st.text_input("Filter by user (leave empty for all):", "")
            with col2:
                show_overdue = st.checkbox("Show only overdue books")
            
            # Apply filters
            filtered_books = issued_books
            if filter_user:
                filtered_books = [b for b in filtered_books if filter_user.lower() in b['user'].lower()]
            if show_overdue:
                filtered_books = [b for b in filtered_books if b['days_remaining'] < 0]
            
            if filtered_books:
                # Create dataframe
                books_data = []
                for book in filtered_books:
                    status = "⚠️ OVERDUE" if book['days_remaining'] < 0 else "✅ ON TIME"
                    books_data.append({
                        'User': book['user'],
                        'Book': book['book'],
                        'Issue Date': book['issue_date'],
                        'Due Date': book['due_date'],
                        'Days Remaining': book['days_remaining'],
                        'Status': status
                    })
                
                df = pd.DataFrame(books_data)
                df.index = df.index + 1
                st.dataframe(df, use_container_width=True)
                st.success(f"Total {len(filtered_books)} issued books matching filters")
            else:
                st.info("No issued books match your filters.")
        else:
            st.info("No books have been issued yet.")
    
    # ==================== ADD NEW BOOK (ADMIN) ====================
    elif page == "Add New Book (Admin)":
        if st.session_state.username == "admin":
            st.title("➕ Add New Book")
            
            col1, col2 = st.columns(2)
            
            with col1:
                book_name = st.text_input("Book Name:")
            
            with col2:
                num_copies = st.number_input("Number of Copies:", min_value=1, value=1)
            
            if st.button("Add Book"):
                success, message = library.add_new_book(book_name, num_copies)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            
            st.divider()
            st.subheader("Current Books in Library")
            
            books_data = []
            for book_name, info in library.data['books'].items():
                books_data.append({
                    'Book Name': book_name,
                    'Total Copies': info['total_copies'],
                    'Available': info['available_copies'],
                    'Issued': info['total_copies'] - info['available_copies']
                })
            
            df = pd.DataFrame(books_data)
            df.index = df.index + 1
            st.dataframe(df, use_container_width=True)
        else:
            st.error("❌ Admin access only. Please login as admin.")
