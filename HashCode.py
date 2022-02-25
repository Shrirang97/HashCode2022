# Inputs
c, p = map(int, input().split(' '))
hmapContri = {}
hmapSkills = {}
hmapProj = {}
hmapRoles = {}
availContri = set()
availProj = set()
for _ in range(c):
    contri, noOfSkills = input().split(' ')
    noOfSkills = int(noOfSkills)
    hmapContri[contri] = {}
    availContri.add(contri)
    for _ in range(noOfSkills):
        skill, level = input().split(' ')
        level = int(level)
        hmapContri[contri][skill] = level
        if skill in hmapSkills:
            hmapSkills[skill][contri] = level
        else:
            hmapSkills[skill] = {}
            hmapSkills[skill][contri] = level
for _ in range(p):
    inputs = input().split(' ')
    pName = inputs[0]
    availProj.add(pName)
    d, s, b, r = map(int, inputs[1:])
    hmap = {}
    for _ in range(r):
        skill, level = input().split(' ')
        level = int(level)
        hmap[skill] = level
    hmapProj[pName] = [d, s, b, r, hmap]

# print('Contributers:  ', hmapContri, end='\n\n')
# print('Projects:  ', hmapProj, end='\n\n')
# print('Skills:  ', hmapSkills, end='\n\n')

# Define intermediate states
hmapProjEnd = {}
timeline = 0
finalScore = 0
finalResult = []


# Define intermediate functions
def isAnyInProgressProjectCompleted(timeline):
    global finalScore, hmapProjEnd, finalResult, availContri, availProj
    if len(hmapProjEnd)==0 or timeline not in hmapProjEnd:
        return
    for proj in hmapProjEnd[timeline].keys():
        availContri = availContri.union(hmapProjEnd[timeline][proj])
        devs = list(hmapProjEnd[timeline][proj])
        finalResult.append([proj, devs])
        finalScore += hmapProj[proj][1]
        if proj in availProj:
            availProj.remove(proj)
        # print('-------Remove proj at timeline ', timeline, availContri, availProj)
        # print('ProjEnd:',hmapProjEnd, '\nskills:', hmapSkills, end='\n\n')


while len(availProj)>0 and timeline<=50:
    # print('timeline ', timeline, availContri, availProj, hmapProjEnd, 'skills:', hmapSkills, end='\n\n')
    isAnyInProgressProjectCompleted(timeline)
    for proj in availProj:
        skills = hmapProj[proj][4]
        assignedContributers = set()
        skillCountDevs = 0
        # print('-->>>', hmapProj[proj])
        for skill in skills.keys():
            minScoreRequired = skills[skill]
            contributers = hmapSkills[skill]
            flag = False
            # print('Skills:', skill, minScoreRequired)
            if len(availContri)==0:
                break
            for dev in contributers:
                # print('Dev:', proj, skill, minScoreRequired, dev, contributers[dev], availContri)
                if dev in availContri and contributers[dev] >= minScoreRequired:
                    # print('Selected Dev:', proj, skill, minScoreRequired, dev, contributers[dev])
                    if contributers[dev]==minScoreRequired:
                        contributers[dev] += 1
                    assignedContributers.add(dev)
                    flag = True
                    skillCountDevs += 1
                    break
            # print(flag, skillCountDevs)
            if not flag:
                break
        # print('-----',skillCountDevs, len(skills))
        if skillCountDevs < len(skills):
            continue
        availContri -= assignedContributers
        if timeline + hmapProj[proj][0] not in hmapProjEnd:
            hmapProjEnd[ (timeline+hmapProj[proj][0]) ] = {}
        hmapProjEnd[timeline+hmapProj[proj][0]][proj] = assignedContributers
    timeline += 1
# print('==>>', availContri, availProj, hmapProjEnd)
print(len(finalResult))
for i in range(len(finalResult)):
    print(finalResult[i][0])
    print(' '.join(finalResult[i][1]))
