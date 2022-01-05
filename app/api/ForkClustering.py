import requests
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from ..models import User, Project, Permission, login_manager
from ..analyse.compare_changes_crawler import fetch_commit_list
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import re


def get_active_forks(repo, access_token):
    active_forks = []
    result_length = 100
    page = 1

    while result_length == 100 and len(active_forks) < 10:
        request_url = "https://api.github.com/repos/%s/forks?per_page=100&page=%d" % (
            repo,
            page,
        )

        res = requests.get(
            url=request_url,
            headers={
                "Accept": "application/json",
                "Authorization": "token {}".format(access_token),
            },
        )

        forks = res.json()
        result_length = len(forks)

        for fork in forks:
            if fork["pushed_at"] > fork["created_at"]:
                active_forks.append(fork)

        page += 1

    return active_forks


def get_commit_list(repo, fork):
    commit_list = []

    # todo find correct url for different branches. Here we make the assumption we are comparing master branches
    url = "https://github.com/%s/compare/master...%s:master" % (
        repo,
        fork,
    )
    s = requests.Session()
    s.mount("https://github.com", HTTPAdapter(max_retries=3))

    try:
        diff_page = s.get(url, timeout=120)
        if diff_page.status_code != requests.codes.ok:
            raise Exception("error on fetch compare page on %s!" % repo)
    except:
        raise Exception("error on fetch compare page on %s!" % repo)

    diff_page_soup = BeautifulSoup(diff_page.content, "html.parser")
    for commit in diff_page_soup.find_all(
        "a", {"class": "Link--primary text-bold js-navigation-open markdown-title"}
    ):
        href = commit.get("href")
        if "https://" not in href:
            href = "https://github.com" + href
        title = commit.text

        commit_list.append({"title": title, "link": href})
    return commit_list


def get_code_diff(repo, fork):
    page_list = []
    function_list = []
    additions = []
    subtractions = []

    # todo find correct url for different branches. Here we make the assumption we are comparing master branches
    url = "https://github.com/%s/compare/master...%s:master.diff" % (
        repo,
        fork,
    )
    # url = requests.get(url, timeout=120).url + '.diff'
    # r = requests.get(url, timeout=120)
    s = requests.Session()
    s.mount("https://github.com", HTTPAdapter(max_retries=3))

    try:
        diff_page = s.get(url, timeout=120)
        if diff_page.status_code != requests.codes.ok:
            raise Exception("error on fetch compare page on %s!" % repo)
    except:
        raise Exception("error on fetch compare page on %s!" % repo)

    diff_page_soup = BeautifulSoup(diff_page.content, "html.parser")
    text = diff_page_soup.text
    diff_list = text.split("diff --git")

    for diff in diff_list[1:]:
        file_full_name = re.findall("a\/.*? b\/(.*?)\n", diff)[0]
        try:
            file_name, file_suffix = file_full_name.split(".")
        except:
            file_name = file_full_name
            file_suffix = None

    check = ""


def analyze_fork(repo, fork):
    fork_name = fork["full_name"][: -(len(fork["name"]) + 1)]
    commit_list = get_commit_list(repo, fork_name)
    code_diff = get_code_diff(repo, fork_name)
    return commit_list


def get_similar_forks(fork):
    pass


class ForkClustering(Resource):
    def __init__(self, jwt):
        self.jwt = jwt

    @jwt_required()
    def get(self):
        req_data = request.args
        repo = req_data.get("repo")

        current_user = get_jwt_identity()
        _user = User.objects(username=current_user).first()
        active_forks = get_active_forks(repo, _user.github_access_token)

        for fork in active_forks:
            analyze_fork(repo, fork)
        check = ""
