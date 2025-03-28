"""
## Problem1 (https://leetcode.com/problems/flood-fill/)
Flood Fill Problem (LeetCode 733)
---------------------------------

You are given an image represented by a 2D integer grid. You must perform a flood fill starting from pixel (sr, sc) and change the color of the pixel and all its 4-directionally connected neighbors with the same color.

Approaches:
1. DFS (recursive)
2. BFS (queue-based)

Time Complexity:  O(m * n)
Space Complexity: O(m * n)
"""

from typing import List
from collections import deque

class Solution:
    # ========== Approach 1: DFS ==========
    def floodFillDFS(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        """
        Perform flood fill using DFS from the starting cell (sr, sc).
        Recursively change all connected cells with the same color.
        """
        m, n = len(image), len(image[0])
        original_color = image[sr][sc]
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        if original_color == color:
            return image  # No need to proceed if the color is already the target

        def dfs(r, c):
            # Base cases: out of bounds or color mismatch
            if r < 0 or c < 0 or r >= m or c >= n or image[r][c] != original_color:
                return

            image[r][c] = color  # Fill the cell

            for dr, dc in directions:
                dfs(r + dr, c + dc)

        dfs(sr, sc)
        return image

    # ========== Approach 2: BFS ==========
    def floodFillBFS(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        """
        Perform flood fill using BFS starting from (sr, sc).
        Use a queue to process cells level by level.
        """
        m, n = len(image), len(image[0])
        original_color = image[sr][sc]
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        if original_color == color:
            return image  # Prevent infinite loop

        queue = deque()
        queue.append((sr, sc))
        image[sr][sc] = color  # Fill the starting pixel

        while queue:
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == original_color:
                    image[nr][nc] = color
                    queue.append((nr, nc))

        return image


