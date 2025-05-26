from json import loads, JSONDecodeError
from typing import Union

def change(data, index, value):
    item = data
    for i in range(len(index) - 1):
        item = item[index[i]]
    item[index[-1]] = value

def is_json(text: str, return_decoded = False) -> Union[bool, dict]:
    if not isinstance(text, (str, bytes, bytearray)): return False
    
    text = text.strip()
    
    if not text: return False
    if text[0] not in {'{', '['} or text[-1] not in {'}', ']'}: return False
    
    try:
        decoded = loads(text)        
    except (ValueError, TypeError, JSONDecodeError):
        return False
    
    if return_decoded: return decoded
    else: return True