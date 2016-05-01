# mysetup.py
from distutils.core import setup
import py2exe

setup(console=["php_shell_scan.py","php_shell_scan_re.py"],
      data_files=[("",
                  [r"parsetab.py",
                   r"parser.out"]),
                 ])