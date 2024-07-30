# Expense Sharing App

This project is an expense-sharing application that helps users manage and split expenses among groups.

## Installation

### Prerequisites

- **Python**: Make sure you have Python 3.6 or higher installed. [Download Python](https://www.python.org/downloads/).
- **Pip**: Python's package installer. Usually comes with Python.

### Setting Up the Project

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/expense-sharing-app.git
   cd expense-sharing-app

2. **Create a Virtual Environment**
   python -m venv venv

3. **Activate the Virtual Environment**
   venv\Scripts\activate

4. **Install Dependencies**
  pip install -r requirements.txt

**Database Setup**
1. **Initialize the Database**

   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   
2. **Run the Application**
   python run.py

3. **Access the Application**

Open your browser and go to http://127.0.0.1:5000 to access the application
## Usage

1. **Register a New Account**

   Go to the registration page and create a new account.

2. **Create a New Group**

   Navigate to the 'Create Group' page to set up a new group.

3. **Add Expenses**

   Use the 'Create Expense' page to add new expenses and split them among group members.
