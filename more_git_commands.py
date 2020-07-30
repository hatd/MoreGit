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
      current_selection = self.view.sel()[0]
      (row_begin,_) = self.view.rowcol(current_selection.begin())
      (row_end,_) = self.view.rowcol(current_selection.end())
      remote_url = re.sub("^git@.*:", "https://github.com/", remote.decode("utf-8")[:-5])
      top_level = subprocess.Popen(["git", "rev-parse", "--show-toplevel"], **kwargs).stdout.read().decode("utf-8")[:-1]
      link = file_name.replace(top_level, remote_url + "/blob/develop")
      link = link + "#L" + str(row_begin + 1)
      if row_begin != row_end:
        link = link + "-" + str(row_end + 1)
      sublime.set_clipboard(link)
    else:
      print("Please setting remote repo!!! Preference > Package Settings > MoreGit > Settings")
