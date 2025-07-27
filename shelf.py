import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import csv
from datetime import datetime
import os

class BookLibrary:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📚 My Book Library")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f4e6')  # Warm, book-like color
        
        # Database setup
        self.db_path = "my_books.sqlite"
        self.setup_database()
        
        # Current view
        self.current_view = "all"
        self.search_term = ""
        
        self.setup_ui()
        self.load_books()
        
    def setup_database(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create books table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                pages INTEGER,
                status TEXT DEFAULT 'Want to Read',
                rating INTEGER DEFAULT 0,
                notes TEXT,
                date_added TEXT,
                date_finished TEXT
            )
        ''')
        self.conn.commit()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#8B4513', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📚 My Personal Library", 
                              font=('Georgia', 28, 'bold'), bg='#8B4513', fg='white')
        title_label.pack(expand=True)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f8f4e6')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left sidebar for controls
        self.setup_sidebar(main_frame)
        
        # Right area for book display
        self.setup_book_area(main_frame)
        
    def setup_sidebar(self, parent):
        sidebar_frame = tk.Frame(parent, bg='#deb887', width=350, relief='raised', bd=3)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar_frame.pack_propagate(False)
        
        # Quick stats
        stats_label = tk.Label(sidebar_frame, text="📊 My Reading Stats", 
                              font=('Georgia', 16, 'bold'), bg='#deb887', fg='#8B4513')
        stats_label.pack(pady=(20, 10))
        
        self.stats_frame = tk.Frame(sidebar_frame, bg='#deb887')
        self.stats_frame.pack(fill=tk.X, padx=20)
        
        # Action buttons
        actions_label = tk.Label(sidebar_frame, text="📖 Quick Actions", 
                                font=('Georgia', 16, 'bold'), bg='#deb887', fg='#8B4513')
        actions_label.pack(pady=(30, 10))
        
        button_style = {
            'font': ('Georgia', 12, 'bold'),
            'fg': 'white',
            'bd': 0,
            'pady': 15,
            'cursor': 'hand2',
            'width': 25
        }
        
        add_book_btn = tk.Button(sidebar_frame, text="➕ Add New Book", 
                                bg='#228B22', command=self.add_book_dialog, **button_style)
        add_book_btn.pack(pady=8, padx=20, fill=tk.X)
        
        search_btn = tk.Button(sidebar_frame, text="🔍 Search Books", 
                              bg='#4169E1', command=self.search_dialog, **button_style)
        search_btn.pack(pady=8, padx=20, fill=tk.X)
        
        import_btn = tk.Button(sidebar_frame, text="📥 Import from CSV", 
                              bg='#FF8C00', command=self.import_books, **button_style)
        import_btn.pack(pady=8, padx=20, fill=tk.X)
        
        export_btn = tk.Button(sidebar_frame, text="📤 Export My Books", 
                              bg='#DC143C', command=self.export_books, **button_style)
        export_btn.pack(pady=8, padx=20, fill=tk.X)
        
        # Filter buttons
        filter_label = tk.Label(sidebar_frame, text="🎯 Filter Books", 
                               font=('Georgia', 16, 'bold'), bg='#deb887', fg='#8B4513')
        filter_label.pack(pady=(30, 10))
        
        filter_style = {
            'font': ('Georgia', 10, 'bold'),
            'fg': 'white',
            'bd': 0,
            'pady': 10,
            'cursor': 'hand2',
            'width': 25
        }
        
        all_btn = tk.Button(sidebar_frame, text="📚 All Books", 
                           bg='#708090', command=lambda: self.filter_books("all"), **filter_style)
        all_btn.pack(pady=4, padx=20, fill=tk.X)
        
        reading_btn = tk.Button(sidebar_frame, text="📖 Currently Reading", 
                               bg='#32CD32', command=lambda: self.filter_books("reading"), **filter_style)
        reading_btn.pack(pady=4, padx=20, fill=tk.X)
        
        finished_btn = tk.Button(sidebar_frame, text="✅ Finished", 
                                bg='#9932CC', command=lambda: self.filter_books("finished"), **filter_style)
        finished_btn.pack(pady=4, padx=20, fill=tk.X)
        
        want_btn = tk.Button(sidebar_frame, text="❤️ Want to Read", 
                            bg='#FF6347', command=lambda: self.filter_books("want"), **filter_style)
        want_btn.pack(pady=4, padx=20, fill=tk.X)
        
    def setup_book_area(self, parent):
        # Books display area
        self.books_frame = tk.Frame(parent, bg='#f8f4e6')
        self.books_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header for book area
        books_header = tk.Frame(self.books_frame, bg='#f8f4e6')
        books_header.pack(fill=tk.X, pady=(0, 20))
        
        self.books_title = tk.Label(books_header, text="📖 All My Books", 
                                   font=('Georgia', 20, 'bold'), bg='#f8f4e6', fg='#8B4513')
        self.books_title.pack(side=tk.LEFT)
        
        self.book_count = tk.Label(books_header, text="", 
                                  font=('Georgia', 14), bg='#f8f4e6', fg='#666')
        self.book_count.pack(side=tk.RIGHT)
        
        # Scrollable frame for books
        canvas = tk.Canvas(self.books_frame, bg='#f8f4e6')
        scrollbar = ttk.Scrollbar(self.books_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f8f4e6')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def update_stats(self):
        # Clear current stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Get statistics
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total_books = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Finished'")
        finished_books = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Currently Reading'")
        reading_books = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Want to Read'")
        want_books = self.cursor.fetchone()[0]
        
        # Display stats
        stats = [
            ("📚 Total Books", total_books, '#4169E1'),
            ("✅ Finished", finished_books, '#228B22'),
            ("📖 Reading", reading_books, '#FF8C00'),
            ("❤️ Want to Read", want_books, '#DC143C')
        ]
        
        for i, (label, count, color) in enumerate(stats):
            stat_frame = tk.Frame(self.stats_frame, bg=color, relief='raised', bd=2)
            stat_frame.pack(fill=tk.X, pady=3)
            
            tk.Label(stat_frame, text=label, font=('Georgia', 10, 'bold'), 
                    bg=color, fg='white').pack()
            tk.Label(stat_frame, text=str(count), font=('Georgia', 14, 'bold'), 
                    bg=color, fg='white').pack()
                    
    def add_book_dialog(self):
        AddBookDialog(self.root, self)
        
    def search_dialog(self):
        search_term = simpledialog.askstring("Search Books", 
                                            "Enter title or author to search:")
        if search_term:
            self.search_term = search_term.lower()
            self.load_books()
        else:
            self.search_term = ""
            self.load_books()
            
    def filter_books(self, filter_type):
        self.current_view = filter_type
        self.load_books()
        
        # Update title
        titles = {
            "all": "📖 All My Books",
            "reading": "📖 Currently Reading",
            "finished": "✅ Books I've Finished",
            "want": "❤️ Books I Want to Read"
        }
        self.books_title.config(text=titles.get(filter_type, "📖 My Books"))
        
    def load_books(self):
        # Clear current books display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Build query based on current view and search
        query = "SELECT * FROM books WHERE 1=1"
        params = []
        
        if self.current_view != "all":
            status_map = {
                "reading": "Currently Reading",
                "finished": "Finished",
                "want": "Want to Read"
            }
            query += " AND status = ?"
            params.append(status_map[self.current_view])
            
        if self.search_term:
            query += " AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ?)"
            params.extend([f"%{self.search_term}%", f"%{self.search_term}%"])
            
        query += " ORDER BY date_added DESC"
        
        self.cursor.execute(query, params)
        books = self.cursor.fetchall()
        
        # Update count
        self.book_count.config(text=f"({len(books)} books)")
        
        # Display books
        if not books:
            no_books_label = tk.Label(self.scrollable_frame, 
                                     text="📭 No books found!\nTry adding some books or changing your filter.", 
                                     font=('Georgia', 16), bg='#f8f4e6', fg='#888',
                                     justify=tk.CENTER)
            no_books_label.pack(expand=True, pady=50)
        else:
            for book in books:
                self.create_book_card(book)
                
        self.update_stats()
        
    def create_book_card(self, book):
        book_id, title, author, genre, pages, status, rating, notes, date_added, date_finished = book
        
        # Main card frame
        card_frame = tk.Frame(self.scrollable_frame, bg='white', relief='raised', bd=2)
        card_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Content frame
        content_frame = tk.Frame(card_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side - book info
        info_frame = tk.Frame(content_frame, bg='white')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title and author
        title_label = tk.Label(info_frame, text=title, font=('Georgia', 16, 'bold'), 
                              bg='white', fg='#2c3e50', anchor='w')
        title_label.pack(fill=tk.X)
        
        author_label = tk.Label(info_frame, text=f"by {author}", font=('Georgia', 12, 'italic'), 
                               bg='white', fg='#7f8c8d', anchor='w')
        author_label.pack(fill=tk.X, pady=(0, 10))
        
        # Details
        details_frame = tk.Frame(info_frame, bg='white')
        details_frame.pack(fill=tk.X)
        
        if genre:
            genre_label = tk.Label(details_frame, text=f"📂 {genre}", font=('Georgia', 10), 
                                  bg='#e8f4fd', fg='#2980b9', padx=8, pady=2)
            genre_label.pack(side=tk.LEFT, padx=(0, 10))
            
        if pages:
            pages_label = tk.Label(details_frame, text=f"📄 {pages} pages", font=('Georgia', 10), 
                                  bg='#fff2e8', fg='#e67e22', padx=8, pady=2)
            pages_label.pack(side=tk.LEFT, padx=(0, 10))
            
        # Status
        status_colors = {
            'Want to Read': '#e74c3c',
            'Currently Reading': '#f39c12',
            'Finished': '#27ae60'
        }
        
        status_frame = tk.Frame(info_frame, bg='white')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = tk.Label(status_frame, text=f"📖 {status}", font=('Georgia', 11, 'bold'), 
                               bg=status_colors.get(status, '#95a5a6'), fg='white', padx=10, pady=5)
        status_label.pack(side=tk.LEFT)
        
        # Rating
        if rating > 0:
            stars = "⭐" * rating
            rating_label = tk.Label(status_frame, text=stars, font=('Georgia', 12), 
                                   bg='white', fg='#f39c12')
            rating_label.pack(side=tk.LEFT, padx=(10, 0))
            
        # Notes preview
        if notes:
            notes_preview = notes[:100] + "..." if len(notes) > 100 else notes
            notes_label = tk.Label(info_frame, text=f"📝 {notes_preview}", font=('Georgia', 9), 
                                  bg='white', fg='#666', anchor='w', justify=tk.LEFT)
            notes_label.pack(fill=tk.X, pady=(10, 0))
            
        # Right side - actions
        actions_frame = tk.Frame(content_frame, bg='white')
        actions_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        edit_btn = tk.Button(actions_frame, text="✏️ Edit", font=('Georgia', 10, 'bold'),
                            bg='#3498db', fg='white', padx=15, pady=8,
                            command=lambda: self.edit_book(book_id))
        edit_btn.pack(pady=2)
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Delete", font=('Georgia', 10, 'bold'),
                              bg='#e74c3c', fg='white', padx=15, pady=8,
                              command=lambda: self.delete_book(book_id, title))
        delete_btn.pack(pady=2)
        
        if status != 'Finished':
            finish_btn = tk.Button(actions_frame, text="✅ Mark Finished", font=('Georgia', 9, 'bold'),
                                  bg='#27ae60', fg='white', padx=10, pady=6,
                                  command=lambda: self.mark_finished(book_id))
            finish_btn.pack(pady=2)
            
    def edit_book(self, book_id):
        EditBookDialog(self.root, self, book_id)
        
    def delete_book(self, book_id, title):
        if messagebox.askyesno("Delete Book", 
                              f"Are you sure you want to delete '{title}'?\nThis cannot be undone!"):
            try:
                self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
                self.conn.commit()
                self.load_books()
                messagebox.showinfo("Success", f"'{title}' has been deleted from your library.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete book: {str(e)}")
                
    def mark_finished(self, book_id):
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("UPDATE books SET status = 'Finished', date_finished = ? WHERE id = ?", 
                              (current_date, book_id))
            self.conn.commit()
            self.load_books()
            messagebox.showinfo("Congratulations!", "📚 Book marked as finished! Great job! 🎉")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")
            
    def import_books(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV file with your books",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    count = 0
                    
                    for row in reader:
                        title = row.get('title', '').strip()
                        author = row.get('author', '').strip()
                        
                        if title and author:
                            genre = row.get('genre', '').strip()
                            pages = row.get('pages', '0')
                            status = row.get('status', 'Want to Read').strip()
                            rating = row.get('rating', '0')
                            notes = row.get('notes', '').strip()
                            
                            # Validate and convert numeric fields
                            try:
                                pages = int(pages) if pages.isdigit() else 0
                            except:
                                pages = 0
                                
                            try:
                                rating = int(rating) if rating.isdigit() and 0 <= int(rating) <= 5 else 0
                            except:
                                rating = 0
                                
                            # Validate status
                            if status not in ['Want to Read', 'Currently Reading', 'Finished']:
                                status = 'Want to Read'
                                
                            current_date = datetime.now().strftime("%Y-%m-%d")
                            
                            self.cursor.execute('''
                                INSERT INTO books (title, author, genre, pages, status, rating, notes, date_added)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (title, author, genre, pages, status, rating, notes, current_date))
                            
                            count += 1
                            
                    self.conn.commit()
                    self.load_books()
                    messagebox.showinfo("Success", f"📚 {count} books imported successfully!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import books: {str(e)}")
                
    def export_books(self):
        file_path = filedialog.asksaveasfilename(
            title="Export your books to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.cursor.execute("SELECT * FROM books ORDER BY title")
                books = self.cursor.fetchall()
                
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['id', 'title', 'author', 'genre', 'pages', 'status', 
                                   'rating', 'notes', 'date_added', 'date_finished'])
                    writer.writerows(books)
                    
                messagebox.showinfo("Success", f"📤 Your books have been exported to:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export books: {str(e)}")
                
    def run(self):
        self.root.mainloop()
        self.conn.close()

