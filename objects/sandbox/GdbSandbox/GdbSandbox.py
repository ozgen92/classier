from classier.objects.sandbox.AbstractSandbox import AbstractSandbox
import pexpect

# TODO: python support, & handle necessary gdb build in a local&restricted way
# https://www.youtube.com/watch?v=xt9v5t4_zvE
# TODO: option to use lldb
# https://lldb.llvm.org/use/python.html
# TODO: jdb
# will require clean rebuild: https://opensource.apple.com/source/lldb/lldb-69/docs/code-signing.txt

class GdbSandbox(AbstractSandbox):
    def __init__(self, cmd):
        super().__init__(cmd)
        p = pexpect.spawn(cmd)
