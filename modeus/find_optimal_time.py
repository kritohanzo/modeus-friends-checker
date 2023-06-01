from .modeus import get_rasps

buildings_nearby = {
    'УЛК-04' : ['УЛК-05', 'УЛК-11'],
    'УЛК-05' : ['УЛК-04', 'УЛК-11'],
    'УЛК-11' : ['УЛК-04', 'УЛК-05'],
}

def find_optimal(me, friends_fullnames):

    me = get_rasps(me).split('|')
    my_lessions = []
    for i in range(len(me)):
        if '—' in me[i]:
            my_lessions.append((me[i].strip(), me[i+1][me[i+1].find('(')+1:me[i+1].find(')')]))


    lessons = [(fullname + "|" + get_rasps(fullname)).split('|') for fullname in friends_fullnames]

    friends = dict()

    for people in lessons:
        for j in range(len(people)):
            if '—' in people[j]:
                if people[0] in friends.keys():
                    friends[people[0]] += [(people[j].strip(), people[j+1][people[j+1].find('(')+1:people[j+1].find(')')])]
                else:
                    friends[people[0]] = [(people[j].strip(), people[j+1][people[j+1].find('(')+1:people[j+1].find(')')])]

    result = []

    for my_lession in my_lessions:
        for friend in friends.keys():
            for friend_lession in friends[friend]:
                if friend_lession[0] == my_lession[0]:
                    if my_lession[0] in buildings_nearby[friend_lession[1]] or friend_lession[1] == my_lession[1]:
                        result.append(f'{friend.strip()} может встретиться с тобой после твоей пары в {my_lession[0].split("—")[0]}.\nОн тоже в это время будет на паре в корпусе {friend_lession[1]}')

    return "\n\n".join(result)