class AddBookDialog:
    def __init__(self, parent, library):
        self.library = library
        
        self.window = tk.Toplevel(parent)
        self.window.title("📚 Add New Book to My Library")
        self.window.geometry("500x600")
        self.window.configure(bg='#f8f4e6')
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.window, bg='#8B4513')
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="📚 Add New Book", 
                               font=('Georgia', 18, 'bold'), bg='#8B4513', fg='white')
        header_label.pack(pady=15)
        
        # Form
        form_frame = tk.Frame(self.window, bg='#f8f4e6')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Book title
        tk.Label(form_frame, text="📖 Book Title *", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = tk.Entry(form_frame, font=('Georgia', 12), width=40)
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Author
        tk.Label(form_frame, text="✍️ Author *", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.author_entry = tk.Entry(form_frame, font=('Georgia', 12), width=40)
        self.author_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Genre
        tk.Label(form_frame, text="📂 Genre", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.genre_entry = tk.Entry(form_frame, font=('Georgia', 12), width=40)
        self.genre_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Pages
        tk.Label(form_frame, text="📄 Number of Pages", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.pages_entry = tk.Entry(form_frame, font=('Georgia', 12), width=20)
        self.pages_entry.pack(anchor=tk.W, pady=(0, 15))
        
        # Status
        tk.Label(form_frame, text="📊 Reading Status", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.status_combo = ttk.Combobox(form_frame, 
                                        values=['Want to Read', 'Currently Reading', 'Finished'],
                                        state='readonly', font=('Georgia', 11), width=20)
        self.status_combo.set('Want to Read')
        self.status_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Rating
        tk.Label(form_frame, text="⭐ My Rating (1-5 stars)", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.rating_combo = ttk.Combobox(form_frame, 
                                        values=['0', '1', '2', '3', '4', '5'],
                                        state='readonly', font=('Georgia', 11), width=10)
        self.rating_combo.set('0')
        self.rating_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Notes
        tk.Label(form_frame, text="📝 My Notes", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.notes_text = tk.Text(form_frame, font=('Georgia', 10), width=40, height=4)
        self.notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#f8f4e6')
        button_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(button_frame, text="💾 Add to My Library", 
                            font=('Georgia', 12, 'bold'), bg='#228B22', fg='white',
                            padx=20, pady=10, command=self.save_book)
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(button_frame, text="❌ Cancel", 
                              font=('Georgia', 12, 'bold'), bg='#DC143C', fg='white',
                              padx=20, pady=10, command=self.window.destroy)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Focus on title entry
        self.title_entry.focus()
        
    def save_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        
        if not title or not author:
            messagebox.showwarning("Missing Information", 
                                  "Please enter at least the book title and author!")
            return
            
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        status = self.status_combo.get()
        rating = int(self.rating_combo.get())
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        # Validate pages
        try:
            pages = int(pages) if pages else 0
        except ValueError:
            pages = 0
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_finished = current_date if status == 'Finished' else None
        
        try:
            self.library.cursor.execute('''
                INSERT INTO books (title, author, genre, pages, status, rating, notes, date_added, date_finished)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, genre, pages, status, rating, notes, current_date, date_finished))
            
            self.library.conn.commit()
            self.library.load_books()
            self.window.destroy()
            
            messagebox.showinfo("Success", f"📚 '{title}' has been added to your library! 🎉")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

class EditBookDialog:
    def __init__(self, parent, library, book_id):
        self.library = library
        self.book_id = book_id
        
        # Get book data
        self.library.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        self.book = self.library.cursor.fetchone()
        
        if not self.book:
            messagebox.showerror("Error", "Book not found!")
            return
            
        self.window = tk.Toplevel(parent)
        self.window.title("✏️ Edit Book")
        self.window.geometry("500x600")
        self.window.configure(bg='#f8f4e6')
        self.window.grab_set()
        
        self.setup_ui()
        self.fill_current_data()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.window, bg='#8B4513')
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="✏️ Edit Book Details", 
                               font=('Georgia', 18, 'bold'), bg='#8B4513', fg='white')
        header_label.pack(pady=15)
        
        # Form
        form_frame = tk.Frame(self.window, bg='#f8f4e6')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Book title
        tk.Label(form_frame, text="📖 Book Title *", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = tk.Entry(form_frame, font=('Georgia', 12), width=40)
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Author
        tk.Label(form_frame, text="✍️ Author *", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.author_entry = tk.Entry(form_frame, font=('Georgia', 12), width=40)
        self.author_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Genre
        tk.Label(form_frame, text="📂 Genre", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.genre_entry = tk.Entry(form_frame, font=('Georgia', 12), width=40)
        self.genre_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Pages
        tk.Label(form_frame, text="📄 Number of Pages", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.pages_entry = tk.Entry(form_frame, font=('Georgia', 12), width=20)
        self.pages_entry.pack(anchor=tk.W, pady=(0, 15))
        
        # Status
        tk.Label(form_frame, text="📊 Reading Status", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.status_combo = ttk.Combobox(form_frame, 
                                        values=['Want to Read', 'Currently Reading', 'Finished'],
                                        state='readonly', font=('Georgia', 11), width=20)
        self.status_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Rating
        tk.Label(form_frame, text="⭐ My Rating (1-5 stars)", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.rating_combo = ttk.Combobox(form_frame, 
                                        values=['0', '1', '2', '3', '4', '5'],
                                        state='readonly', font=('Georgia', 11), width=10)
        self.rating_combo.pack(anchor=tk.W, pady=(0, 15))
        
        # Notes
        tk.Label(form_frame, text="📝 My Notes", font=('Georgia', 12, 'bold'),
                bg='#f8f4e6', fg='#8B4513').pack(anchor=tk.W, pady=(0, 5))
        self.notes_text = tk.Text(form_frame, font=('Georgia', 10), width=40, height=4)
        self.notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#f8f4e6')
        button_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(button_frame, text="💾 Save Changes", 
                            font=('Georgia', 12, 'bold'), bg='#228B22', fg='white',
                            padx=20, pady=10, command=self.save_changes)
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(button_frame, text="❌ Cancel", 
                              font=('Georgia', 12, 'bold'), bg='#DC143C', fg='white',
                              padx=20, pady=10, command=self.window.destroy)
        cancel_btn.pack(side=tk.RIGHT)
        
    def fill_current_data(self):
        book_id, title, author, genre, pages, status, rating, notes, date_added, date_finished = self.book
        
        self.title_entry.insert(0, title or '')
        self.author_entry.insert(0, author or '')
        self.genre_entry.insert(0, genre or '')
        self.pages_entry.insert(0, str(pages) if pages else '')
        self.status_combo.set(status or 'Want to Read')
        self.rating_combo.set(str(rating) if rating else '0')
        if notes:
            self.notes_text.insert(1.0, notes)
            
    def save_changes(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        
        if not title or not author:
            messagebox.showwarning("Missing Information", 
                                  "Please enter at least the book title and author!")
            return
            
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        status = self.status_combo.get()
        rating = int(self.rating_combo.get())
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        # Validate pages
        try:
            pages = int(pages) if pages else 0
        except ValueError:
            pages = 0
            
        # Handle date_finished
        date_finished = None
        if status == 'Finished':
            # Check if it was already finished
            if self.book[5] != 'Finished':  # status field
                date_finished = datetime.now().strftime("%Y-%m-%d")
            else:
                date_finished = self.book[9]  # keep existing date_finished
                
        try:
            self.library.cursor.execute('''
                UPDATE books SET title=?, author=?, genre=?, pages=?, status=?, 
                               rating=?, notes=?, date_finished=?
                WHERE id=?
            ''', (title, author, genre, pages, status, rating, notes, date_finished, self.book_id))
            
            self.library.conn.commit()
            self.library.load_books()
            self.window.destroy()
            
            messagebox.showinfo("Success", f"📚 '{title}' has been updated! ✨")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")

if __name__ == "__main__":
    app = BookLibrary()
    app.run()