import os
import sublime
import sublime_plugin
import subprocess
import re

class CopyGitCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    file_name = self.view.file_name()
    dir_path = os.path.dirname(file_name)

    kwargs = {}
    kwargs["stdout"] = subprocess.PIPE
    kwargs["cwd"] = dir_path

    settings = sublime.load_settings("MoreGit.sublime-settings")
    remote_name = settings.get("remote_name")
    remote = subprocess.Popen(["git", "config", "--get", "remote." + remote_name + ".url"], **kwargs).stdout.read()

    if remote:
      (row,col) = self.view.rowcol(self.view.sel()[0].begin())
      remote_url = re.sub("^git@.*:", "https://github.com/", remote.decode("utf-8")[:-5])
      top_level = subprocess.Popen(["git", "rev-parse", "--show-toplevel"], **kwargs).stdout.read().decode("utf-8")[:-1]
      file = file_name.replace(top_level, "")
      link = remote_url + "/blob/develop" + file + "#L" + str(row + 1)
      sublime.set_clipboard(link)
    else:
      print("not have repo")

