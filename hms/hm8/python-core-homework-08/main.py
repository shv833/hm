from datetime import date, datetime, timedelta
from pprint import pprint
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")

# return example
# {'Monday': ['Bill', 'Jan'], 'Wednesday': ['Kim']}
def close_birthday_users(users, start, end):
    now = datetime.today().date()
    result = []
    for user in users:
        birthday = user.get('birthday').replace(year=now.year)
        if start <= birthday <= end:
            result.append(user)
    return result

def get_birthdays_per_week(users):
    if not users:
        return {}
    TEST = timedelta(days=2)
    
    now = datetime.today().date()  #+ TEST
    current_week_day = now.weekday()
    start_date = now
        
    end_date = now + timedelta(days=6)
    
    birthday_users = close_birthday_users(users, start=start_date, end=end_date)
    weekday = None
    if not birthday_users:
        return {}
    
    res = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": []
    }

    for user in sorted(birthday_users, key=lambda x: x['birthday'].replace(year=now.year)):
        user_birthday = user.get('birthday').replace(year=now.year).weekday()
        try:
            user_happy_day = WEEKDAYS[user_birthday]
        except IndexError:
            user_happy_day = WEEKDAYS[0]
        if weekday != user_happy_day:
            weekday = user_happy_day

        res[weekday].append(user.get('name'))
    
    test_res = {}
    for key, val in res.items():
        if val:
            test_res[key] = val
    return test_res
    # return res


if __name__ == "__main__":
    users = [
        {"name": "0", "birthday": datetime(1976, 1, 1).date()},
        {"name": "1", "birthday": datetime(2023, 11, 26).date()},
        {"name": "2", "birthday": datetime(2023, 11, 27).date()},
        {"name": "3", "birthday": datetime(2023, 11, 28).date()},
        {"name": "4", "birthday": datetime(2023, 11, 29).date()},
        {"name": "5", "birthday": datetime(2023, 11, 30).date()},
        {"name": "6", "birthday": datetime(2023, 12, 1).date()},
        {"name": "7", "birthday": datetime(2023, 12, 2).date()},
        {"name": "8", "birthday": datetime(2023, 12, 3).date()},
        {"name": "9", "birthday": datetime(2023, 12, 5).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
