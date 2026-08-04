from backend.algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


def check(case_name, result, expected):

    if result == expected:
        print(f"PASS: {case_name}")

    else:
        print(
            f"FAIL: {case_name} — expected {expected}, got {result}"
        )


# 1. Empty list

records = []

insertion_sort(records, "value")

check(
    "Insertion sort empty list",
    records,
    []
)


# 2. Single element

records = [
    {"value":5}
]

insertion_sort(records,"value")

check(
    "Insertion sort single element",
    records,
    [{"value":5}]
)


# 3. Binary search first index

records = [
    {"value":1},
    {"value":2},
    {"value":3}
]

check(
    "Binary search first index",
    binary_search(records,1,"value"),
    0
)


# 4. Binary search last index

check(
    "Binary search last index",
    binary_search(records,3,"value"),
    2
)


# 5. Binary search middle

check(
    "Binary search middle index",
    binary_search(records,2,"value"),
    1
)


# 6. Not found

check(
    "Binary search not found",
    binary_search(records,10,"value"),
    -1
)


# 7. insertion sort count

records = [
    {"value":3},
    {"value":1},
    {"value":2}
]


count = insertion_sort_count(records,"value")


check(
    "Insertion sort count type",
    type(count)==int and count>0,
    True
)


# 8. binary search count

result = binary_search_count(
    records,
    2,
    "value"
)


check(
    "Binary search count",
    result["index"],
    1
)


# 9. linear search absent

result = linear_search_count(
    records,
    100,
    "value"
)


check(
    "Linear search absent count",
    result["comparison_count"],
    len(records)
)