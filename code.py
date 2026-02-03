import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class Library:
    """Advanced Library Management System with multiple copies support"""
    
    def __init__(self, data_file='library_data.json'):
        self.data_file = data_file
        self.max_borrow_days = 15
        self.data = self.load_data()
        
    def load_data(self) -> Dict:
        """Load library data from JSON file or initialize empty structure"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return self.initialize_default_data()
        return self.initialize_default_data()
    
    def initialize_default_data(self) -> Dict:
        """Initialize default library data"""
        return {
            'books': {
                'The Great Gatsby': {'total_copies': 3, 'available_copies': 3},
                'To Kill a Mockingbird': {'total_copies': 2, 'available_copies': 2},
                '1984': {'total_copies': 3, 'available_copies': 3},
                'Pride and Prejudice': {'total_copies': 2, 'available_copies': 2},
                'The Catcher in the Rye': {'total_copies': 2, 'available_copies': 2},
                'Brave New World': {'total_copies': 3, 'available_copies': 3}
            },
            'issued_books': {}  # Format: {transaction_id: {user, book, issue_date, due_date}}
        }
    
    def save_data(self):
        """Save library data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def get_available_books(self) -> Dict:
        """Get all available books with copy information"""
        available = {}
        for book, info in self.data['books'].items():
            if info['available_copies'] > 0:
                available[book] = info
        return available
    
    def get_issued_books(self) -> List[Dict]:
        """Get all issued books with details"""
        issued_list = []
        for trans_id, details in self.data['issued_books'].items():
            issued_list.append({
                'transaction_id': trans_id,
                'user': details['user'],
                'book': details['book'],
                'issue_date': details['issue_date'],
                'due_date': details['due_date'],
                'days_remaining': self.calculate_days_remaining(details['due_date'])
            })
        return issued_list
    
    def issue_book(self, user: str, book_name: str) -> Tuple[bool, str]:
        """Issue a book to a user"""
        if book_name not in self.data['books']:
            return False, f"Book '{book_name}' not found in library."
        
        if self.data['books'][book_name]['available_copies'] <= 0:
            return False, f"No copies of '{book_name}' available."
        
        # Create transaction
        issue_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        due_date = (datetime.now() + timedelta(days=self.max_borrow_days)).strftime('%Y-%m-%d')
        trans_id = f"{user}_{book_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Update data
        self.data['books'][book_name]['available_copies'] -= 1
        self.data['issued_books'][trans_id] = {
            'user': user,
            'book': book_name,
            'issue_date': issue_date,
            'due_date': due_date
        }
        
        self.save_data()
        return True, f"Book '{book_name}' issued successfully. Return by {due_date}"
    
    def return_book(self, transaction_id: str) -> Tuple[bool, str]:
        """Return a book using transaction ID"""
        if transaction_id not in self.data['issued_books']:
            return False, "Transaction ID not found."
        
        details = self.data['issued_books'][transaction_id]
        book_name = details['book']
        
        # Update data
        self.data['books'][book_name]['available_copies'] += 1
        del self.data['issued_books'][transaction_id]
        
        self.save_data()
        return True, f"Book '{book_name}' returned successfully."
    
    def get_user_borrowed_books(self, user: str) -> List[Dict]:
        """Get all books borrowed by a specific user"""
        user_books = []
        for trans_id, details in self.data['issued_books'].items():
            if details['user'] == user:
                days_remaining = self.calculate_days_remaining(details['due_date'])
                user_books.append({
                    'transaction_id': trans_id,
                    'book': details['book'],
                    'issue_date': details['issue_date'],
                    'due_date': details['due_date'],
                    'days_remaining': days_remaining,
                    'is_overdue': days_remaining < 0
                })
        return user_books
    
    def calculate_days_remaining(self, due_date_str: str) -> int:
        """Calculate days remaining until due date"""
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        days_remaining = (due_date - datetime.now()).days
        return days_remaining
    
    def add_new_book(self, book_name: str, copies: int) -> Tuple[bool, str]:
        """Add a new book to the library"""
        if book_name in self.data['books']:
            return False, f"Book '{book_name}' already exists."
        
        self.data['books'][book_name] = {
            'total_copies': copies,
            'available_copies': copies
        }
        self.save_data()
        return True, f"Book '{book_name}' added with {copies} copies."


class User:
    """User class for library system"""
    
    def __init__(self, username: str):
        self.username = username
    
    def get_username(self) -> str:
        return self.username


if __name__ == "__main__":
    # Example usage
    lib = Library()
    print("Library initialized successfully!")

    while True:
        print("\nMenu:")
        print("1. Display available books")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            library.display_available_books()
        elif choice == '2':
            book_name = student.request_book()
            library.borrow_book(book_name)
        elif choice == '3':
            book_name = student.return_book()
            library.return_book(book_name)
        elif choice == '4':
            print("Thank you for using the library management system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")  

    