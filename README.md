## Box Platform Access Token Microservice 
- Authenticates a requests username / password Authorization header  
- Returns 200 success response with a Box Platform access token is username / password are valid  
- Returns 401 unauthorized response if the username / password aren't valid  
- Returns 500 server error response if an exception is raise  
- Includes unit, integration and functional test suite  
### Set up and Run  
1. From the project root folder, create a Python 3.6+ virtual environment  
`$ virtualenv --python=python3 env`  
2. Activate the virtual environment  
`$ source env/bin/activate`  
3. Install the project dependencies  
`$ pip install -r requirements.txt`  
4. Add Box Platform JWT keys to configuration file  
`/box_jwt_keys.yml`  
5. Run the API  
`$ python src/main.py runserver` 
6. Call the API  
`$ python src/main.py callserver` 
### Set up and Run with Docker  
1. Build and run the development Docker image
`$ make dev`  
### Run the test suite  
`$ pytest`