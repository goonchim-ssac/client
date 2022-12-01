import re
from datetime import date

# df / 22. / 10 23/ d

# 날짜형식 확인
def check_date(year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    thisyear = date.today().year - 2000

    # +/-10년 사이인 유통기한만 처리

    start_year = thisyear - 10
    end_year = thisyear + 10

    if year < start_year or end_year < year:
        return 0

    # 월/일 형식 확인
    if month >= 1 and month <= 12:
       
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            if day >= 1 and day <= 31:
                return 1
            
        elif month == 4 or month == 6 or month == 9 or month == 11:
            if day >= 1 and day <= 30:
                return 1
            
        elif month == 2:
            
            # 윤년 판별
            if (year % 100 != 0 and year % 4 == 0) or (year % 400 == 0):
                if day >= 1 and day <= 29:
                    return 1
            elif day >= 1 and day <= 28:
                return 1

    return 0

# OCR병합, 숫자만 남김
def change_num(ocr_list):
    
    ocr_word = ''.join(ocr_list)
    date_n = re.sub(r'[^0-9]', '', ocr_word)

    return date_n



# 유통기한(yyyy/mm/dd) 형식으로 변경
def change_ex(ocr_list): #date_n
    date_n = change_num(ocr_list)
    size = len(date_n)
    exdate = []
    year = any
    month = any
    day = any
    
    # 해외 주류
    if size == 8 and check_date(date_n[4:8], date_n[2:4], date_n[0:2]):
        exdate.append(f'{date_n[4:8]}/{date_n[2:4]}/{date_n[0:2]}')

    # 4자리 : 유제품류 mm dd
    elif size == 4:
    
        month = date_n[0:2]
        day = date_n[2:4]
        today = date.today()
        today_m = str(date.today().month)

        if today_m == '12' and month == '01':
            exdate.append(f'{today.year + 1}/{month}/{day}')
        else:
            exdate.append(f'{today.year}/{month}/{day}')

    # 6자리 : yy mm dd / mm dd yy
    elif size == 6:
    
        if date_n[0] == '2':
            year = date_n[0:2]
            month = date_n[2:4]
            day = date_n[4:6]
            
        else:
            year = date_n[4:6]
            month = date_n[0:2]
            day = date_n[2:4]
            
        result = check_date(year, month, day)
        
        if result == 1:
            exdate.append(f'20{year}/{month}/{day}')
            
                
    # 8자리 : (yy)yy mm dd / mm dd (yy)yy
    elif size == 8:
        
        if date_n[0] == '2': 
            year = date_n[2:4]
            month = date_n[4:6]
            day = date_n[6:8]
                
        else:
            year = date_n[6:8]
            month = date_n[0:2]
            day = date_n[2:4]

        result = check_date(year, month, day)
        
        if result == 1:
            exdate.append(f'20{year}/{month}/{day}')
                
    # 그외 : 정보부족/전처리안됨
    else:
        exdate.append("")

    return exdate


def text_postprocessing():
    '''
    수정한 후처리 코드로 변경 필요
    '''
    pass

if __name__ == "__main__":
    print(change_ex(['22','10.10']))
