from datetime import datetime

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%Y년 %m월 %d일, %A. %H:%M")
    # 요일을 한국어로 변환
    weekdays = {
        'Monday': '월요일', 'Tuesday': '화요일', 'Wednesday': '수요일',
        'Thursday': '목요일', 'Friday': '금요일', 'Saturday': '토요일', 'Sunday': '일요일'
    }
    current_time = current_time.replace(now.strftime('%A'), weekdays[now.strftime('%A')])
    return current_time