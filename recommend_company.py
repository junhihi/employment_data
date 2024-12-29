import json
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import rc


# JSON 파일 읽기
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

#학점
def gradeclass(grades):
    gradecnt = [0, 0, 0, 0, 0, 0]
    gradelabs = []
    for grade in grades:
        if grade > 4: gradecnt[0] += 1
        elif grade > 3.5: gradecnt[1] += 1
        elif grade > 3: gradecnt[2] += 1
        elif grade > 2.5: gradecnt[3] += 1
        elif grade > 2: gradecnt[4] += 1
        else: gradecnt[5] += 1

    for i, value in enumerate(gradecnt):
        if value != 0:
            if i == 0: gradelabs.append('A+')
            elif i == 1: gradelabs.append('A')
            elif i == 2: gradelabs.append('B+')
            elif i == 3: gradelabs.append('B')
            elif i == 4: gradelabs.append('C+')
            elif i == 5: gradelabs.append('C')

    for i in range(len(gradecnt) - 1, -1, -1):
        if gradecnt[i] == 0: gradecnt.pop(i)

    return gradelabs, gradecnt

#토익
def toeicclass(toeics):
    toeiccnt = [0, 0, 0, 0, 0, 0]
    toeiclabs = []
    for toeic in toeics:
        if toeic > 900: toeiccnt[0] += 1
        elif toeic > 800: toeiccnt[1] += 1
        elif toeic > 700: toeiccnt[2] += 1
        elif toeic > 600: toeiccnt[3] += 1
        elif toeic > 500: toeiccnt[4] += 1
        else: toeiccnt[5] += 1

    for i, value in enumerate(toeiccnt):
        if value != 0:
            if i == 0: toeiclabs.append('900 ~')
            elif i == 1: toeiclabs.append('800 ~ 900')
            elif i == 2: toeiclabs.append('700 ~ 800')
            elif i == 3: toeiclabs.append('600 ~ 700')
            elif i == 4: toeiclabs.append('500 ~ 600')
            elif i == 5: toeiclabs.append('~ 500')
    
    for i in range(len(toeiccnt) - 1, -1, -1):
        if toeiccnt[i] == 0: toeiccnt.pop(i)

    return toeiclabs, toeiccnt

#자격증, 인턴, 공모전, 연수
def target(targets, k = 5, switch = False):
    all = []
    targetcnts = []
    targetlabs = []
    for target in targets:
        i = 0
        n = 0
        while 1:
            try:
                index = target.index(', ', i)
                all.append(target[i:index])
                i = index + len(', ')
                n += 1
            except ValueError:
                if target != '':
                    all.append(target[i:])
                    n += 1
                break

        targetcnts.append(n)

    # 각 항목의 등장 횟수를 세기
    counter = Counter(all)

    # 자격증 총 개수
    leng = 0

    titles = []
    ratios = []
    for title, cnt in counter.items():
        leng += cnt

    # 가장 많이 언급된 항목 k개 선택
    many = counter.most_common(k)

    for licen, cnt in many:
        ratio = cnt/leng*100
        ratios.append(ratio)
        titles.append(licen)
    
    gita = 100-sum(ratios)
    if gita == 100:
        ratios.append(gita)
        titles.append('없음')
        if switch == True:
            if gita > 0:
                ratios.append(gita)
                titles.append('기타')

    targetcounter = Counter(targetcnts)

    numcnt = []
    for item in targetcounter.items():
        numcnt.append(item)

    nums = sorted(numcnt, key = lambda x: x[0])
    
    targetlabs = [str(num[0]) for num in nums]
    targetcnt = [round(num[1], 2) for num in nums]

    return [titles, ratios, targetlabs, targetcnt, leng]


def delcomma(targets):
    all = []
    for target in targets:
        i = 0
        n = 0
        while 1:
            try:
                index = target.index(', ', i)
                all.append(target[i:index])
                i = index + len(', ')
                n += 1
            except ValueError:
                all.append(target[i:])
                n += 1
                break
        for i in range(len(all)):
            if all[i] == '': all.pop(i)

    return all

