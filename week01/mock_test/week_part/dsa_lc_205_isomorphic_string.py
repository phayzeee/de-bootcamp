from collections import Counter

from mypy.typeops import false_only


def isIsomorphic( s: str, t: str) -> bool:
    s_t = {}
    t_s = {}

    for i in range(len(s)):
        c1 = s[i]
        c2 = t[i]

        if c1 in s_t:
            if s_t[c1] != c2:
                return False
        else:
            s_t[c1] = c2

        if c2 in t_s:
            if t_s[c2] != c1:
                return False
        else:
            t_s[c2] = c1

    return True




print(isIsomorphic("foo", "bar"))