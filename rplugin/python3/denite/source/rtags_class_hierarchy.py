import os
import sys
import subprocess
from denite.source.base import Base
import denite.util

sys.path.insert(1, os.path.dirname(__file__))

class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'rtags_class_hierarchy'
        self.kind = 'file'

    def gather_candidates(self, context):

        search_info = "{}:{}:{}".format(self.vim.current.window.buffer.name,
                                        self.vim.current.window.cursor[0],
                                        self.vim.current.window.cursor[1] + 1)
        ret = subprocess.run(["rc", "--class-hierarchy",
                                    search_info], stdout=subprocess.PIPE)
        if ret.returncode != 0:
            return []

        ret = ret.stdout.decode().split('\n')[1:-1]
        candidates = []
        for line in ret:
            file_desc = line.split(':')
            candidates.append({
                'word': line,
                'action__path': file_desc[0].split()[-1],
                'action__line': file_desc[1],
                'action__col': file_desc[2]
            })

        return candidates
