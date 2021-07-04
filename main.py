from QueryGrade import login
from requests import Session
from QueryGrade.query_grade import query_grade

if __name__ == "__main__":
    username = input("学号(统一认证号): ")
    password = input("密码:")
    query_grade(username, password)