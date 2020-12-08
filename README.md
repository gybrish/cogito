### Setup

This projectioon requires python 3.8 & uses pipenv to manage dependencies.

`python3.8 -m pip install pipenv`

### Running

This project uses FastAPI which uses uvicorn to run the web server.

To run the project the following from the root directory of the project:

`python3.8 -m pipenv run uvicorn file_api.api.main:app`

It will auto create the sqlite databse in the database folder and all files will be saved to the uploads folder.

### Testing

If this were to be production code all db operations & api end points would be covered in unit tests. This would require stubbing/mocking sqlalchemy reads/writes in order to emulate db operations. This would include known edge cases and failure scenarios (eg. db not accessable, time out issues, permissions issues etc.)

Integration tests would also be included to stand up the application and perform end to end tests as in:
 * Test all end points given an empty DB 
 * Fill it with given file set
 * Test access patterns with /{id} end points
 * Ensure /mrufiles is correctly listing accessed files
 