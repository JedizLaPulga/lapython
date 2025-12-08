from .non_modifying import (
    for_each, 
    find, 
    find_if, 
    find_if_not, 
    count, 
    count_if, 
    all_of, 
    any_of, 
    none_of
)

from .modifying import (
    copy,
    copy_if,
    copy_n,
    fill,
    fill_n,
    generate,
    transform,
    replace,
    replace_if
)

from .sorting import (
    sort,
    stable_sort,
    is_sorted,
    lower_bound,
    upper_bound,
    binary_search
)

from .numeric import (
    iota,
    accumulate,
    inner_product,
    partial_sum,
    adjacent_difference
)

__all__ = [
    'for_each', 
    'find', 
    'find_if', 
    'find_if_not', 
    'count', 
    'count_if', 
    'all_of', 
    'any_of', 
    'none_of',
    'copy',
    'copy_if',
    'copy_n',
    'fill',
    'fill_n',
    'generate',
    'transform',
    'replace',
    'replace_if',
    'sort',
    'stable_sort',
    'is_sorted',
    'lower_bound',
    'upper_bound',
    'binary_search',
    'iota',
    'accumulate',
    'inner_product',
    'partial_sum',
    'adjacent_difference'
]
