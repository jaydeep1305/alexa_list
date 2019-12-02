import re
import requests
import redis
import json

try:
    from urllib.parse import quote_plus as url_encode
except ImportError:
    from urllib import quote_plus as url_encode

def decode_html(string):
    "decode common html/xml entities"
    new_string = string
    decoded = ['>', '<', '"', '&', '\'']
    encoded = ['&gt;', '&lt;', '&quot;', '&amp;', '&#039;']
    for e, d in zip(encoded, decoded):
        new_string = new_string.replace(e, d)
    for e, d in zip(encoded[::-1], decoded[::-1]):
        new_string = new_string.replace(e, d)
    return new_string

def parse2(string,query):
    parsed = []
    pattern = r'''<a[^>]* href="([^"]*)"'''
    links = re.finditer(pattern, string)
    for link in links:
        if query in link.group(1) :
            link = (link.group(1)).split("#",1)[0]
            parsed.append(link)
    return parsed

def parse(string,query):
    try:
        parsed = {}
        pattern = r'''<a[^>]* href="([^"]*)"'''
        matches = re.finditer(pattern, string)
        for match in matches:
            parsed = match.group(1)
            if "site:"+query not in parsed:
                if query in parsed:
                    # print(parsed)
                    pattern2 = r'''^/url\?q=(.*)/'''
                    matches2 = re.search(pattern2, parsed)
                    parsed = matches2.group(1)
                    # print(matches2.group(1))
                    break            
        return parsed
    except Exception as ex:
        print(ex)

def search(query):
    try:
        global cookie
        escaped = url_encode('https://google.com/search?q=%s' % url_encode("site:" + query))
        headers = {
        'Host': 'developers.facebook.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
        }
        response = requests.get('https://developers.facebook.com/tools/debug/echo/?q=%s' % escaped, headers=headers)
        cleaned_response = decode_html(response.text)
        
        substr = "</script>The document returned no data."
        if substr in cleaned_response :
            print("cookie expired")
            exit()

        # print(cleaned_response)
        parsed = parse(cleaned_response,query)
        return parsed
    except Exception as ex:
        print(ex)

def search_internal(parsed,query):
    try:
        global cookie
        escaped = url_encode(parsed)
        headers = {
        'Host': 'developers.facebook.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
        }
        response = requests.get('https://developers.facebook.com/tools/debug/echo/?q=%s' % escaped, headers=headers)
        cleaned_response = decode_html(response.text)
        
        substr = "</script>The document returned no data."
        if substr in cleaned_response :
            print("domain not working")

        # print(cleaned_response)
        parsed = parse2(cleaned_response,query)
        return parsed
    except Exception as ex:
        print(ex)

try:
    r = redis.Redis(host='68.183.246.217', port=6379)
    xs = r.get('xs')
    c_user = r.get('c_user')
    cookie = "c_user="+ c_user.decode("utf-8")  +"; xs="+ xs.decode("utf-8")  +";"
    

    filepath = 'list.txt'
    result = open('result.txt', 'w', buffering=1)

    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            query = line.strip()
            line = fp.readline()
            cnt += 1

            new_url = search(query)
            count   = search_internal(new_url,query)
            result.write(query+"\t"+new_url+"\t"+str(len(count))+"\n")
            print(query+"\t"+new_url+"\t"+str(len(count)))

except Exception as ex:
    print(ex)
    exit('Failed to connect, terminating.')
