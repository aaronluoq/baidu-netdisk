#!/usr/bin/python
import urllib2,urllib,MultipartPostHandler,cookielib,json
class BaiduPan:
	access_token=""
	rootUrl="https://pcs.baidu.com/rest/2.0/"
	def httpget(self,url):
		urlo=urllib2.urlopen(url)
		return urlo.read()
	def httppost(self,url,data={}):
		print url
		urlo=urllib2.urlopen(url,data)
		return urlo.read()
	def geturl(self,apitype,data):
		return BaiduPan.rootUrl+apitype+"?access_token="+BaiduPan.access_token+"&"+urllib.urlencode(data)
	def file(self,data,action):
		url=self.geturl("file",data)
		if action=="get":
			return self.httpget(url)
		else:
			return self.httppost(url)
	def quota(self):
		url=self.geturl("quota",{"method":"info"})
		return self.httpget(url);
	def mkdir(self,path):
		return self.file({"method":"mkdir","path":path},"post")
	def list(self,path):
		return self.file({"method":"list","path":path},"get")
	def meta(self,path):
		return self.file({"method":"meta","path":path},"get")
	def meta_mti(self,paths):
		return self.file({"method":"meta","param":json.dumps({"list":[{"path":x} for x in paths]})},"post")
	def move(self,ffrom,to):
		return self.file({"from":ffrom,"to":to,"method":"move"},"post")
	def move_mti(self,param):
		return self.file({"param":json.dumps({"list":param}),"method":"move"},"post")
	def copy(self,ffrom,to):
		return self.file({"from":ffrom,"to":to,"method":"copy"},"post")
	def copy_mti(self,param):
		return self.file({"param":json.dumps({"list":param}),"method":"copy"},"post")
	def delete(self,path):
		return self.file({"method":"delete","path":path},"post")
	def delete_mti(self,paths):
		return self.file({"method":"delete","param":json.dumps({"list":[{"path":x} for x in paths]})},"post")
	def search(self,path,wd,re=0):
		return self.file({"method":"search","path":path,"wd":wd,"re":re},"get")
	def upload(self,pathlocal,pathr):
		url=self.geturl("file",{"path":pathr,"method":"upload"})
		cookies=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),MultipartPostHandler.MultipartPostHandler)
		params={"file":open(pathlocal,"rb")}
		return opener.open(url,params).read()
	def download(self,path,local):
		f=open(local,"w")
		f.write(self.file({"method":"download","path":path},"get"))
		f.close()
	def diff(self,cursor="null"):
    		return self.file({"method":"diff","cursor":cursor},"get")
