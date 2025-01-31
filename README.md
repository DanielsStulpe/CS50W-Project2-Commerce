# CS50 Web - Project 2 - Commerce

## Overview
Commerce is an eBay-like e-commerce auction site built with Django. Users can create auction listings, place bids, comment on listings, and add listings to a watchlist. The platform supports user authentication, category-based listing organization, and an admin interface for managing listings, bids, and comments.

## Features
- User authentication (register, login, logout)
- Create auction listings with title, description, starting bid, image URL, and category
- View all active listings on the homepage
- Individual listing pages with details and bidding functionality
- Add or remove items from a watchlist
- Place bids with validation for the highest bid
- Close auctions for listings created by the user
- Display the winning bidder on closed auctions
- Commenting system for each listing
- Browse listings by category
- Django Admin interface for site management

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/commerce.git
   cd commerce
   ```
2. Apply migrations:
   ```sh
   python manage.py makemigrations auctions
   python manage.py migrate
   ```
3. Create a superuser (optional):
   ```sh
   python manage.py createsuperuser
   ```
4. Run the development server:
   ```sh
   python manage.py runserver
   ```
5. Open a web browser and navigate to `http://127.0.0.1:8000/`

## Usage
- Register an account and log in
- Create new auction listings
- Browse active listings and place bids
- Manage your watchlist
- Close auctions if you are the listing creator
- Add comments to auction listings
- View listings by category

## Technologies Used
- Django (Python Web Framework)
- SQLite (Database)
- Bootstrap (CSS Framework)

## License
This project is part of CS50’s Web Programming course and is intended for educational purposes.

