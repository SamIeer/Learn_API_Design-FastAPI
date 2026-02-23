#Testing Overview
'''
What is Testing 
it is a way for us to make sure our application working as intended
part of software development lifecycle that aims to identify:
-> Bugs -> Error -> Deffects
Meets user requirements and specifications
Ensuring software is high quality, reliabe, secure and user friendly

Manual Testing 
it is the testing have been doing so far
We have been manuallhy running our application and testing our api endpoints and other functionalities if they are 
working or not. That is manual testing

Unit Testing
Involves testing individual components or units of software is isolation from the rest of the application
Validatess that each unit of the software performs as designed 
unit = Testable part of the application
Developers wright unit tests during the development phase
Tests are automated and execures by a testing framework (Pytest)
Benefir is to identify bugs early in the development process

Integration Testing
Focisess on testing the interactions between different units ot components units togehter
Helps identify problems for the entire solution
Example: Call an API endpoint and make sure the correct solution is returned

Pytest:
Popular testing framework for python
known for simplicity, scalablility and ability to handle both unit and integration tests
TOp reasons to use Pytest:
Simple and Flexible - Native Assertions
Fixtures - Features setup and teardown
Parameterized testing - Run same tests with different data
'''
