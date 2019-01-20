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


def remove_duplicates(lst):
    hg = []
    for k in lst:
        if k not in hg:
            hg.append(k)

    return hg


x = remove_duplicates(new_list)
fhg = sorted(x[0:10], reverse=True) # this must be used in main.py


