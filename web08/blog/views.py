# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms




class UserForm(forms.Form):
	username = forms.CharField()
	headImg	= forms.FileField() 

def regist(req):
	if req.method == "POST":
      		uf = UserForm(req.POST, req.FILES)
		if uf.is_valid():
			print uf.cleaned_data['username']
			print req.FILES
			print uf.cleaned_data['headImg'].name
			print uf.cleaned_data['headImg'].size
			fp = file('/upload/'+uf.cleaned_data['headImg'].name, 'wb')
			s = uf.cleaned_data['headImg'].read()	
			fp.write(s)
			fp.close()		
			return HttpResponse('ok')


	
	else:
		uf = UserForm()

	return render_to_response('regist.html', {'uf':uf})
