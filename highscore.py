def high_score(result):
    with open('high_score', 'a') as e:
        e.write('{}\n'.format(result))


high_score(0)

hg_lst = []
with open('high_score', 'r') as file:
    c = file.read()
    for item in c.split('\n'):
        hg_lst.append(item)

new_list = []
for each in hg_lst:
    try:
        each = int(each)
        new_list.append(each)
    except (ValueError, Exception):
        pass

final_list = []
comp = [final_list.append(c) for c in new_list if c not in final_list]
work_list = []


counter = 0
while counter < 10:

    for item in reversed(final_list):
        counter += 1
        work_list.append(item)


high_scores = work_list[0:10]  # this should use in main.py
print(sorted(high_scores, reverse=True))



