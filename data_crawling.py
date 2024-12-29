from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import Workbook
import time

#에러없이 복사해주는 함수
def tryto(xpath):
    try:
        mother = driver.find_element(By.XPATH, xpath)
        child = mother.find_element(By.XPATH, "..").text
        return child
    except NoSuchElementException:
        return "none"
    
#크롬 드라이버
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://portal.koreatech.ac.kr/login.jsp")

#엑셀
wb = Workbook()
ws = wb.active
ws.title = "emp1"
col = ['기업', '업종별', '구분', '지원분야', '학교', '학점', '토익', '오픽', '자격증', '인턴', '공모전', '연수', '자소서 질문', '자소서 답변']
ws.append(col)

# 로그인 정보 입력
elem = driver.find_element(By.ID, 'user_id')
elem.send_keys('')
elem = driver.find_element(By.ID, 'user_pwd')
elem.send_keys('')
elem.send_keys(Keys.RETURN)

# 잡솔루션
time.sleep(0.5)
driver.get("https://job.koreatech.ac.kr/jobs/educe.aspx/passReport?p=sub")
time.sleep(0.5)

#잡솔루션
driver.execute_script('window.open("https://u.educe.co.kr/jobkut/passReport?p=sub");')  #구글 창 새 탭으로 열기
time.sleep(0.5)

#새로 연 탭으로 이동
driver.switch_to.window(driver.window_handles[1]) 

#업종별
sectors = [driver.find_element(By.CSS_SELECTOR, '#category_scroll > ul').text]

sectits = []
count = 0
for target in sectors:
        i = 0
        n = 0
        while 1:
            try:
                index = target.index('\n', i)
                sectits.append(target[i:index])
                i = index + len('\n')
                n += 1
            except ValueError:
                if target != '':
                    sectits.append(target[i:])
                    n += 1
                break

for _ in range(11):
    sectits.pop(0)


for title in secti ts:
    sector = title
    element = driver.find_element(By.XPATH, f"//*[contains(text(), '{title}')]")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

    # 요소 클릭
    element.click()
    time.sleep(0.5)

    #페이지 번호 저장
    cnt = ''

    while 1:   
        #새로 연 탭으로 이동
        driver.switch_to.window(driver.window_handles[1]) 

        #한페이지의 기업 수
        cpnlen = driver.find_elements(By.CSS_SELECTOR, ".title.cursor-pointer")

        #페이지 번호
        try:
            on = driver.find_element(By.CSS_SELECTOR, '.on').text
        except NoSuchElementException:
            on = 1
        #페이지 번호가 다를때
        if on != cnt:
            for i in range(len(cpnlen)):   
                #새로 연 탭으로 이동
                driver.switch_to.window(driver.window_handles[1]) 

                #기업 복사
                cpn = driver.find_elements(By.CSS_SELECTOR, ".title.cursor-pointer")[i].text

                #기업 이름만 복사
                if cpn.find(" 합") != -1:
                    cpn = cpn[:cpn.index(" 합")]
                elif cpn.find(" 4") != -1:
                    cpn = cpn[:cpn.index(" 4")]
                elif cpn.find(" 3") != -1:
                    cpn = cpn[:cpn.index(" 3")]
                elif cpn.find(" 2") != -1:
                    cpn = cpn[:cpn.index(" 2")]
                elif cpn.find(" 1") != -1:
                    cpn = cpn[:cpn.index(" 1")]
                elif cpn.find(" 0") != -1:
                    cpn = cpn[:cpn.index(" 0")]
                
                
                #합격자 자기소개서
                driver.find_elements(By.XPATH, "//*[contains(text(),'내용보기')]")[i].click()
                time.sleep(0.5)

                #새로 연 탭으로 이동
                driver.switch_to.window(driver.window_handles[-1])

                #복사
                div = driver.find_element(By.CSS_SELECTOR, "#print_area > div > div.view-subject > span > span").text
                field = tryto('//li/strong[contains(text(), "지원분야")]')[7:]
                univ = tryto('//li/strong[contains(text(), "학교")]')[5:]         
                grade = tryto('//li/strong[contains(text(), "학점")]')[5:]
                toeic = tryto('//li/strong[contains(text(), "토익")]')[7:]
                opic = tryto('//li/strong[contains(text(), "오픽")]')[7:]
                licen = tryto('//li/strong[contains(text(), "자격증")]')[6:]
                intern = tryto('//li/strong[contains(text(), "인턴")]')[5:]
                gongmo = tryto('//li/strong[contains(text(), "공모전")]')[6:]
                trip = tryto('//li/strong[contains(text(), "연수")]')[5:]

                quests = driver.find_elements(By.CSS_SELECTOR, ".mt30")
                answers = driver.find_elements(By.CSS_SELECTOR, ".mb50.contents")
                
                fullque = ""
                fullans = ""
                num = 0
            
                # for title, text in zip(titles, texts):
                #     realText += title.text + "\n\n" + text.text + "\n\n"
                
                for quest, answer in zip(quests, answers):
                    fullque += str(num + 1) + "번째 질문 : " + quest.text + "\n\n"
                    fullans += str(num + 1) + "번째 답변 : " + answer.text + "\n\n"
                    num +=1

                #마지막쯤 페이지에 데이터가 없는 것이 있음
                if univ == '' : continue
                if grade == '' : continue
                
                #나중에 업데이트 할 때 중복 제거
                if cpn == '' and field == '' and grade == '' and toeic == '' and licen == '':
                    break
                
                col = [cpn, sector, div, field, univ, grade, toeic, opic, licen, intern, gongmo, trip, fullque, fullans]
                #엑셀 저장
                ws.append(col)
                count += 1
                print(count, " ok")
                #창닫기
                driver.close()

            #새로 연 탭으로 이동
            driver.switch_to.window(driver.window_handles[1])
            try:
                nextbtn = driver.find_element(By.CSS_SELECTOR, ".next")
            except NoSuchElementException:
                break
            cnt = on
            nextbtn.click()
            time.sleep(0.5)

        else: break

    wb.save(r'C:\Users\user\Desktop\dataset.xlsx.')

#엑셀 저장
wb.save(r'C:\Users\user\Desktop\dataset.xlsx.')
wb.close()
