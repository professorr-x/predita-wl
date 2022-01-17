from itertools import cycle

def GetProxy(proxy_pool):
    proxy = next(proxy_pool)
    if len(proxy.split(':')) == 4:
        splitted = proxy.split(':')
        return f"http://{splitted[2]}:{splitted[3]}@{splitted[0]}:{splitted[1]}"
    
    return proxy