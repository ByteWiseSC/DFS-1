"""
01 Matrix Problem (LeetCode 542)
---------------------------------
## Problem2 (https://leetcode.com/problems/01-matrix/)

You are given a binary matrix. Return a matrix where each cell containing 1 is replaced with the distance to the nearest 0. Distance is defined as the number of steps needed to move to a neighboring cell (4 directions only).

Approaches included:
1. Brute-force BFS from each 1 cell (O((m*n)^2))
2. Optimized Multi-source BFS from all 0s (O(m*n))
3. DFS from each 0 (not optimal, avoids TLE by pruning)
4. Dynamic Programming (2-pass approach, O(m*n))
"""

from collections import deque
from typing import List


class Solution:

    # ========== 1. Brute-force BFS from Each 1 ==========
    def updateMatrix_BruteBFS(self, mat: List[List[int]]) -> List[List[int]]:
        """
        BFS from each 1 to find nearest 0 (inefficient).
        Time: O((m * n)^2), Space: O(m * n)
        """
        m, n = len(mat), len(mat[0])
        result = [[0] * n for _ in range(m)]
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        def bfs(r, c):
            queue = deque([(r, c)])
            visited = [[False] * n for _ in range(m)]
            visited[r][c] = True
            distance = 0

            while queue:
                level_size = len(queue)
                for _ in range(level_size):
                    row, col = queue.popleft()
                    if mat[row][col] == 0:
                        return distance
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                distance += 1
            return 0

        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    result[i][j] = bfs(i, j)

        return result

    # ========== 2. Optimized Multi-Source BFS ==========
    def updateMatrix_MultiSourceBFS(self, mat: List[List[int]]) -> List[List[int]]:
        """
        BFS from all 0s at once to compute minimum distance for 1s.
        Time: O(m * n), Space: O(m * n)
        """
        m, n = len(mat), len(mat[0])
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        queue = deque()

        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    queue.append((i, j))
                else:
                    mat[i][j] = -1  # Mark unvisited

        dist = 0
        while queue:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and mat[nr][nc] == -1:
                        mat[nr][nc] = mat[r][c] + 1
                        queue.append((nr, nc))
        return mat

    # ========== 3. DFS from Each 0 (With Pruning) ==========
    def updateMatrix_DFS(self, mat: List[List[int]]) -> List[List[int]]:
        """
        DFS from each 0 and update distance for surrounding 1s.
        Prune paths that already have shorter distances.
        Time: O((m * n)^2) worst-case, Space: O(m * n)
        """
        m, n = len(mat), len(mat[0])
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    mat[i][j] = -1  # Mark unvisited

        def dfs(r, c, dist):
            if r < 0 or r >= m or c < 0 or c >= n:
                return
            if mat[r][c] != -1 and mat[r][c] < dist:
                return
            mat[r][c] = dist
            for dr, dc in directions:
                dfs(r + dr, c + dc, dist + 1)

        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    dfs(i, j, 0)

        return mat

    # ========== 4. Dynamic Programming (2-pass) ==========
    def updateMatrix_DP(self, mat: List[List[int]]) -> List[List[int]]:
        """
        DP approach: 2 passes to compute min distance using neighbors.
        Pass 1: top-left to bottom-right
        Pass 2: bottom-right to top-left

        Time: O(m * n), Space: O(m * n)
        """
        m, n = len(mat), len(mat[0])
        MAX = float("inf")
        dp = [[MAX] * n for _ in range(m)]

        # First pass (top-left to bottom-right)
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    dp[i][j] = 0
                else:
                    if i > 0:
                        dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)
                    if j > 0:
                        dp[i][j] = min(dp[i][j], dp[i][j - 1] + 1)

        # Second pass (bottom-right to top-left)
        for i in reversed(range(m)):
            for j in reversed(range(n)):
                if i < m - 1:
                    dp[i][j] = min(dp[i][j], dp[i + 1][j] + 1)
                if j < n - 1:
                    dp[i][j] = min(dp[i][j], dp[i][j + 1] + 1)

        return dp
