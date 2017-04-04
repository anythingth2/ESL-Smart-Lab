import urllib
import urllib2
import json

url='file:///C:/Users/ChiChaChai/Documents/ESL%20Smart%20Lab/EslWeb/controller.html'
url_posttest='http://posttestserver.com/post.php'
data={'test':'test',
       'Name':'ChiChaChai',
       'Email':'chatchaishaetan@gmail.com' }
header={'Header':'ESL smart lab'}
json_post=json.dumps(data)


with open('historyTable','w+') as file:
    json.dump(json_post,file)

request = urllib2.Request(url,urllib.urlencode(data),header)
#request = urllib2.Request(url)
response=urllib2.urlopen(request)
#json_get=json.loads(response.read())

print response.read()