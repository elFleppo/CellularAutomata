import os
#Decorators and utilities
def log_decorator(original_function):
    def wrapper(*args, **kwargs):

        # Call the original function
        result = original_function(*args, **kwargs)
        
        logfile_name = "logs/decorator-log.txt"
        if not os.path.isdir("logs"):
            os.mkdir("logs")
            
        with open("logs/decorator-log.txt", "a") as logfile:
            logfile.write(
                f"Calling {original_function.__name__} with args: {args}, kwargs: {kwargs} \n"
                f" {original_function.__name__} returned: {result}\n ")

        # Return the result
        return result
    return wrapper