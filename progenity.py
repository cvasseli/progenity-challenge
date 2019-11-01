import subprocess
import os
from argparse import ArgumentParser

def cloneRepo(repo_url, username, password):
    user_pass_string = "//" + username + ":" + password + "@"
    clone_url = repo_url.replace("//", user_pass_string)
    clone_command = "git clone " + repo_url

    try:
        subprocess.call(clone_command, shell=True)
    except:
        print("Failed to clone repository, please ensure the account associated with your username and password have access to clone it.")
    return clone_url

def changeConfigFile(config_filename):
    replacement_message = "Roll Tide!"
    try:
        file = open(config_filename, "w+")
        file.write(replacement_message)
        file.close()
    except:
        print("Unable to make changes to the requested config file, please ensure the given name is correct and the file is in the root of the repository.")

def createPullRequest(url, branch_name, filename, username, password):
    checkout_command = "git checkout -b " + branch_name
    add_command = "git add " + filename
    commit_command = "git commit -m \"Time for a change\" "
    push_command = "git push " + url + " " + branch_name
    pr_command = "hub pull-request -m \"The times, they are a-changin.\" -b master -h " + branch_name
    unset_user = "unset GITHUB_USER"
    unset_pass = "unset GITHUB_PASSWORD"

    try:
        os.environ['GITHUB_USER'] = username
        os.environ['GITHUB_PASSWORD'] = password
    except:
        print("Unable to export credentials.")
    try:
        subprocess.call(checkout_command, shell=True)
    except:
        print("Failed to checkout branch.")
    try:
        subprocess.call(add_command, shell=True)
    except:
        print("Failed to add file to commit.")
    try:
        subprocess.call(commit_command, shell=True)
    except:
        print("Failed to commit changes.")
    try:
        subprocess.call(push_command, shell=True)
    except:
        print("Failed to push commit.")
    try:
        subprocess.call(pr_command, shell=True)
    except:
        print("Failed to create pull request.")
    try:
        os.environ['GITHUB_USER'] = ""
        os.environ['GITHUB_PASSWORD'] = ""
    except:
        print("Failed to destroy credentials.")

def main():
    parser = ArgumentParser()
    parser.add_argument('-u', '--user', action='store', dest='user', help='Github user name')
    parser.add_argument('-p', '--password', action='store', dest='password', help='Github password')
    parser.add_argument('-f', '--filename', action='store', dest='filename', help='Name of the file you want to change, default is config.txt', default="config.txt")
    parser.add_argument('-b', '--branch', action='store', dest='branch', help='Desired branch name for PR, default is test-pr', default="test-pr")

    arguments = parser.parse_args()
    username = arguments.user
    password = arguments.password
    filename = arguments.filename
    branch = arguments.branch

    repo_urls = ["https://github.com/cvasseli/progenity-challenge"]
    cwd = os.getcwd()

    for url in repo_urls:
        authenticated_url = cloneRepo(url, username, password)
        split_repo = url.split("/")
        repo_name = split_repo[-1]
        os.chdir(repo_name)
        changeConfigFile(filename)
        createPullRequest(authenticated_url, branch, filename, username, password)
        os.chdir(cwd)

    print("Done!")

if __name__ == '__main__':
    main()
