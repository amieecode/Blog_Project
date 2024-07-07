from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView 
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by =3 
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404( Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day )
    return render( request, 'blog/post/detail.html', {'post': post} )

def post_share(request, post_id):
    #Retrieve post by id 
    post = get_object_or_404( Post, id=post_id, status=Post.Status.PUBLISHED )
    sent = False
    if request.method == 'POST':
        #Form was submitted from
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #form field passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri( post.get_absolute_url())
            subject = ( f"{cd['name']} ({cd['email']})" f"recommend you read {post.title}" )
            message = ( f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}" )
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']] )
            sent = True
    #...Send email 
    else:
        form = EmailPostForm()
    return render( request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent } )
