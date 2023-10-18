from functools import cache

MAX_DEPTH = 3

with open('data/aoc-2021-23.txt') as f:
    dat = [x.strip() for x in f.readlines()]

row1 = dat[2].split('#')[3:7]
row2 = dat[3].split('#')[1:5]

@cache
def valid_moves(state):
    moves = []
    for i, c in enumerate(state[0:11]):
        if c in 'ABCD':
            ridx = 11 + 4*(ord(c) - 65)
            samesies = [s == c.lower() for s in state[ridx:ridx+4] if s in 'abcdABCD']
            if not all(samesies):
                continue

            nrg = 0
            hidx = 2*(ord(c)-64)
            if hidx < i:
                if any([s in 'ABCD' for s in state[hidx:i]]):
                    continue
            else:
                if any([s in 'ABCD' for s in state[i+1:hidx+1]]):
                    continue

            dp = MAX_DEPTH - len(samesies)
            nrg += dp
            os = ridx + dp
            nm = state[0:i] + '-' + state[i+1:os] + c.lower() + state[os+1:]
            nrg *= 10**(ord(c)-65)
            moves += [(nrg, nm)]
    for r in range(4):
        ridx = 11 + 4*r
        for i, c in enumerate(state[ridx:ridx+4]):
            if c in 'ABCD':
                hidx = 2*(r+1)
                nrg = 1 + i

                left = [i for i, x in enumerate(state[0:hidx]) if x in 'ABCD']
                right = [i+hidx+1 for i, x in enumerate(state[hidx+1:11]) if x in 'ABCD']
                li = 0 if not left else max(left)+1
                ri = 11 if not right else min(right)

                ret_hidx = 2*(ord(c)-64)

                for l in range(li, hidx):
                    if l in [2,4,6,8]:
                        continue
                    nm = state[0:l] + c + state[l+1:ridx+i] + '_' + state[ridx+i+1:]
                    if l < ret_hidx:
                        ret_nrg = 1 + ret_hidx - l
                    else:
                        ret_nrg = 1 + l - ret_hidx
                    moves += [((10**(ord(c)-65))*(nrg + hidx-l + ret_nrg), nm)]

                for r in range(hidx+1, ri):
                    if r in [2,4,6,8]:
                        continue
                    nm = state[0:r] + c + state[r+1:ridx+i] + '_' + state[ridx+i+1:]
                    if r < ret_hidx:
                        ret_nrg = 1 + ret_hidx - r
                    else:
                        ret_nrg = 1 + r - ret_hidx
                    moves += [((10**(ord(c)-65))*(nrg + r-hidx + ret_nrg), nm)]

                break

    return moves

def solved(state):
    for r in range(4):
        ridx = 11 + 4*r
        if state[ridx] not in 'abcd':
            return False
    return True

def dfs4():
    curr_state = ''.join(['--x-x-x-x--',f'{row1[0]}DD{row2[0]}',f'{row1[1]}CB{row2[1]}',f'{row1[2]}BA{row2[2]}',f'{row1[3]}AC{row2[3]}'])

    to_do = valid_moves(curr_state)

    seen = 0
    min_r = 50000

    while len(to_do) > 0:

        seen += 1
        g = to_do.pop()

        nm = valid_moves(g[1])
        for n in nm:
            score = n[0] + g[0]
            if solved(n[1]):
                if score < min_r:
                    min_r = score
            elif score < min_r:
                to_do += [(score, n[1])]

    return min_r

print('Part 2:', dfs4())
