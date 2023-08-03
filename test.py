cell_name = [
            "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
            "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
            "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
            "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
            "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
            "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
            "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
            "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
        ]

column = list("87654321")
row = list("abcdefgh")

for a, b in enumerate(cell_name):
    if b == "a1":

        for row_index, i in enumerate(row):
            if i == b[0]:
                print(row[row_index-1], row[row_index+1])
        for column_index, j in enumerate(column):
            if j == b[1]:
                if column_index-1 != -1:
                    index_1 = column_index-1
                    print("1", column[index_1])
                if column_index+1 != 8:
                    index_2 = column_index+1
                    print("2", column[index_2])
