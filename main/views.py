from django.shortcuts import render, redirect
from main.forms import UserForm
from main.models import movies
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'main/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'main/registeration.html',
                  {'user_form': user_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                data = request.POST.get('textbox1')

                context = {'data': data}
                return redirect('/success')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'main/login.html', {})


def successpage(request):
    return render(request, 'main/successpage.html', context={})


def mainpage5(request):
    data = request.POST.get('search')
    def recommender(request):
        import pandas as pd
        # import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set_style('white')
        # %matplotlib inline
        df_movies = pd.read_csv(r"C:\Users\Welcome\Desktop\Project\movielens data sets\movies.csv")
        df_ratings = pd.read_csv(r"C:\Users\Welcome\Desktop\Project\movielens data sets\ratings.csv")
        df = pd.merge(df_movies, df_ratings, on='movieId', how='outer')
        (df.groupby('title')['rating'].count().sort_values(ascending=False).head())
        ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
        moviemat = df.pivot_table(index='userId', columns='title', values='rating')
        ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
        ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
        # print(ratings.sort_values('num of ratings',ascending=False).head(10))
        movie_name = request.POST.get('search')
        user_ratings1 = moviemat[movie_name]
        user_ratings1.head()
        similar_to_starwars = moviemat.corrwith(user_ratings1)
        corr_ur = pd.DataFrame(similar_to_starwars, columns=['Correlation'])
        corr_ur.dropna(inplace=True)
        corr_ur.sort_values('Correlation', ascending=False).head(10)
        corr_ur = corr_ur.join(ratings['num of ratings'])
        variable= corr_ur[corr_ur['num of ratings'] > 100].sort_values('Correlation', ascending=False).head()
        variable.dropna(inplace=True)
        variable_dict = variable.to_dict('series')
        return variable_dict

    context= recommender(request)
    print(context)
    return render(request, 'main/mainpage.html', context)


def mainpage(request):

    data = request.POST.get('search')
    import pandas as pd
    # import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('white')
    # %matplotlib inline
    df_movies = pd.read_csv(r"C:\Users\Welcome\Desktop\Project\movielens data sets\movies.csv")
    df_ratings = pd.read_csv(r"C:\Users\Welcome\Desktop\Project\movielens data sets\ratings.csv")
    df = pd.merge(df_movies, df_ratings, on='movieId', how='outer')
    (df.groupby('title')['rating'].count().sort_values(ascending=False).head())
    ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
    moviemat = df.pivot_table(index='userId', columns='title', values='rating')
    ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
    ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
    # print(ratings.sort_values('num of ratings',ascending=False).head(10))
    movie_name = request.POST.get('search')
    user_ratings1 = moviemat[movie_name]
    user_ratings1.head()
    similar_to_starwars = moviemat.corrwith(user_ratings1)
    corr_ur = pd.DataFrame(similar_to_starwars, columns=['Correlation'])
    corr_ur.dropna(inplace=True)
    corr_ur.sort_values('Correlation', ascending=False).head(10)
    corr_ur = corr_ur.join(ratings['num of ratings'])
    variable = corr_ur[corr_ur['num of ratings'] > 100].sort_values('Correlation', ascending=False).head()
    results = pd.DataFrame(
        columns=['title',
                 'rating']
    )
    x = variable.to_dict(orient='dict')
    df = pd.DataFrame.from_dict(x, orient='columns')
    df.transpose()
    results = pd.concat([results, df], sort=False)
    a=[]
    a=results['title']
    b=[]
    b=results['rating']
   # variable.dropna(inplace=True)
    #variable_dict = variable.to_dict('series')
    #vv = variable_dict
    #=[]
    ##print(vv)
   # print('123',vv)
   #context = {
     #   'contexts':vv,

    return render(request, 'main/mainpage.html',{'a':a,'b':b})




