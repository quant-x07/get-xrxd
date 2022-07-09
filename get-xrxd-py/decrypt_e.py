from itertools import cycle

def hexToBin(hexStr):
    return bytearray.fromhex(hexStr)

def decrypt_e(data, cipherHex, access_token):
    cipher0 = hexToBin(cipherHex)
    access_token_bytes = access_token.encode()
    cipher = bytearray(a ^ b for a, b in zip(bytearray(cipher0), cycle(bytearray(access_token_bytes))))
    data = bytearray(a ^ b for a, b in zip(bytearray(data), cycle(bytearray(cipher))))
    return data
