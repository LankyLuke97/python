from functools import cache
from time import perf_counter
# 8.1 Triple Step: A child is running up a staircase with h steps and can hoop either 1 step, 2 steps, or 3 steps at a time. Implement a method to count how many possible ways the child can run up the stairs.


def ways_up_stairs(n: int) -> int:
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4

    dp3, dp2, dp1 = 1, 2, 4

    for _ in range(4, n + 1):
        dp3, dp2, dp1 = dp2, dp1, dp1 + dp2 + dp3

    return dp1


@cache
def recurse(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return recurse(n - 3) + recurse(n - 2) + recurse(n - 1)


start_recurse = perf_counter()
recurse_res = recurse(1_000)
end_recurse = perf_counter()
start_dp = perf_counter()
dp_res = ways_up_stairs(1_000)
end_dp = perf_counter()

assert recurse_res == dp_res
print(
    f"Recursion took {end_recurse - start_recurse}, while bottom-up dp took {end_dp - start_dp}"
)

n = 100_000

start_dp = perf_counter()
dp_res = ways_up_stairs(n)
end_dp = perf_counter()

print(f"Bottom up with n = {n} took {end_dp - start_dp}")
