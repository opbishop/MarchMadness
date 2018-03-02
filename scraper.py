import requests

def get_url(url):
    user_agent = {
        'name': 'John Smith',
        'email': 'john.smith@js.com'
    }
    response = requests.get(url+'/robots.txt', headers={
        'User - Agent': 'python - requests / 4.8.2(Compatible;{};{})'.format(user_agent['name'], user_agent['email'])},
                            timeout=10)
    if response.status_code == 200:
        #Only scrape URL if allowed by robots.txt
        return requests.get(url)
    else:
        #TODO: raise not allowed by robots.txt exception
        print("Not allowed by robots.txt")

if __name__ == '__main__':
    url = 'http://webscraper.io'

    r = get_url(url)
    print(r.text)
