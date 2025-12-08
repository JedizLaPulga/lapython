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

from .set_operations import (
    merge,
    includes,
    set_union,
    set_intersection,
    set_difference,
    set_symmetric_difference
)

from .min_max import (
    min_element,
    max_element,
    minmax_element,
    clamp
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
    'adjacent_difference',
    'merge',
    'includes',
    'set_union',
    'set_intersection',
    'set_difference',
    'set_symmetric_difference',
    'min_element',
    'max_element',
    'minmax_element',
    'clamp'
]
