from django.shortcuts import render, get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from .templates import blog
from .models import Post,Comment
from django.utils import timezone
from .forms import PostFormNew,EmailPostForm,PostForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import Http404
from .forms import CommentForm
from django.views.decorators.csrf import csrf_exempt   
from markdown import markdown  

def post_share(request,post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,id=post_id)
    
    if request.method=='POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            #...send email
    else:
        form = EmailPostForm()
    return render(request,'blog/post_share.html',{'post':post,'form':form})   
 
def post_list(request):
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(object_list, 4) # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page':page,'posts':posts})

#@csrf_exempt    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Last page and next page
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(object_list,1) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    # Add Comment
    # List of active comments for this post
    comments = post.comments.filter(active=True)   
    if request.method == "POST":
        # A comment was posted
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            # Assign the current post to the comment
            new_comment.blog = post
            # Save the comment to the database
            new_comment.save()
    else:
        form = CommentForm()
    
    post_id = post.pk
    liked = False
    if request.session.get('has_liked_'+str(post_id), liked):
        liked = True
        print("liked {}_{}".format(liked, post_id))

    
    # clicks、comments and hearts count
    if request.user.is_authenticated:
        pass
    else:
        post.click_number += 1
    post.comment_number = len(post.comments.all())
    # post.heart_number = 
    post.save()
    
    ctx = {
        'post': post,
        'comments': post.comments.all().order_by('-created'),
        'form': form,
        'page':page,
        'posts':posts,
        'liked': liked
        }
        
    return render(request, 'blog/post_detail.html', ctx)
           
    
def post_new(request):
    if request.method == "POST":
        form = PostFormNew(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            text = cd['text']
            content_html = markdown(cd['text'])
            published_date = timezone.now()
            post = Post()
            post.title = title
            post.author = request.user
            post.text = text
            post.content_html = content_html
            post.published_date = published_date
            post.save()
            
            form = CommentForm()
            
            object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            paginator = Paginator(object_list, 1) # 1 posts in each page
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer deliver the first page
                posts = paginator.page(1)
            except EmptyPage:
            # If page is out of range deliver last page of results
                posts = paginator.page(paginator.num_pages)
                
            post_id = post.pk
            liked = False
            if request.session.get('has_liked_'+str(post_id), liked):
                liked = True
                #print("liked {}_{}".format(liked, post_id))
            ctx = {
                'post': post,
                'comments': post.comments.all().order_by('-created'),
                'form': form,
                'page':page,
                'posts':posts,
                'liked': liked
                }        
            return render(request, 'blog/post_detail.html', ctx)
            
            #return redirect('post_detail', pk=post.pk)
    else:
        form = PostFormNew()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            print('form is valid')
            print(form.cleaned_data)
            cd = form.cleaned_data
            title = cd['title']
            text = cd['text']
            #author = cd['author']
            content_html = markdown(cd['text'])
            published_date = timezone.now()
            ''' 这种方式会创建一篇新的文章
                而不是覆盖修改前的原文
            post = Post(
                title = title,
                author = request.user,
                text = text,
                content_html = content_html,
                published_date = published_date)
                下面的方式才会修改原文 '''
                
            post.title = title
            post.author = request.user
            post.text = text
            post.content_html = content_html
            post.published_date = published_date
            post.save()
            return redirect('post_detail', pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})    

def like_count_blog(request):
    liked = False
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.get(id=int(post_id))
        if request.session.get('has_liked_'+post_id, liked):
            print("unlike")
            if post.likes > 0:
                likes = post.likes - 1
                try:
                    del request.session['has_liked_'+post_id]
                except KeyError:
                    print("keyerror")
        else:
            print("like")
            request.session['has_liked_'+post_id] = True
            likes = post.likes + 1
    post.likes = likes
    post.save()
    return HttpResponse(likes, liked)
    
def delete_blog(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
    '''
    if request.method == 'GET':
        post_id = request.GET['post_id2']
        post = Post.objects.get(id=int(post_id))
        post.delete()
        return redirect('post_list')
    '''
    
