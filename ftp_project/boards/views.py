from __future__ import unicode_literals
from django.shortcuts import render, redirect ,render_to_response
from django.contrib.auth.models	import	User
from django.http import HttpResponse, StreamingHttpResponse
import os, sys
from .models import Path,User
from django.views.decorators.http import require_http_methods,require_GET
from django.contrib.auth.decorators import login_required


ftp_path = '/srv/ftp/'

def home(request):
	dirs = os.listdir(ftp_path)
	list = []
	for x in dirs:
		list.append(ftp_path + x)
	file_list = dict(zip(dirs,list))
	keys = ['path', 'file_list', 'others']
	values = [ftp_path,file_list, dirs]
	info = dict(zip(keys,values))
	return render(request, 'home.html', {'info': info})

#获取文件的大小,结果保留两位小数，单位为MB
def get_FileSize(filePath):
	filePath = unicode(filePath,'utf8')
	fsize = os.path.getsize(filePath)
	fsize = fsize/float(1024*1024)
	return round(fsize,2)



def list_dir(request):
	a = request.GET['a']
	if a.count('/') == 6:
		father_path = os.path.dirname(a)
		list = []
		dirs = os.listdir(a)
		for x in dirs:
			y = '/' + x  
			list.append(a + y)
		file_list = dict(zip(dirs,list))
		# size = os.path.getsize(a)
		# print(size)
		keys = ['father_path','path','file_list','others']
		values = [father_path,a, file_list,dirs]
		info = dict(zip(keys,values))
		return render(request, 'file_list.html', {'info': info})
		# if os.path.isdir(a):
		# 	list = []
		# 	dirs = os.listdir(a)
		# 	for x in dirs:
		# 		y = '/' + x  
		# 		list.append(a + y)
		# 	file_list = dict(zip(dirs,list))
		# 	keys = ['father_path','path','file_list','others']
		# 	values = [father_path,a, file_list,dirs]
		# 	info = dict(zip(keys,values))
		# 	print(father_path)
		# 	return render(request, 'upload.html', {'info': info})
	 
		# else:
		# 	print('this is a file')
		# 	filename = a
		# 	def readFile(filename,chunk_size=51200):  
		# 		with open(filename,'rb') as f:  
		# 			while True:  
		# 				c = f.read(chunk_size)  
		# 				if c:  
		# 					yield c  
		# 				else:
		# 					break
		# 		f.close()
		# 	the_file_name= os.path.dirname(a)
		# 	filename= a 
		# 	response=StreamingHttpResponse(readFile(filename))  
		# 	response['Content-Type']='application/octet-stream'  
		# 	response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)  
		# 	return response
	elif a.count('/') <= 5:		
		father_path = os.path.dirname(a)
		if father_path == '/srv':
			return redirect("http://127.0.0.1:8000/?a=/srv/ftp")
		else:
			if os.path.isdir(a):
				list = []
				dirs = os.listdir(a)
				for x in dirs:
					y = '/' + x  
					list.append(a + y)
				file_list = dict(zip(dirs,list))
				keys = ['father_path','path','file_list','others']
				values = [father_path,a, file_list,dirs]
				info = dict(zip(keys,values))
				return render(request, 'list_dir.html', {'info': info})
		 
			else:
				print('this is a file')
				filename = a
				def readFile(filename,chunk_size=51200):  
					with open(filename,'rb') as f:  
						while True:  
							c = f.read(chunk_size)  
							if c:  
								yield c  
							else:
								break
					f.close()
				the_file_name= os.path.dirname(a)
				filename= a 
				response=StreamingHttpResponse(readFile(filename))  
				response['Content-Type']='application/octet-stream'  
				response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)  
				return response
	elif a.count('/') > 7:
		return HttpResponse('page error')

@login_required
def create_dir(request):
	a = request.GET['a']
	created_basedir = a
	father_path = os.path.dirname(a)
	if	request.method	==	'POST':
		subject	= request.POST['subject']
		created_path = os.path.join(created_basedir, subject)
		if subject.isalnum():
			print('ok')
			os.system("mkdir %s " % created_path)
		else:
			print('no')
		list = []
		dirs = os.listdir(a)
		for x in dirs:
			y = '/' + x  
			list.append(a + y)
		file_list = dict(zip(dirs,list))
		keys = ['father_path','path','file_list','others']
		values = [father_path,a, file_list,dirs]
		info = dict(zip(keys,values))
		return render(request, 'list_dir.html', {'info': info})

		# return	redirect('list_dir.html',	{'list':list})		#	TODO:redirect	to	the	created	topic	page

	return render(request, 'create_dir.html')


def downloads(request):
	a = request.GET['a']
	filename = a
	if os.path.isdir(a):
		return HttpResponse('this is a dir!')
	else:
		def readFile(filename,chunk_size=5120000):  
			with open(filename,'rb') as f:  
				while True:  
					c = f.read(chunk_size)  
					if c:  
						yield c  
					else:
						break
			f.close()
		the_file_name= os.path.dirname(a)
		response=StreamingHttpResponse(readFile(filename))  
		response['Content-Type']='application/octet-stream'  
		response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)  
		return response



from django.http import HttpResponseRedirect
from boards.forms import UploadFileForm

 

@login_required
def upload_file(request):
	a = request.GET['a']
	father_path = os.path.dirname(a)
	if	request.method	==	'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			# handle_upload_file(request.FILES['file'])
			file = request.FILES['file']
			path = os.path.join(a,file.name)
			with open(path, 'wb+') as f:
				for chunk in file.chunks():
					f.write(chunk)
			list = []
			dirs = os.listdir(a)
			for x in dirs:
				y = '/' + x  
				list.append(a + y)
			file_list = dict(zip(dirs,list))
			keys = ['father_path','path','file_list','others']
			values = [father_path,a, file_list,dirs]
			info = dict(zip(keys,values))
			return render(request, 'file_list.html', {'info': info})

            #handle_upload_file(form.files['file'])
			# return HttpResponse('upload success!')

	else:
		form = UploadFileForm()
	return render(request, 'upload_file.html', {'form': form})
		# list = []
		# dirs = os.listdir(a)
		# for x in dirs:
		# 	y = '/' + x  
		# 	list.append(a + y)
		# file_list = dict(zip(dirs,list))
		# keys = ['father_path','path','file_list','others']
		# values = [father_path,a, file_list,dirs]
		# info = dict(zip(keys,values))
		# return render(request, 'list_dir.html', {'info': info})



