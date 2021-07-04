from QueryGrade import login
from requests import Session
from QueryGrade.query_grade import query_grade

if __name__ == "__main__":
    username = "20181656"
    password = "7509220qaz"
    query_grade(username, password)