def part1(data):
    large = [entry["대분류"] for entry in data if entry["대분류"] != '']
    middle = [entry["중분류"] for entry in data if entry["중분류"] != '']
    lm = [entry["대중분류"] for entry in data if entry["대중분류"] != '']
    small = [entry["소분류"] for entry in data if entry["소분류"] != '']
    
    #인덱스 번호
    n = []
    #해당 지원분야 리스트
    li = []
    
    larges = delcomma(large)
    print(larges)

    #지원 분야중복 선택 가능
    lar = input("대분류를 입력하세요: ")

    if lar == '전체':
        jiwon = delcomma([small[0]])
        jiwon.pop(0)

    else:
        l = delcomma([lar])
        print(l)

        for i in l:
            n.append(large.index(i))

        for i in n:
            li += delcomma([middle[i]])
        print(li)

        mid = input("중분류를 입력하세요: ")

        midall = delcomma([mid])

        if mid == '전체':
            midall = delcomma(li)
    

        print(midall)

        n = []
        li = []
        jiwon = ['전체']
        for i in midall:
            n.append(lm.index(i))

        for i in n:
            li = delcomma([small[i]])
            li.pop(0)
            jiwon += li

    print(jiwon)

    jiwons = input("소분류를 입력하세요: ")

    jiwons = delcomma([jiwons])

    if jiwons == ['전체']:
        jiwon.pop(0)
        jiwons = []
    else:
        jiwon = jiwons
        jiwons = []

    for j in jiwon:
        for entry in data: 
            if entry.get("지원분야") == j:
                jiwons.append(entry)

    if jiwons:
        upjongs = [entry["업종별"] for entry in jiwons]
        upjongs = delcomma(upjongs)
        upjong = set(upjongs)
        print(upjong)

        upjong = [input("업종을 입력하세요: ")]
        upjong = delcomma(upjong)
        upjong = set(upjong)
        print(upjong)

        upjongs = []
        if '전체' in upjong:
            upjongs = [entry for entry in jiwons]

        else: 
            for j in upjong:
                for entry in jiwons: 
                    if entry.get("업종별") == j:
                        upjongs.append(entry)


        return upjongs

def part2(data):
    jiwons = [entry["지원분야"] for entry in data]
    jiwons = delcomma(jiwons)
    jiwon = set(jiwons)
    print(jiwon)

    #지원 분야중복 선택 가능
    jiwon = [input("지원분야를 입력하세요: ")]
    jiwon = delcomma(jiwon)
    jiwon = set(jiwon)
    print(jiwon)
    jiwons = []
        
    if '전체' in jiwon:
        jiwons = [entry for entry in data]
    else:
        for j in jiwon:
            for entry in data: 
                if entry.get("지원분야") == j:
                    jiwons.append(entry)

        return jiwons

