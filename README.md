Use Notes:
    - If you would like a fresh password book remove the user_data.db file
    - On first time run the setup_database.py file
    - main_service.py is the running microservice loop
    - emmulate_message.py was included as an example use case for integration. 

COMMUNICATION CONTRACT:
    - Communication will be done over sockets. IP addresses can be adjusted (in main_service.py) by final user.
    - Messages will be sent as dictionaries with {"message": "example_command", additional data}
    - An example of both interactions can be seen in emmulate_message.py

    REQUESTING DATA:    
        - This is an example of REQUESTING for the service to save a password:     message = {"message": "save_password", "password": "abc123"}
        - Another available REQUEST is the number of users: message = {"message": "number_of_users"}
        - Current Available Commands:
            + "save_password": must be accompanied by a "password" entry where the string for the generated password can go
            + "number_of_users": prints out all users in the database in the microservice consol. Sends message back with number.

    RECEIVING DATA:
        - This is an example of a message that the service would send for you to RECEIVE: return_data = {"message": "return_number_of_users", "number_of_users": len(users)}
        - Current Return Messages:
            + "return_number_of_users": accompanied by a "number_of_users" entry which returns a integer with how many users there are.
