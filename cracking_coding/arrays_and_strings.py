# Interview questions for strings and arrays, under data structures

class Questions:
    def q_1_1_is_unique(self, s):
        # Implement an algorithm to determine if a string has all unique characters.
        # What if you cannot use additional data structures?

        # Easy approach is just to use a set
        # return len(s) == len(set(s))

        # Could also use a bit vector, or equivalent.
        # But what about with no additional data structures?

        s = sorted(s)
        for i in range(1, len(s)):
            if s[i] == s[i-1]: return False
        return True

class TestQuestions:
    def test_q_1_1_is_unique(self):
        q = Questions()
        assert not q.q_1_1_is_unique('test')
        assert not q.q_1_1_is_unique('amazing')
        assert q.q_1_1_is_unique('thequickbrown')
        assert q.q_1_1_is_unique('')
        assert q.q_1_1_is_unique(' ') 
        assert not q.q_1_1_is_unique('mabcdefghijklm')
        assert q.q_1_1_is_unique('and this?')