#학점
def gear(data, giup, graph = False):
    giupdata = [entry for entry in data if entry.get("기업") == giup]
    grades = [float(entry["학점"]) for entry in giupdata if entry["학점"] != '']
    toeics = [int(float(entry['토익'])) for entry in giupdata if entry['토익'] != '']
    licens = [entry['자격증'] for entry in giupdata if entry['자격증'] != '']
    interns = [entry['인턴'] for entry in giupdata if entry['인턴'] != '']
    gongmos = [entry['공모전'] for entry in giupdata if entry['공모전'] != '']
    trips = [entry['연수'] for entry in giupdata if entry['연수'] != '']
    # jaso = [entry["자소서 질문"] for entry in jiwon]

    #성적
    gradelabs, gradecnt = gradeclass(grades)

    #토익
    toeiclabs, toeiccnt = toeicclass(toeics)
    if grades:
        # 평균 학점 계산
        avggrade = sum(grades) / len(grades)
        avggrade = round(avggrade, 2)
        # 평균 토익 계산
        if len(toeics) != 0:
            avgtoeic = sum(toeics) / len(toeics)
            avgtoeic = round(avgtoeic)
        else: avgtoeic = 0
        
        if graph == True:
            #자격증
            a = target(licens, switch =True)
            titles, ratios, licenlabs, licencnt, lileng = a[0], a[1], a[2], a[3], a[4]
            licenlabs = [lab + '개' for lab in licenlabs]
            license = len(grades) - len(licens)
            if license != 0: 
                licenlabs.insert(0, '0개')
                licencnt.insert(0, license)

            #인턴
            a = target(interns, switch =True)
            intit, inrat, inlabs, incnt, inleng = a[0], a[1], a[2], a[3], a[4]
            inlabs = [lab + '번' for lab in inlabs]
            intern = len(grades) - len(interns)
            if intern != 0:
                inlabs.insert(0, '0번')
                incnt.insert(0, intern)

            #공모전
            a = target(gongmos, switch =True)
            gotit, gorat, golabs, gocnt, goleng = a[0], a[1], a[2], a[3], a[4]
            golabs = [lab + '번' for lab in golabs]
            gongmo = len(grades) - len(gongmos)
            if gongmo != 0:
                golabs.insert(0, '0번')
                gocnt.insert(0, gongmo)

            #연수
            a = target(trips, switch =True)
            trtit, trrat, trlabs, trcnt, trleng = a[0], a[1], a[2], a[3], a[4]
            trlabs = [lab + '번' for lab in trlabs]
            trip = len(grades) - len(trips)
            if trip != 0:
                trlabs.insert(0, '0번')
                trcnt.insert(0, trip)
            

            
            print(f"{giup}의 합격자들의 평균 학점: {avggrade:.2f}점")
        
            print(f"{giup}의 합격자들의 평균 토익 점수: {avgtoeic:.0f}점")
        
            print(f"토익을 본 합격자의 비율 : {len(toeics)/len(grades)*100:.1f}%")

            print(f"자격증이 있는 합격자의 비율 : {len(licens)/ len(grades)*100:.1f}%")
            
            print(f"인턴 경험이 있는 합격자의 비율 : {len(interns)/ len(grades)*100:.1f}%")

            print(f"공모전에 나간 경험이 있는 합격자의 비율 : {len(gongmos)/ len(grades)*100:.1f}%")

            print(f"연수 간 경험이 있는 합격자의 비율 : {len(trips)/ len(grades)*100:.1f}%")
            
            print()

            for i in range(len(gradelabs)):
                print(f"{gradelabs[i]} : {gradecnt[i]}명")

            for i in range(len(toeiclabs)):
                print(f"{toeiclabs[i]} : {toeiccnt[i]}명")
            
            print("상위 자격증 8개:")
            for i in range(len(titles)):
                print(f"{titles[i]} : {ratios[i]:.2f}%")

            for i in range(len(licenlabs)):
                print(f"{licenlabs[i]}의 자격증을 가진 합격자 : {licencnt[i]}명")
            
            print()

            for i in range(len(intit)):
                print(f"{intit[i]} : {inrat[i]:.2f}%")

            for i in range(len(inlabs)):
                print(f"{inlabs[i]} 인턴 경험이 있는 합격자 : {incnt[i]}명")

            print()

            for i in range(len(gotit)):
                print(f"{gotit[i]} : {gorat[i]:.2f}%")

            for i in range(len(golabs)):
                print(f"{golabs[i]} 공모전 경험이 있는 합격자 : {gocnt[i]}명")

            print()

            for i in range(len(trtit)):
                print(f"{trtit[i]} : {trrat[i]:.2f}%")

            for i in range(len(trlabs)):
                print(f"{trlabs[i]} 연수 경험이 있는 합격자 : {trcnt[i]}명")


            # 원형 그래프로 학점 분포를 시각화
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.pie(gradecnt, labels=gradelabs, autopct='%1.1f%%', startangle=140)
            plt.title(f'{giup}기업의 합격자 학점 분포')
            plt.axis('equal')

            plt.subplot(1, 2, 2)
            plt.pie(toeiccnt, labels=toeiclabs, autopct='%1.1f%%', startangle=140)
            plt.title(f'{giup}의 합격자 토익 점수 분포')
            plt.axis('equal')

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.pie(licencnt, labels=licenlabs, autopct='%1.1f%%', startangle=140)
            plt.title(f'{giup}의 합격자 자격증 분포')
            plt.axis('equal')

            plt.subplot(1, 2, 2)
            plt.pie(ratios, labels=titles, autopct='%1.1f%%', startangle=140)
            plt.title('자격증이 있는 합격자의 자격증 분포')
            plt.axis('equal')

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.pie(inrat, labels=intit, autopct='%1.1f%%', startangle=140)
            plt.title('인턴 경험이 있는 합격자의 분야 분포')
            plt.axis('equal')

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.pie(gorat, labels=gotit, autopct='%1.1f%%', startangle=140)
            plt.title('공모전 경험이 있는 합격자의 분야 분포')
            plt.axis('equal')

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.pie(trrat, labels=trtit, autopct='%1.1f%%', startangle=140)
            plt.title('연수 경험이 있는 합격자의 국가 분포')
            plt.axis('equal')
            plt.show()

        

    
        a = target(licens, k = 0)
        lileng = a[4]

        avglicen = lileng/len(grades)
        if int(avglicen) != round(avglicen, 1):
            avglicen = round(avglicen, 1)
        else: avglicen = int(avglicen)

        a = target(licens, k = round(avglicen))
        titles = a[0]

        a = target(interns, k = 0)
        inleng = a[4]

        avgintern = inleng/len(grades)
        if int(avgintern) != round(avgintern, 1):
            avgintern = round(avgintern, 1)
        else: avgintern = int(avgintern)

        a = target(interns, k = round(avgintern))
        intit = a[0]

        a = target(gongmos, k = 0)
        goleng = a[4]

        avggongmo = goleng/len(grades)
        if int(avggongmo) != round(avggongmo, 1):
            avggongmo = round(avggongmo, 1)
        else: avggongmo = int(avggongmo)

        a = target(gongmos, k = round(avggongmo))
        gotit = a[0]

        a = target(trips, k = 0)
        trleng = a[4]

        avgtrip = trleng/len(grades)
        if int(avgtrip) != round(avgtrip, 1):
            avgtrip = round(avgtrip, 1)
        else: avgtrip = int(avgtrip)

        a = target(trips, k = round(avgtrip))
        trtit = a[0]

        title = [titles, intit, gotit, trtit]

        return [avggrade, avgtoeic, avglicen, avgintern, avggongmo, avgtrip, title]
            
    else: print("기업이 존재하지 않습니다.")

