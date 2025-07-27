# 📚 My Book Library

A beautiful, simple desktop application for organizing your personal book collection. Perfect for book lovers who want an easy way to track their reading journey!

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- 📖 **Easy Book Management** - Add books with title, author, genre, and page count
- 📊 **Reading Progress Tracking** - Track status: Want to Read → Currently Reading → Finished
- ⭐ **Personal Ratings** - Rate your books from 1-5 stars
- 📝 **Personal Notes** - Add your thoughts and reviews
- 🔍 **Smart Search & Filter** - Find books instantly by title or author
- 📥 **CSV Import** - Import your existing book lists
- 📤 **CSV Export** - Backup and share your library
- 📈 **Reading Statistics** - See your reading progress at a glance
- 🎨 **Beautiful Interface** - Warm, library-like design that's easy on the eyes

## 🖼️ Screenshots

### Main Library View
The clean, organized view of your book collection with easy filtering options.

### Add New Book
Simple form to add books to your collection - no complicated fields!

### Reading Statistics
Track your reading progress with beautiful visual statistics.

## 🚀 Quick Start

### Option 1: Download and Run
1. **Download** the `book_library.py` file
2. **Double-click** to run (if Python is installed)
3. **Start adding your books!**

### Option 2: Clone Repository
```bash
git clone https://github.com/yourusername/book-library-app.git
cd book-library-app
python book_library.py
```

## 💻 System Requirements

- **Python 3.6 or higher** (most computers have this already)
- **No additional installations needed!** Uses only Python built-in libraries

### Check if you have Python:
```bash
python --version
```

If you don't have Python, download it free from [python.org](https://www.python.org/downloads/)

## 📖 How to Use

### Adding Your First Book
1. Click **"➕ Add New Book"**
2. Fill in the book details (only title and author are required)
3. Choose reading status and add a rating if you've read it
4. Click **"💾 Add to My Library"**

### Organizing Your Collection
- **Filter books** by reading status using the sidebar buttons
- **Search** for specific books using the search feature
- **Edit** any book by clicking the "✏️ Edit" button
- **Mark books as finished** when you complete them

### Import Your Existing List
1. Prepare a CSV file with columns: `title, author, genre, pages, status, rating, notes`
2. Click **"📥 Import from CSV"**
3. Select your file and watch your library populate!

## 🎯 Perfect For

- 📚 **Book enthusiasts** who want to organize their personal collection
- 👵 **Older readers** who prefer simple, clear interfaces
- 📱 **Anyone** who wants a lightweight alternative to complex book management software
- 🏠 **Home libraries** that need better organization
- 📖 **Reading groups** who want to track member progress

## 🔧 Technical Details

- **Database**: SQLite (lightweight, no server needed)
- **GUI Framework**: tkinter (cross-platform, built into Python)
- **Data Format**: CSV import/export for compatibility
- **Storage**: Local database file (`my_books.sqlite`)

## 🤝 Contributing

Found a bug or want to add a feature? I'd love your help!

1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Ideas for Contributions
- 🌐 Add online book lookup (Google Books API)
- 📱 Create a mobile-friendly version
- 🎨 Additional themes and color schemes
- 📊 More detailed reading statistics
- 🔒 Book lending tracker
- 📚 Series/collection grouping

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 🙏 Acknowledgments

- Built with ❤️ for book lovers everywhere
- Inspired by the need for simple, effective personal organization tools
- Special thanks to the Python community for amazing open-source libraries

## 📞 Support

Having issues? Here are some solutions:

### Common Issues
**App won't start?**
- Make sure Python 3.6+ is installed
- Try running from command line: `python book_library.py`

**Can't import CSV?**
- Check that your CSV has the correct column headers
- Make sure the file encoding is UTF-8

**Database issues?**
- Delete the `my_books.sqlite` file to start fresh
- Make sure you have write permissions in the app directory

### Get Help
- 🐛 **Report bugs**: [Open an issue](https://github.com/keym11/shelf/issues)
- 💡 **Feature requests**: [Start a discussion](https://github.com/keym11/shelf/discussions)
- 📧 **Contact**: [saud69262@gmail.com]

## ⭐ Show Your Support

If this app helps you organize your book collection, please give it a star! ⭐

It really helps others discover the project and motivates continued development.

---

**Happy Reading!** 📚✨

