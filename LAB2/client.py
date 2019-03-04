import requests
import json

API_URL = 'http://0.0.0.0:5000'

def makeGuess(num):
    endpoint = '{}/guess/{}' .format(API_URL, str(num))
    response = requests.get(endpoint)
    responseJSON = response.json()
    encodedJSON = json.loads(responseJSON)
    result = encodedJSON.get("result")
    return result

if __name__ == '__main__':
    
    # request random number
    endpoint = '{}/random'.format(API_URL)
    response = requests.get(endpoint)
    if response.ok:
        pass

    endpoint = '{}/getRange'.format(API_URL)
    response = requests.get(endpoint)
    responseJSON = response.json()

    start = int(responseJSON['start'])
    end = int(responseJSON['end'])

    found = False

    while end >= start and not found:
        mid = int((start + end)/2)
        res = makeGuess(mid)
        
        if 'equal' == res:
            found = True
            print('Random number in the server is {}'.format(mid))
        else:
            if 'less' == res:
                end = mid - 1 # looking the left side of the array
            else:
                start = mid + 1 # looking the right side of the array   
    
    if found == False:
        print('Random number in the server is not found')