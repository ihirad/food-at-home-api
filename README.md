# Food At Home API

Food At Home API is a backend server to support pantry and recipe management. The mission of the app is to reduce food waste to ensure you always have food at home. The backend server manages pantry tracking with expiration dates, saves recipes, recipe search, and creates shopping notes.


## Setup & Installation

### 1. Clone the Repository
First, open your terminal and navigate to the directory where you want to store the project.  
Now, run the following commands:
```sh
git clone https://github.com/ihirad/food-at-home-api.git
cd food-at-home-api
```
This will download the project files and move you into the project directory.

### 2. Set Up the Virtual Environment
To ensure all dependencies are installed in an isolated environment, set up a **virtual environment**.

On Mac/Linux:
```sh
python -m venv venv
source venv/bin/activate
```

On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
| Dependency         | Version  | Description |
|--------------------|----------|-------------|
| Python | 3.12+   | Programming Language |
| PostgreSQL             | Latest | Database |

Now, install the remaining dependencies by running:
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file and add the following:
```ini
SPOONACULAR_ID=your_spoonacularID
SQLALCHEMY_DATABASE_URI==postgresql://your_username:your_password@localhost/your_database_name
SQLALCHEMY_TEST_DATABASE_URI=postgresql://your_username:your_password@localhost/your_test_database_name
SECRET_KEY=your_secret_key
```

### 5. Set Up the Database
Open PostgreSQL in the terminal:
```sh
psql -U postgres
```
Create a test database
```sh
CREATE DATABASE <your_test_database_name>
```
Create the main local database
```sh
CREATE DATABASE <your_database_name>
```
Connect to a database
```sh
\c <your_database_name>
```
quit
```sh
/q
```
Run the database migrations:
```sh
flask db upgrade
```

### 6. Run the Server
```sh
flask run
```
The API should now be running at: **`http://127.0.0.1:5000/`**  

---

## API Endpoints

| **Category**         | **Method** | **Endpoint**               | **Description** |
|----------------------|-----------|----------------------------|----------------|
| **Ingredients**      | GET       | `/ingredients`             | Fetch all ingredients |
|                      | POST      | `/ingredients`             | Add a new ingredient |
|                      | PUT       | `/ingredients/<id>`        | Update an ingredient |
|                      | DELETE    | `/ingredients/<id>`        | Remove an ingredient |
| **User Ingredients** | GET       | `/user_ingredients`        | Get user-specific ingredients |
|                      | POST      | `/user_ingredients`        | Add an ingredient for a user |
| **Recipes**         | GET       | `/recipes`                 | Get all recipes |
|                      | POST      | `/recipes`                 | Add a new recipe |
|                      | PUT       | `/recipes/<id>`            | Update a recipe |
|                      | DELETE    | `/recipes/<id>`            | Remove a recipe |
| **Users**           | POST      | `/users/register`          | Register a user |
|                      | POST      | `/users/login`             | Log in a user |
|                      | GET       | `/users/<id>`              | Get user profile |
| **Shopping Notes**   | GET       | `/notes`                   | Get all notes |
|                      | POST      | `/notes`                   | Add a new note |
|                      | DELETE    | `/notes/<id>`              | Remove a note |