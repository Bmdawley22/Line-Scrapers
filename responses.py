import random

def get_response(msg: str) -> str:
    p_msg = msg.lower()

    if p_msg == 'hello':
        return 'Hey there!'
    
    if p_msg == 'roll':
        return str(random.randint(1,6))
    
    if p_msg == '!help':
        return "can't help"
    
    return "I didn't understand what you wrote. Try typing 'help'"