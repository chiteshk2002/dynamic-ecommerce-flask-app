# SneakPeak – Flask eCommerce Store

This is my submission for IFQ557 Assignment 2: Solution.  
**SneakPeak** is an online sneaker store that allows customers to browse exclusive sneakers, view details, add them to a shopping basket, and complete a purchase using a secure checkout form.

---

## 🔧 Technologies Used

- Python + Flask
- Flask-WTF (WTForms)
- Flask-SQLAlchemy (ORM)
- SQLite (ecommerce.db)
- HTML5 + Bootstrap 5

---

## 📁 Project Structure

```
/sneakpeak_assignment2/
│
├── app.py              # Main Flask application
├── models.py           # Database models
├── forms.py            # Checkout form using WTForms
├── templates/          # HTML pages (Jinja2)
├── static/             # CSS + images
├── instance/
│   └── ecommerce.db    # Preloaded SQLite database
└── README.md           # Project overview
```

---

## 🚀 Running the App

1. Make sure you have Flask installed:
   ```
   python3 -m pip install Flask Flask-WTF Flask-SQLAlchemy email-validator
   ```

2. Run the application:
   ```
   python3 app.py
   ```

## 📦 Notes

- This project uses a pre-populated SQLite database (`ecommerce.db`) for testing.
- No external dependencies outside standard Flask extensions.
- The `venv/` folder is intentionally excluded as per submission instructions.
- A full 4-minute demo video is submitted separately under Assignment 2: Video Submission.

---

**Author:** Chitesh Kolakaleti  
**Unit:** IFQ557 – Rapid Web Development  

