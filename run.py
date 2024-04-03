import sys
sys.path.append('/source')
from source.permutation_group import permutation_group



p = permutation_group(4)
p.get_all_standard_tableaus()
p.print()