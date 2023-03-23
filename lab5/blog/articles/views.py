from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def archive(request):
    return render(request, 'archive.html',{"posts": Article.objects.all()})

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                flag = 0
                for i in Article.objects.all():
                    if form["title"] == i.title:
                        flag = 1
                        break
                if flag == 0:
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('/article/', article_id=Article.id)
                else:
                    form['errors'] = u"Имя вашей статьи не уникальное"
                    return render(request, 'create_post.html', {'form': form})
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})

    else:
        raise Http404

