from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
# Create your views here.
# from django.utils.datastructures import MultiValueDictKeyError
from .models import Board, Topic, Post
from django.http import Http404

def home(request):
	boards = Board.objects.all()
	return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
	try:
		board = Board.objects.get(pk=pk)
	except Board.DoesNotExist:
		raise Http404
	return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)

	# try:
 #    	is_private = request.POST['is_private']
	# except MultiValueDictKeyError:
 #    	is_private = False

	if request.method =='POST':
		subject = request.POST['Subject']
		message = request.POST['message']
		# print subject
		# print message
		user = User.objects.first()
		topic = Topic.objects.create(
			subject=subject, 
			board=board, 
			starter=user)

		post = POST.objects.create(
			message=message, 
			topic=topic, 
			created_by=user)

		return redirect('board_topics', pk=board.pk)

	return render(request, 'new_topic.html', {'board': board})



