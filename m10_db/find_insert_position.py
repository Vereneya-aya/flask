def find_insert_position(A, x):
    left, right = 0, len(A)

    while left < right:
        mid = (left + right) // 2
        if A[mid] < x:
            left = mid + 1
        else:
            right = mid

    return left


A = [1, 2, 3, 3, 3, 5,8]
x = 4
assert find_insert_position(A, x) == 5

A = []
x = 10
assert find_insert_position(A, x) == 0

A = [2, 4, 6, 8]
x = 1
assert find_insert_position(A, x) == 0

A = [2, 4, 6, 8]
x = 10
assert find_insert_position(A, x) == 4

