def v_add(v1,v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def colorMapping(val):
    val = 1-val
    color_val = val * 255
    return (color_val, color_val, color_val)

def isNeighbor(grid,r,c):
    def isValid(r,c):
        return True if (r >= 0) and (c >= 0) and (r <= len(grid) - 1) and(c <= len(grid) - 1) else False
    def f(r,c):
        return True if isValid(r,c) and grid[r][c] == 1 else False

    list = [f(r-2,c-2),f(r-2,c-1),f(r-2,c),f(r-2,c+1),f(r-2,c+2),
            f(r-1,c-2),f(r-1,c-1),f(r-1,c),f(r-1,c+1),f(r-1,c+2),
            f(r,c-2),  f(r,c-1),  f(r,c),  f(r,c+1),  f(r,c+2),
            f(r+1,c-2),f(r+1,c-1),f(r+1,c),f(r+1,c+1),f(r+1,c+2),
            f(r+2,c-2),f(r+2,c-1),f(r+2,c),f(r+2,c+1),f(r+2,c+2)]

    return any(list)
