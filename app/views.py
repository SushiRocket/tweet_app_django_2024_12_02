from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from.models import Tweet,Like,User,Follow
from.forms import TweetForm,SignUpForm,ProfileUpdateForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden,JsonResponse


# Create your views here.

class IndexView(ListView):
    model=Tweet
    template_name='app/index.html'
    context_object_name='tweets'
    ordering=['-created_at']
    paginate_by=5

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('app:tweet_detail', pk=tweet.pk)
    else:
        form = TweetForm()
    return render(request, 'app/tweet_create.html', {'form':form})


class SignUpView(View):
    form_class=SignUpForm
    template_name='app/signup.html'

    #Viewを継承しているので自分で定義が必要。CreateViewやListViewはDjangoのgenericを使用しているので定義の必要がない。
    #self はクラス内のメソッドで、自身のインスタンス。
    #request は、Djangoが生成するHTTPリクエストオブジェクト。
    #ユーザーが送信した情報（GET/POSTデータ、ヘッダー、Cookieなど）が格納されています。
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        form=self.form_class(request.POST)#ユーザの入力を渡す
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, 'アカウントが作成され、ログインが成功しました！')#djangoのmessageフレームワーク
            return redirect('app:index')
        else:
            return render(request, self.template_name, {'form':form})

def tweet_detail(request, pk):
    tweet = get_object_or_404(Tweet,pk=pk) #Djangoの関数。特定のモデルオブジェクトを取得

    is_liked = False #初期値をFolseで設定
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, tweet=tweet).exists() #Likeモデルに紐づく投稿があればis_like=Trueに

        context = {#contextでテンプレートにviewを辞書でわたす
            'tweet': tweet,
            'is_liked': is_liked,
            'like_count': tweet.likes.count(),
        }
        return render(request, 'app/tweet_detail.html', context)

@login_required
def tweet_edit(request,pk):
    tweet = get_object_or_404(Tweet,pk=pk)
    if tweet.author != request.user:
        return HttpResponseForbidden('あなたはこのツイートを編集する権限がありません。') #データは存在するがアクセス権限がないとき。メッセージ返せる。
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('app:tweet_detail', pk=tweet.pk)
    else:
        form = TweetForm(instance=tweet)
        return render(request, 'app/tweet_edit.html', {'form': form, 'tweet': tweet})

@login_required
def tweet_delete(request,pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.author != request.user:
        return HttpResponseForbidden('あなたはこのツイートを削除する権限がありません。')
    if request.method == 'POST':
        tweet.delete()
        return redirect('app:index')
    return render(request, 'app/tweet_delete.html', {'tweet': tweet})

@require_POST
@login_required
def like_toggle(request,pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)

        if not created:
            like.delete()
            liked=False
        else:
            liked=True
        like_count=tweet.likes.count()
        return JsonResponse({'liked': liked, 'like_count': like_count})

def user_profile(request, username): #URLからusernameを取得。path('user/<str:username>/', views.user_profile, name='user_profile')
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(author=user).order_by('-created_at')

    context = { #テンプレートに辞書で返す
        'profile_user': user,
        'tweets': tweets,
    }

    return render(request, 'app/user_profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile )#HTTP リクエストの内容を保持する属性
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールが正常に更新されました！')
            return redirect ('app:user_profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': form
    }

    return render(request, 'app/edit_profile.html', context)

@login_required
@require_POST
def follow_toggle(request,username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return JsonResponse({'error': '自分自身をふぉろーすることはできません'}, status=400)
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)

    if not created:
        follow.delete()
        following=False

    else:
        following=True
    
    follower_count = target_user.follower.count()
    following_count = target_user.following.count()

    return JsonResponse({
        'following': following,
        'follower_count': follower_count,
        'following_count': following_count,
    })