# restaurant API backend 

## About

I didn't have enough time to create a complete website using Vue.js, so I created a restaurant management system that uploads the available food items (breakfast, lunch, dessert, etc....) and sends only the name of the item and stores it in the database under the name "type".
Also, the person responsible for the restaurant raises the food dishes available to them and sends the name of the dish "name" and the type to which it belongs "rate_it", which is the 'ID' number of the item to which it belongs, and the person responsible for the restaurant can amend or delete items and dishes.
As for restaurant customers, they can retrieve lists of food items and dishes
There are two ranks, the first has the right to make all modifications (Manager), and the second has the right to read data only (Barista)
Most of the ideas wrote their own codes for previous projects, so some of the codes did not need to be modified, such as user verification, and others I modified to suit my idea, and in the future, God willing, I will create the front end and develop the project further

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

## Running the server

To run the server, execute:
```
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://capstone-for-nd-udacity.onrender.com/

The live application can only be used to generate tokens via Auth0 [login here](https://moaz.uk.auth0.com/authorize?audience=restaurant&response_type=token&client_id=DribS2kVibf9SFkcTFNmOoTWQTNA1WwD&redirect_uri=https://capstone-for-nd-udacity.onrender.com/), the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.


## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Two roles are assigned to this API: 'Barista' and 'Manager'. The 'Barista' role is assigned by default when someone creates an account
from the login page, while the 'Manager' role is already pre-assigned to certain users.


A token needs to be passed to each endpoint. 
The following only works for / endpoints:
The token can be retrived by following these steps:
1. Go to [login here](https://moaz.uk.auth0.com/authorize?audience=restaurant&response_type=token&client_id=DribS2kVibf9SFkcTFNmOoTWQTNA1WwD&redirect_uri=https://capstone-for-nd-udacity.onrender.com/),
2. Click on Login and enter any credentials into the Auth0 login page. The role is automatically assigned by Auth0. 
   Alternatively, sample account that has already been created can be used:
   -Barista account
   ```
      User: barista2@udacity.com
      password: udacity123*
    ```
    -Manager account
    ```
      User: restaurant_manager@udacity.com
      password: udacity123*
    ```

#### GET '/food-items-detail'
Returns all the food items in the restaurant and the success value
```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://capstone-for-nd-udacity.onrender.com/food-items-detail
```

OR
```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/food-items-detail
```

Sample response output:
```
{
    "food_items": [
        {
            "id": 1,
            "type": "fast food"
        },
        {
            "id": 2,
            "type": "lunch"
        },
        {
            "id": 3,
            "type": "dinner"
        },
        {
            "id": 4,
            "type": "refreshment"
        },
        {
            "id": 5,
            "type": "desalination"
        }
    ],
    "success": true
}
```

#### POST '/food-items'
Return all food items in the restaurant in addition to the new items and the value of success
```
curl https://capstone-for-nd-udacity.onrender.com/food-items -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"type": "sundae"}'
```

OR

```
curl http://localhost:5000/food-items -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"type": "sundae"}'
```

Sample response output:
```
{
    "food_items": [
        {
            "id": 1,
            "type": "fast food"
        },
        {
            "id": 2,
            "type": "lunch"
        },
        {
            "id": 3,
            "type": "dinner"
        },
        {
            "id": 4,
            "type": "refreshment"
        },
        {
            "id": 5,
            "type": "desalination"
        },
        {
            "id": 6,
            "type": "sundae"
        }
    ],
    "success": true
}
```

#### PATCH '/food-items/\<int:id\>'
Returns all items in the restaurant, in addition to the updated items and the success value
Sample curl:
```
curl https://capstone-for-nd-udacity.onrender.com/food-items/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"type":"Eat fast"}'
```

OR

```
curl http://localhost:5000/food-items/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"type":"Eat fast"}'
```

Sample response output:
```
{
    "food_items": [
        {
            "id": 1,
            "type": "Eat fast"
        },
        {
            "id": 2,
            "type": "lunch"
        },
        {
            "id": 3,
            "type": "dinner"
        },
        {
            "id": 4,
            "type": "refreshment"
        },
        {
            "id": 5,
            "type": "desalination"
        },
        {
            "id": 6,
            "type": "sundae"
        }
    ],
    "success": true
}
```

#### DELETE '/food-items/\<int:id\>'
Returns the ID number of the item to be deleted along with a success status
```
curl https://capstone-for-nd-udacity.onrender.com/food-items/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```

OR

```
curl http://localhost:5000/food-items/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```

Sample response output:
```
{
    "delete": 1,
    "success": true
}
```

#### GET '/the-food-detail'
Returns all food dishes in the restaurant and the success value
```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://capstone-for-nd-udacity.onrender.com/the-food-detail
```

