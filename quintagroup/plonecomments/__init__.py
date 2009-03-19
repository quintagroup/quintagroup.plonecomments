from AccessControl import allow_module

# Feed our monkeys :-)
from quintagroup.plonecomments import patch

allow_module('quintagroup.plonecomments.utils')
