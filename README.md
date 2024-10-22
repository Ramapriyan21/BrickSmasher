# BrickSmasher - VHS Movie Rental System

BrickSmasher is a web application designed for a movie rental chain that revives the nostalgia of renting VHS tapes. Store employees can manage customer accounts, movie inventory, and rental processes through this system.

## Features

- **Account Creation**: Create customer accounts with unique email addresses.
- **Movie Management**: Add new movies, track inventory, and update stock.
- **Rent/Return Movies**: Manage movie rentals and returns with validation to ensure no more than 3 movies are rented at once.

## Requirements

To run this project, you need Python and the following libraries:

- Python 3.x
- `Django 4.x`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/bricksmasher.git
    cd bricksmasher
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Migrate the database:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser for accessing the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

5. Run the server:
    ```bash
    python manage.py runserver
    ```

6. Access the application at:
    ```bash
    http://127.0.0.1:8000/
    ```

## Pages Overview

- **Home**: Main menu with links to account creation, movie management, and rent/return pages.
- **Account Creation**: Form for creating customer accounts with error handling for duplicate emails.
- **Manage Movies**: View, add, and update the stock of movies.
- **Rent/Return Movies**: Rent and return movies for customers based on their email, with rental limits.

## AJAX Endpoints

- **Manage Users (`/dbUser/`)**: Handle user account creation and lookup via AJAX.
- **Manage Movies (`/dbMovie/`)**: Add new movies or update stock via AJAX.
- **Manage Rentals (`/dbRent/`)**: Rent or return movies using AJAX.

## Available Features

- **Account Creation**: Employees can create customer accounts and manage them.
- **Movie Management**: Employees can add new movies, update movie stock, and view inventory.
- **Rental System**: Customers can rent and return VHS tapes with validation to ensure no more than 3 movies are rented at a time.

## Customization

You can expand the system by adding more management features, such as integrating a search functionality, or improving the rental system to include a rental history feature. You can also integrate other types of media for rental, such as DVDs or Blu-rays.

## Known Issues

- The app requires a stable internet connection for running Django-based AJAX features.
