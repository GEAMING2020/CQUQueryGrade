# CQUQueryGrade
重庆大学学生成绩查询（新教务网），也可以参考思路实现认证<br>
注意：统一认证网页输入的学号和密码一旦错三次将会产生验证码认证，该脚本并未实现验证码处理，所以三次以内必须输入正确用户名和密码

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate  # 环境激活因平台而异
pip install -r requirements.txt
python main.py
```