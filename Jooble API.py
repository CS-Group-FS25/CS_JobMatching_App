#API von Jooble 
#API ist begrenzt auf 500 Versuche, kann aber neu Anfragen

api_key = "191d9abc-7de2-4e48-a82f-ad26afef2234"

import http.client

host = 'jooble.org'
key = api_key

connection = http.client.HTTPConnection(host)
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "it", "location": "Bern"}'

connection.request('POST','/api/' + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)
print(response.read())

#API funktioniert. Variablen nach denen gesucht werden sind:
#Keywords: keywords: Keywords to search for jobs by.
#location: Location to search for jobs in.
#radius (optional): Search radius, converted to kilometers (type: string).
#salary (optional): Minimum salary for the job search (type: integer).
#page (optional): The page number of the search results.
#ResultOnPage (optional): Number of jobs displayed on each page.
#SearchMode (optional): The search mode, default is 0.
#companysearch (optional):
    #true – To search for keywords in the company name of the job.
    #false – To search for keywords in the job title or description.
