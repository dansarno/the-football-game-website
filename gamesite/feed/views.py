from django.shortcuts import render

posts = [
    {
        'author': 'Daniel Sarno',
        'title': 'Status Update 1',
        'content': 'This is my first update',
        'date_posted': 'November 25, 2020'
    },
    {
        'author': 'Daniel Sarno',
        'title': 'Status Update 2',
        'content': 'Here is another update for everyone',
        'date_posted': 'November 26, 2020'
    },
    {
        'author': 'Rosario Sarno',
        'title': 'Status Update 3',
        'content': 'How about that result, fun game  huh?!',
        'date_posted': 'November 27, 2020'
    }
]


def home(request, template_name="feed/home.html"):
    return render(request, template_name, {
        'title': "Home",
        'posts': posts
    })
