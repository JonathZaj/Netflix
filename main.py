import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, jinja2_view, error)
import utils
import json


# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    shows = []
    for show in utils.AVAILABE_SHOWS:
        json_show = utils.getJsonFromFile(show)
        dict_show = json.loads(json_show)
        shows.append(dict_show)
    sectionData = shows
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/search')
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})


@post('/search')
@jinja2_view('search_result.tpl', template_lookup=['templates'])
def search_result():
    shows = []
    results = []
    query = request.forms.get('q')
    for show in utils.AVAILABE_SHOWS:
        json_show = utils.getJsonFromFile(show)
        dict_show = json.loads(json_show)
        shows.append(dict_show)
    for show in shows:
        for episode in show["_embedded"]["episodes"]:
            s = {}
            if type(episode['summary']) == str and query in episode['summary'] or type(
                    episode['name']) == str and query in episode['name']:
                s["showid"] = show['id']
                s['episodeid'] = episode['id']
                s['text'] = show["name"] + " : " + episode["name"]
                results.append(s)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate="./templates/search_result.tpl",
                    sectionData={}, results=results, query=query)


@route('/show/<number>')
def show(number):
    sectionTemplate = "./templates/show.tpl"
    json_show = utils.getJsonFromFile(number)
    result = json.loads(json_show)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=result)


@route('/ajax/show/<number>')
def show(number):
    json_show = utils.getJsonFromFile(number)
    result = json.loads(json_show)
    return template("./templates/show.tpl", result=result)


@route('/show/<number>/episode/<episode_number>')
def show(number, episode_number):
    sectionTemplate = "./templates/episode.tpl"
    json_show = utils.getJsonFromFile(number)
    show = json.loads(json_show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=result_episode)


@route('/ajax/show/<number>/episode/<episode_number>')
def show(number, episode_number):
    json_show = utils.getJsonFromFile(number)
    show = json.loads(json_show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./templates/episode.tpl", result=result_episode)


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})

@error(500)
def error500(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 5000))
