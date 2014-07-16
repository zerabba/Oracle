import sublime
import sublime_plugin
from . import oracle_lib
import subprocess
import os


class OracleGotoBodyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def _on_change(result):
            try:
                ln = int(result) - 1

                if ln >= 0:
                    row, col = self.view.rowcol(pkgbody.begin())
                    pos = self.view.text_point(row + ln, 0)
                    reg = sublime.Region(pos, pos)
                    self.view.sel().clear()
                    self.view.sel().add(reg)
                    self.view.show(reg)
            except:
                ln = None

        pkgbody = oracle_lib.find_body(self.view)
        if pkgbody:
            self.view.window().show_input_panel('Package body line number:', '', _on_change, _on_change, None)
        else:
            sublime.error_message('Error: Package body not found !')

class OracleFormat(sublime_plugin.TextCommand):
   def run(self, edit):
        #def _on_change(result):

            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            self.view.run_command("save")
            process = subprocess.Popen(([os.path.join(sublime.packages_path(), 'Oracle', 'format_sql.bat'), '"' + self.view.file_name() + '"'])) #stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo
            print('Source Formated: ' + self.view.file_name())