# Point of Sale (POS) System using SQLite3

## 📌 Overview
This is a simple yet efficient **Point of Sale (POS) System** built with **Python and SQLite3**. It provides essential features to manage products, search for items, edit product details, and remove products from the database. The system follows a modular architecture, making it easy to maintain and expand.

## ✨ Features
- **Add Product**: Admin can add new products with details like name, brand, code, price, and unit.
- **View Products**: Display all available products in the database.
- **Search Products**: Search by product name, brand, or code.
- **Edit Product**: Update product details based on name, brand, or code.
- **Delete Product**: Remove a product and automatically reorder the product IDs sequentially.
- **Clear Screen Support**: Keeps the interface clean for better readability.
- **Modular Code Structure**: Organized into multiple files for better maintainability.

## 🏗 Project Structure
```
kasir_app/
│── main.py          # Main file to run the application
│── db.py            # Database initialization and connection handling
│── produk.py        # CRUD operations for product management
│── utils.py         # Utility functions like clear_screen
│── kasir.db         # SQLite3 database file (generated automatically)
```

## ⚙️ Installation & Usage
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```
### 2️⃣ Install Python (if not installed)
Ensure you have **Python 3.x** installed. Check with:
```bash
python --version
```
### 3️⃣ Run the Program
```bash
python main.py
```

## 🛠 Dependencies
This project runs on standard Python libraries, so no additional installation is required.

## 📌 How to Use
1. Run `python main.py` to start the POS system.
2. Choose an option from the menu:
   - **1**: Add a new product
   - **2**: View all products
   - **3**: Search for a product
   - **4**: Edit an existing product
   - **5**: Delete a product
   - **6**: Exit the application

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## 🌟 Acknowledgments
Special thanks to all open-source contributors and Python developers who inspired this project.
