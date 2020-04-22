# -*- coding: utf-8 -*-
with open ('replaced.txt', 'r') as f:
  old_data = f.read()

new_data = old_data.replace('строка 2dfasdf', 'строка два')

with open ('replaced.txt', 'w') as f:
  f.write(new_data)