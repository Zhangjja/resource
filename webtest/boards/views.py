from __future__ import unicode_literals
import json
from django.shortcuts import render

def home(request):
	List = ['zzz','jasf','/home/zzz/ftp',4]
	LIST = [6,7,8,9]

	return render(request,'home.html',{'List':json.dumps(List),
		'LIST':json.dumps(LIST)})