OR

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/the-food-detail
```

Sample response output:
```
{
    "success": true,
    "the_food": [
        {
            "id": 1,
            "name": "Cheese pies",
            "type": "fast food"
        },
        {
            "id": 2,
            "name": "Falafel",
            "type": "fast food"
        },
        {
            "id": 3,
            "name": "Shawarma",
            "type": "fast food"
        },
        {
            "id": 4,
            "name": "Mansaf meat",
            "type": "lunch"
        },
        {
            "id": 5,
            "name": "Grilled kibbeh",
            "type": "lunch"
        },
        {
            "id": 6,
            "name": "Fava Beans",
            "type": "dinner"
        },
        {
            "id": 7,
            "name": "Homs rosary",
            "type": "dinner"
        },
        {
            "id": 8,
            "name": "Mango juice",
            "type": "refreshment"
        },
        {
            "id": 9,
            "name": "Soft drinks",
            "type": "refreshment"
        },
        {
            "id": 10,
            "name": "cupcake",
            "type": "desalination"
        }
    ]
}
```

#### POST '/the-food'
Return all food dishes in the restaurant, in addition to the new dishes and the value of success
```
curl https://capstone-for-nd-udacity.onrender.com/the-food -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"meet", "rate_it": "2"}'
```

OR

```
curl http://localhost:5000/the-food -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"meet", "rate_it": "2"}'
```

Sample response output:
```
{
    "success": true,
    "the_food": [
        {
            "id": 1,
            "name": "Cheese pies",
            "type": "fast food"
        },
        {
            "id": 2,
            "name": "Falafel",
            "type": "fast food"
        },
        {
            "id": 3,
            "name": "Shawarma",
            "type": "fast food"
        },
        {
            "id": 4,
            "name": "Mansaf meat",
            "type": "lunch"
        },
        {
            "id": 5,
            "name": "Grilled kibbeh",
            "type": "lunch"
        },
        {
            "id": 6,
            "name": "Fava Beans",
            "type": "dinner"
        },
        {
            "id": 7,
            "name": "Homs rosary",
            "type": "dinner"
        },
        {
            "id": 8,
            "name": "Mango juice",
            "type": "refreshment"
        },
        {
            "id": 9,
            "name": "Soft drinks",
            "type": "refreshment"
        },
        {
            "id": 10,
            "name": "cupcake",
            "type": "desalination"
        },
        {
            "id": 11,
            "name": "meet",
            "type": "lunch"
        }
    ]
}
```

#### PATCH 'the-food/\<int:id\>'
Returns all the dishes in the restaurant in addition to the updated dishes and the success value
Sample curl:
```
curl https://capstone-for-nd-udacity.onrender.com/the-food/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Cheese", "rate_it": "2"}'
```

OR

```
curl http://localhost:5000/the-food/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Cheese", "rate_it": "2"}'
```

Sample response output:
```
{
    "success": true,
    "the_food": [
        {
            "id": 1,
            "name": "Cheese",
            "type": "lunch"
        },
        {
            "id": 2,
            "name": "Falafel",
            "type": "Eat fast"
        },
        {
            "id": 3,
            "name": "Shawarma",
            "type": "Eat fast"
        },
        {
            "id": 4,
            "name": "Mansaf meat",
            "type": "lunch"
        },
        {
            "id": 5,
            "name": "Grilled kibbeh",
            "type": "lunch"
        },
        {
            "id": 6,
            "name": "Fava Beans",
            "type": "dinner"
        },
        {
            "id": 7,
            "name": "Homs rosary",
            "type": "dinner"
        },
        {
            "id": 8,
            "name": "Mango juice",
            "type": "refreshment"
        },
        {
            "id": 9,
            "name": "Soft drinks",
            "type": "refreshment"
        },
        {
            "id": 10,
            "name": "cupcake",
            "type": "desalination"
        },
        {
            "id": 11,
            "name": "meet",
            "type": "lunch"
        }
    ]
}
```

#### DELETE '/the-food/\<int:id\>'
Returns the ID number of the item to be deleted along with a success status
```
curl https://capstone-for-nd-udacity.onrender.com/the-food/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```
OR
```
curl http://localhost:5000/the-food/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```
Sample response output:
```
{
    "delete": 1,
    "success": true
}
```

## Testing
There are 16 unittests in test_app.py. To run this file use:
```
python -m unittest my_app.test_app
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.
Further, the file 'final-project-nd.postman_collection.json' contains postman tests containing tokens for specific roles.
To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> directory/final-project-nd.postman_collection.json
3. Click on the runner, select the collection and run all the tests.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'Barista ' and 'Manager ' roles.

## DEPLOYMENT
The app is hosted live on render  at the URL: 
https://capstone-for-nd-udacity.onrender.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.

Take a look at the GitHub repository if you like
[github repo](https://github.com/MoazAlsabouh/final-project-for-nd)