def gear1(data, grade, toeic, licen, intern, gongmo, trip, two = True):
    if two == True:
        upjongs = part1(data)
    else: upjongs = part2(data)
    if upjongs:
        giups = [entry['기업'] for entry in upjongs if entry["학점"] != '']
        giups = set(giups)

        # 기업 평균
        avggrade, avgtoeic, avgli, avgin, avggo, avgtr = 0, 0, 0, 0, 0, 0
        # 사용자와 기업 평균 비교
        comgrade, comtoeic, comli, comin, comgo, comtr = 0, 0, 0, 0, 0, 0
        # 저장
        syngrade, syntoeic, synli, synin, syngo, syntr = [], [], [], [], [], []
        # 갯수
        cnt = 0
        total = []
        realsug = []
        suggest = []
        for giup in giups:
            avg = gear(upjongs, giup)
            total.append(avg)
            avggrade = avg[0]
            avgtoeic = avg[1]
            avgli = avg[2]
            avgin = avg[3]
            avggo = avg[4]
            avgtr = avg[5]

            comgrade = round(grade - avggrade,2)
            comtoeic = round(toeic - avgtoeic)
            comli = round(licen - avgli,1)
            comin = round(intern - avgin,1)
            comgo = round(gongmo - avggo,1)
            comtr = round(trip - avgtr,1)
            
            syn = [comgrade*5, comtoeic/100, comli, comin, comgo, comtr]

            realsug.append((sum(syn)))
            suggest.append(abs(sum(syn)))

            syn = [comgrade, comtoeic, comli, comin, comgo, comtr]

            for i, v in enumerate(syn):
                if v > 0: syn[i] = '+' + str(v)

            syngrade.append(syn[0])
            syntoeic.append(syn[1])
            synli.append(syn[2])
            synin.append(syn[3])
            syngo.append(syn[4])
            syntr.append(syn[5])

            # print(syngrade[cnt], syntoeic[cnt], synli[cnt], synin[cnt], syngo[cnt], syntr[cnt])

            cnt += 1

        index = sorted(range(len(suggest)), key=lambda k: suggest[k])
        giups = list(giups)
        for i in index:
            print(giups[i])
            print()
            print(total[i])
            print()
            print(f" 학점: {syngrade[i]}, 토익: {syntoeic[i]}, 자격증 갯수: {synli[i]}, 인턴 횟수: {synin[i]}, 공모전 횟수: {syngo[i]}, 연수 횟수: {syntr[i]}")
            print()
            print(f"총합 점수 : {realsug[i]:.2f}")
            print()
        return syngrade, syntoeic, synli, synin, syngo, syntr
    else: print("기업이 존재하지 않습니다.")
    
