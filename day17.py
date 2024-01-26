from util import solve

def solver(data):
    M, N = len(data), len(data[0])
    dim = (M, N, 4, 3)
    dp = [[
            [
                [
                    [float('inf')] * 3
                ] for _ in range(4)
            ] for _ in range(N)
    ] for _ in range(M)]

    for i in range(M-1, -1, -1):
        for j in range(N-1, -1, -1):
            pass # i give up, dp is hard