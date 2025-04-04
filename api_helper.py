import requests
import json
from cookie import cookie

def post_api_call_with_cookie(url, params={}, headers={}, payload={}):
    try:
        print("url",url)
        headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        headers['accept-encoding'] = 'gzip, deflate, br, zstd'
        headers['accept-language'] = 'en-US,en;q=0.9'
        headers['cache-control'] ='max-age=0'
        headers['connection'] = 'keep-alive'
        headers['Cookie'] = cookie
        headers['host'] = 'aagchatbot-api-backend-1970155331536418.18.azure.databricksapps.com'
        response = requests.post(url, params=params, headers=headers, data=payload)
        if response.status_code != 200:
            return "Error! " + str(response.status_code) + " " + response.text
        return response.json()
    except Exception as e:
        print("e",e)
        return "Error! " + str(e)

def get_api_call_with_cookie(url, params={}, headers={}):
    headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    headers['accept-encoding'] = 'gzip, deflate, br, zstd'
    headers['accept-language'] = 'en-US,en;q=0.9'
    headers['cache-control'] ='max-age=0'
    headers['connection'] = 'keep-alive'
    headers['Cookie'] = cookie
    headers['host'] = 'aagchatbot-api-backend-1970155331536418.18.azure.databricksapps.com'
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return "Error! " + str(response.status_code) + " " + response.text
    return response.json()