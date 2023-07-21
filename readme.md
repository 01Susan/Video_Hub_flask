# Video Hub


Video Hub is a web application that enables users to manage and organize videos in a MySQL database. This application is built using Python 3.10 and utilizes the power of MySQL for efficient data storage and retrieval.

## Table of Contents

- [Introduction](#video-hub)
- [Used Technologies](#used-technologies)
- [Setup](#setup)
  - [Database Configuration](#database-configuration)
  - [Install Dependencies](#install-dependencies)
  - [Run the Application](#run-the-application)
- [API Endpoints](#api-endpoints)
- [Postman Collection](#postman-collection)
- [Contributing](#contributing)
- [License](#license)

## Used Technologies

- MySQL: The database management system used to store and organize video data.
- Python 3.10: The programming language used to build the Video Hub application.

## Setup

To set up and run the Video Hub application, follow the steps below:

### Database Configuration

1. Rename `.env.sample` to `.env` and open the `.env` file.
2. Configure the database connection parameters inside the `.env` file:
   - Provide the appropriate `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
   - Ensure that the database name (`DB_NAME`) provided already exists on the MySQL server. If not, you can create it using the SQL query provided in the `collections/database.sql` file.

### Install Dependencies

1. Open your terminal or command prompt and navigate to the project directory.
2. (Optional) Create a new Python environment:
   ```
   python -m venv myenv
   ```
3. Activate the newly created environment:
   - On Windows:
     ```
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```
4. Install the required packages from `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

### Run the Application

1. Ensure your MySQL server is running and accessible.
2. In the terminal or command prompt, navigate to the project directory.
3. Run the `main.py` file to start the server:
   ```
   python main.py
   ```

## API Endpoints

Video Hub provides a set of API endpoints that enable users to manage videos efficiently. These endpoints include standard CRUD (Create, Read, Update, Delete) operations. For a comprehensive list of available endpoints and their usage, please refer to the Postman collection in the `collections` folder.

## Postman Collection

The `collections` folder contains a Postman collection with pre-configured API requests for interacting with the Video Hub server. You can import this collection into your Postman application to get started quickly.


