from QueryGrade.query_grade import query_grade
import os
if __name__ == "__main__":
    username = input("学号(统一认证号): ")
    password = input("密码:")
    query_grade(username, password)
    os.system("pause")
