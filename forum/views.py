import re
from urllib import quote
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext

from forum.models import Category, Board, Topic, Post
from forum.forms import *


def forum_home(Request):
    """
    Displays the boards and the most recent post for each
    """
    Categories = Category.objects.order_by('position')

    return render_to_response('forum/index.html', {'category_list': Categories}, context_instance=RequestContext(Request))

def forum_board(Request, BoardID, BoardStr):
    """
    Displays the topics on a board
    """
    CurrBoard = get_object_or_404(Board, pk=BoardID)

    if BoardStr != re.sub(r'[^a-zA-Z0-9:-]', '', CurrBoard.title.replace(' ', '-')): 
        return HttpResponseRedirect('/forum/' + CurrBoard.get_URL())

    return render_to_response('forum/board.html', {'board': CurrBoard}, context_instance=RequestContext(Request))

def forum_topic(Request, TopicID, TopicStr, Page):
    """
    Displays the topic
    """
    CurrTopic = get_object_or_404(Topic, pk=TopicID)

    if TopicStr != re.sub(r'[^a-zA-Z0-9:-]', '', CurrTopic.title.replace(' ', '-')):
        return HttpResponseRedirect('/forum/' + CurrTopic.get_URL())

    return render_to_response('forum/topic.html', {'topic': CurrTopic}, context_instance=RequestContext(Request))

@login_required()
@permission_required("forum.add_topic", raise_exception=True)
def forum_new_topic(Request, BoardID):
    """
    Posts a new topic
    """

    CurrBoard = get_object_or_404(Board, pk=BoardID)

    if Request.method == 'POST':
        form = NewTopicForm(Request.POST)
        if form.is_valid():
            time = timezone.now()

            topic = Topic(board=CurrBoard, title=form.cleaned_data['subject'])
            topic.save()

            post = Post(topic=topic, author=Request.user.userprofile, body=form.cleaned_data['body'], date_posted=time, last_edit=time)
            post.save()

            return HttpResponseRedirect('/forum')
    else:
        form = NewTopicForm()

    return render_to_response('forum/new_topic.html', {'form': form}, context_instance=RequestContext(Request))

@login_required()
@permission_required("forum.add_post", raise_exception=True)
def forum_new_post(Request, TopicID):
    """
    Posts a reply to a topic
    """

    CurrTopic = get_object_or_404(Topic, pk=TopicID)

    if Request.method == 'POST':
        form = NewPostForm(Request.POST)
        if form.is_valid():
            time = timezone.now()

            post = Post(topic=CurrTopic, author=Request.user.userprofile, body=form.cleaned_data['body'], date_posted=time, last_edit=time)
            post.save()
            
            return HttpResponseRedirect('/forum')
    else:
        form = NewPostForm()

    return render_to_response('forum/new_topic.html', {'form': form}, context_instance=RequestContext(Request))

@login_required()
def forum_delete_topic(Request, TopicID):
    """
    Displays a confirmation form and then deletes a topic
    """
    
    CurrTopic = get_object_or_404(Topic, pk=TopicID)

    # Confirm the user can delete the topic
    if not ((Request.user == CurrTopic.get_author().user 
            and Request.user.has_perm("forum.delete_topic")) 
            or Request.user.has_perm("forum.delete_other_topic")):
        raise Http404

    if Request.method == 'POST':
        form = DeleteTopicForm(Request.POST)
        if form.is_valid():
            url = '/forum/' + CurrTopic.board.get_URL()
            CurrTopic.delete()

            return HttpResponseRedirect(url)
    else:
        form = DeleteTopicForm()

    return render_to_response('forum/delete_topic.html', {'form': form}, context_instance=RequestContext(Request))

@login_required()
def forum_delete_post(Request, PostID):
    """
    Displays a confirmation form and then deletes a post
    """

    CurrPost = get_object_or_404(Post, pk=PostID)

    # Confirm the user can delete the post
    if not ((Request.user == CurrPost.author.user and Request.user.has_perm("forum.delete_post")) or Request.user.has_perm("forum.delete_other_post")):
        raise Http404

    if Request.method == 'POST':
        form = DeletePostForm(Request.POST)
        if form.is_valid():
            url = "/forum/" + CurrPost.topic.get_URL()
            CurrPost.delete()

            return HttpResponseRedirect(url)
    else:
        form = DeletePostForm()

    return render_to_response('forum/delete_post.html', {'form': form}, context_instance=RequestContext(Request))

def forum_edit_post(Request, PostID):
    pass
