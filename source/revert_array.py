# from typing import List
#
#
# def revert_array(two_d_list) -> List[List[int]]:
#         """ reverting the list of numbers in a row into a list of numbers in a column """
#         max_length = max(len(row) for row in two_d_list)
#         spalten = []
#         for i in range(max_length):
#             column = []
#             for row in two_d_list:
#                  if i < len(row):
#                      column.append(row[i])
#             spalten.append(column)
#         return spalten
#         #  return [[row[i] for row in self.numbers_in_row if i < len(row)] for i in range(max_length)]
