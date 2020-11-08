# Coffee Shop Full Stack

## Auth0 account
```
AUTH0_DOMAIN = 'coffee-shop-ud.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'drink'
```

There is a Postman collection that tests the APIs. Some of those tests may fail because the token expired. I have created two dummy accounts that you can use to get fresh tokens.

### Manager Account
```
User: gandalf@shire.com
password: MyPrecious123

```

### Barista Account
```
User: bilbobagins@shire.com
password: MyPrecious123

```

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application now can:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.


## About the Stack

### Backend

The `./backend` directory contains a completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. The endpoints are complete, Auth0 has been configured, and integrated for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)
