from django.shortcuts import render, get_object_or_404
from .models import *
from utilities import PaginateObjects
from main.views import MyCustomMixin
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

# Create your views here.

class PostListView(MyCustomMixin, View):
    template_name = 'blog/post_list.html'
    def get(self, request, *args, **kwargs):
        if request.GET.get('category'):
            try:
                queryset=list(Post.objects.filter(category__label=request.GET.get('category')))
            except:
                queryset = list(Post.objects.all())
        else:
            queryset = list(Post.objects.all())
        posts_per_page = 6
        page_number = request.GET.get('page', 1)
        
        custom_range, posts, paginator = PaginateObjects(queryset, page_number, posts_per_page)
        
        context = {'custom_range':custom_range, 'posts':posts, 'paginator':paginator, 'footer_events':self.footer_events}
        
        return render(request, self.template_name, context)


class PostDetailView(MyCustomMixin, View):
    template_name = 'blog/post_detail.html'
    
    def get(self, request, url_aware_title, *args, **kwargs):
        self.context['latest_posts'] = Post.objects.all()[:3]
        self.context['categories'] = Category.objects.all()
        post = get_object_or_404(Post, url_aware_title=url_aware_title)
        post_base_comments = post.comments.exclude(parent_comment__isnull=False)[:6]
        self.context ['post'] = post
        self.context ['post_base_comments'] = post_base_comments
        
        post.comment_count  = len(post.comments.all())
        post.save()
        
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, url_aware_title=self.kwargs.get('url_aware_title'))
        # print(request.POST, 'THIS IS THE POST REQUEST')
        if request.POST.get('create_comment'):
            
            name = request.POST.get('commentor_name')
            message = request.POST.get('commentor_message')   
            
            if len(name)>3 and len(message)>2:
                if request.GET.get('reply_to'):
                    try:
                        parent_comment = Comment.objects.get(id=int(request.GET.get('reply_to')))
                        Comment.objects.create(parent_comment=parent_comment, commentor_name=name, post=post, content = str(message))
                    except:
                        pass
                else:
                    print('In the else block #$#$#$#$#$')
                    Comment.objects.create(commentor_name=name, post=post, content = str(message))
                post.comment_count = post.comments.count()
                post.save()
                messages.success(request, 'Your comment had been successfully posted.')
            else:messages.error(request, 'Please enter a valid name and comment')

        

        return self.get(request, self.kwargs.get('url_aware_title'))

# path('search_posts/', search_posts, name='post_ajax-search')
def search_posts(request):
    '''
    this function will perform live searches for posts on the site.
    it will probably be called by an ajax post request and return a JsonResponse
    '''
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.POST.get('search_query')
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(author__username__icontains=query) | 
            Q(content__icontains=query)
        )

        if results and query:
            output = [{'title':result.title, 'url_aware_title':result.url_aware_title, 'image':str(result.image.url), 'comment_count':result.comment_count, 'author_name':result.author.username } for result in results ]
        else:
            output = 'No Posts match your description...'
        
        return JsonResponse({'data': output})
    return JsonResponse({})