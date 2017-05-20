import urllib2
import json
 
 
hjson = json.loads("{\"city_Name\":\"123\",\"city_Url\":\"http://krl.meituan.com\"}")
 
print hjson['city_Url']
