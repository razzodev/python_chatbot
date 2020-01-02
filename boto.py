"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
from my_bot_func import *


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    for k, v in all_functions.items():
        if k(user_message):
            v(user_message)
            return json.dumps({"animation": boto['animation'], "msg": boto['reply']})
    return json.dumps({"animation": "confused", "msg": '''Oh man, I have nothing to say. Type 'commands' to see what i can do'''})


@route("/test", method='POST')
def test():
    user_message = request.POST.get('msg')
    # user_message = 'test route'
    return json.dumps({"animation": 'inlove', "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000, reloader=True)


if __name__ == '__main__':
    main()
