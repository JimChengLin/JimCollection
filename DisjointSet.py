class DisjointSetNode:
    def __init__(self, identifier, parent=None):
        self.identifier = identifier
        if not parent:
            self.parent = self

    def __repr__(self):
        return self.identifier


class SetPathCompressed(DisjointSetNode):
    def find(self):
        cursor = self
        prev_cursors = []
        while cursor.parent is not cursor:
            cursor = cursor.parent
            prev_cursors.append(cursor)

        for i in prev_cursors:
            i.parent = cursor
        return cursor

    def union(self, other):
        other.parent = self
        return self


class SetUnionRank(DisjointSetNode):
    def __init__(self, identifier, parent=None):
        super().__init__(identifier, parent)
        self.rank = 0

    def find(self):
        cursor = self
        while cursor.parent is not cursor:
            cursor = cursor.parent
        return cursor

    def union(self, other):
        if self.rank == other.rank:
            other.parent = self
            return self

        if self.rank < other.rank:
            small, big = self, other
        else:
            small, big = other, self

        small.parent = big
        return big


if __name__ == '__main__':
    sample_1 = ('c', 'h', 'e', 'b')
    sample_2 = ('f', 'd', 'g')

    sample_1 = [SetUnionRank(i) for i in sample_1]
    sample_2 = [SetUnionRank(i) for i in sample_2]

    for i in sample_1[1:]:
        sample_1[0].union(i)

    for i in sample_2[1:]:
        sample_2[0].union(i)

    for i in sample_1:
        if i.find() is not sample_1[0]:
            raise Exception

    for i in sample_2:
        if i.find() is not sample_2[0]:
            raise Exception

    sample_1[0].union(sample_2[0])
    for i in sample_1[1:] + sample_2:
        print(i.find())
        if i.find() is not sample_1[0]:
            raise Exception
