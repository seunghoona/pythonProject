import time

import pyperclip as pyperclip
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys



#클립보드에 input을 복사한 뒤
#해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기

def copy_input(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

id = 'khigkrdlf'
pw = 'rlahaK7254'

# chrome 드라이버
driver = webdriver.Chrome('../chromedriver.exe')

driver.get('https://nid.naver.com/nidlogin.login?svctype=262144')

#네이버 로그인 페이지
driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

#로그인정보 입력
copy_input('//*[@id="id"]', id)
copy_input('//*[@id="pw"]', pw)

#로그인 상태유지
driver.find_element_by_xpath('//*[@id="label_login_chk"]').click()
time.sleep(1)

# 로그인 클릭
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

time.sleep(2)

#카페이동
driver.get('https://cafe.naver.com/motiontree')

#카페 메뉴이동
base_url = 'https://cafe.naver.com/motiontree/ArticleList.nhn?search.clubid=20409993'


page = 0  # 카페 게시판 페이지


#Excel 파일 만들기위한 변수 선언
titleList = []
contentList =[]
commentList =[]


#조회하고자 하는 페이지 수
while page < 95:
    page = page + 1
    quest_urls = []
    try:
        # add personal conditions
        # &search.menuid = : 게시판 번호(카페마다 상이)
        # &search.page = : 데이터 수집 할 페이지 번호
        # &userDisplay = 50 : 한 페이지에 보여질 게시글 수
        driver.get(base_url + '&search.menuid=631&search.page=' + str(page) + '&userDisplay=50')
        driver.switch_to.frame('cafe_main')  # iframe으로 프레임 전환
        quest_list = driver.find_elements_by_css_selector('div.inner_list > a.article')  # 이 태그 부분 카페마다 다르다던데....
        quest_urls = [i.get_attribute('href') for i in quest_list] # 게시판 개수
        print("".join(["페이지수",str(page)]))
        # 게시판 개수만큼  만큼 반복
        for quest in quest_urls:

            try:  # 게시글이 삭제되었을 경우가 있기 때문에 try-exception

                driver.get(quest)
                driver.switch_to.frame('cafe_main')
                time.sleep(3)
                soup = bs(driver.page_source, 'html.parser')
                try:


                    # 제목 추출
                    # title = soup.find('.title_text')
                    rexTitle = str(soup.find('h3',{'class':'title_text'}))
                    title = re.sub('<.+?>', '', rexTitle, 0).strip()
                    print(title)

                    # 내용 추출

                    rexContent_tags = str(soup.find('div',{'class':'ContentRenderer'}))
                    content = re.sub('<.+?>', '', rexContent_tags, 0).strip()
                    print(content)

                    # 답변 추출
                    tagComment = soup.find('ul', {'class': 'comment_list'})
                    tagCommentLi = str(tagComment.findAll("span"))
                    comment = re.sub('<.+?>', '', tagCommentLi, 0).strip()

                    print(comment)
                #답변이 없으면 패쓰
                except Exception as ex:  # 에러 종류
                    print('답글에러가 발생했습니다', ex)
                    pass
                time.sleep(5)

                titleList.append(title)
                contentList.append(content)
                commentList.append(comment)


            except:  # chrome alert창 처리해줌
                driver.switch_to_alert.accpet()
                driver.switch_to_alert
                driver.switch_to_alert.accpet()
    except Exception as ex:  # 에러 종류
        print('전체 에러가 발생했습니다. ', ex)
        pass




index_format = titleList
columns_format = ['제목', '내용', '답글']
values = pd.DataFrame(index=index_format, columns=columns_format)
print(values)

# x & y 값 정의
x = titleList
y = contentList
z = commentList

for ii in range(values.shape[0]):
    values.iloc[ii, 0] = x[ii]

    values.iloc[ii, 1] = y[ii]

    values.iloc[ii, 2] = z[ii]

values.to_excel('./motiontree.xlsx',
                sheet_name='Sheet1',
                columns=columns_format,
                header=True,
                index=index_format,
                index_label="제목",
                startrow=1,
                startcol=0,
                engine=None,
                merge_cells=True,
                encoding=None,
                inf_rep='inf',
                verbose=True,
                freeze_panes=None)