def gear2(data, grade, toeic, licen, intern, gongmo, trip):
    upjongs = [entry["업종별"] for entry in data]
    upjongs = delcomma(upjongs)
    upjong = set(upjongs)
    print(upjong)

    upjong = [input("업종을 입력하세요: ")]
    upjong = delcomma(upjong)
    upjong = set(upjong)
    print(upjong)

    upjongs = []
    if '전체' in upjong:
        upjongs = [entry for entry in data]

    else: 
        for j in upjong:
            for entry in data: 
                if entry.get("업종별") == j:
                    upjongs.append(entry)

    giuplist = [entry["기업"] for entry in upjongs if entry.get("기업") != '']
    giuplist = set(giuplist)
    print(giuplist)

    giup = input("기업을 입력하세요: ")
    
    # 기업의 지원자들의 학점 데이터 추출
    giupdata = [entry for entry in data if entry.get("기업") == giup]
   

    a = gear1(giupdata, grade, toeic, licen, intern, gongmo, trip, False)
    comgrade, comtoeic, comli, comin, comgo, comtr = a[0], a[1], a[2], a[3], a[4], a[5]

    print(comgrade, comtoeic, comli, comin, comgo, comtr)
    gear(giupdata, giup, graph = True)


rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False

# 예시 JSON 파일 경로
file_path = '/Users/junhi/Desktop/dataset.json'

# JSON 파일 읽기
json_data = read_json_file(file_path)


grade = float(input("학점을 입력하세요: "))

toeicox = input("토익이 있으십니까?: ")
if toeicox == '네':
    toeic = int(input("토익을 입력하세요: "))
else:toeic = 0

lics = [entry["자격증"] for entry in json_data]
licenox = input("자격증이 있으십니까?: ")
if licenox == '네':
    licen = [input("자격증을 입력하세요: ")]
else: licen = ['']
a = target(licen, k = 0)
licen = a[4]
print()

itns = [entry["인턴"] for entry in json_data]
internox = input("인턴 경험이 있으십니까?: ")
if internox == '네':
    intern = [input("인턴 경험을 입력하세요: ")]
else: intern = ['']
a = target(intern, k = 0)
intern = a[4]
print()

gms = [entry["공모전"] for entry in json_data]
gongmoox = input("공모전 경험이 있으십니까?: ")
if gongmoox == '네':
    gongmo = [input("공모전 경험을 입력하세요: ")]
else: gongmo = ['']
a = target(gongmo, k = 0)
gongmo = a[4]
print()

trs = [entry["연수"] for entry in json_data]
trip = input("연수 경험이 있으십니까?: ")
if trip == '네':
    trip = [input("연수 경험을 입력하세요: ")]
else: trip = ['']
a = target(trip, k = 0)
trip = a[4]
print()

jasoox = input("자기소개서가 있으십니까?: ")
if jasoox == '네':
    jaso = [input("자기소개서를 입력하세요: ")]
else: jaso = ['']

gear2(json_data, grade, toeic, licen, intern, gongmo, trip)

