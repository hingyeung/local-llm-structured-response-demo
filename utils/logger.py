from termcolor import colored, cprint

def _log(role, msg, color):
    cprint(colored(f"{role}: ", color, attrs=["bold"]) + colored(msg, color))

def log_ai(msg):
    _log("AI", msg, "blue")

def log_user(msg):
    _log("USER", msg, "green")

def log_system(msg):
    _log("SYSTEM", msg, "grey")
    
def log_error(msg):
    _log("ERROR", msg, "red")

def log(msg):
    print(msg)