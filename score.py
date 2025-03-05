"""
项目计分程序。

用法1：计算某个项目的得分
  python score.py --project <用户名>/<项目目录>

用法2：计算某个用户的得分明细
  python score.py --user <用户名>

用法3：计算所有项目得分
  python score.py --all

如一次性指定多个参数，则优先级为：--project > --user > --all
"""

import os
import sys
import json
import argparse

# 忽略的目录和文件扩展名
IGNORE_DIRS = ['.git', '__pycache__', '.idea', '.vscode']
IGNORE_EXTENSIONS = ['.gitignore', '.DS_Store', '.md', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.pack', '.idx']

def score(string: str) -> int:
    """
    计算给定字符串的ASCII码之和。包括空格、换行符等。
    """
    return sum(ord(c) for c in string)

def score_file(path: str) -> int:
    """
    计算给定文件的ASCII码之和。
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return score(content)
    except UnicodeDecodeError:
        # 如果文件不是文本文件，则跳过
        print(f"警告: 跳过二进制文件 {path}")
        return 0

def score_dir(path: str) -> int:
    """
    遍历目录及子目录下的所有文件，排除忽略的文件名（或文件扩展名），计算所有文件的ASCII码之和。
    遇到无法读取的文件，则跳过该文件。
    报告总分和得分明细。
    例如：
    总分：190
    ./main.py 120
    ./utils/string.py 70
    """
    total_score = 0
    score_details = []
    
    for root, dirs, files in os.walk(path):
        # 忽略特定目录
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # 检查文件扩展名是否在忽略列表中
            should_ignore = False
            for ignore in IGNORE_EXTENSIONS:
                if file.endswith(ignore):
                    should_ignore = True
                    break
            
            if should_ignore:
                continue
                
            try:
                file_score = score_file(file_path)
                total_score += file_score
                score_details.append([f"{file_path}", file_score])
            except Exception as e:
                print(f"警告: 无法读取文件 {file_path}: {e}")
                continue
                
    return total_score, score_details

def score_user(user_path: str):
    """
    遍历用户目录下所有项目目录，计算所有项目的得分。
    输出项目得分明细，以及最低得分项目
    """
    score_details = {}
    min_score_program = []
    for project in os.listdir(user_path):
        project_path = os.path.join(user_path, project)
        if os.path.isdir(project_path):
            score, details = score_dir(project_path)
            score_details[project] = {
                "score": score,
                "details": details
            }
            if not min_score_program or score < min_score_program[1]:
                min_score_program = [project, score]
    return score_details, min_score_program

def score_all():
    """
    遍历根目录下所有用户目录，计算所有用户的得分。
    输出每个用户的最低得分项目
    """
    all_score_details = {}
    for user in os.listdir('.'):
        if os.path.isdir(user) and user not in IGNORE_DIRS:
            user_score_details, min_score_program = score_user(user)
            all_score_details[user] = {
                "projects": user_score_details,
                "best_program": min_score_program
            }
    return all_score_details

def coculate(type: str, path: str):
    if type == "project":
        if os.path.isdir(path):
            score, details = score_dir(path)
            print(f"总分: {score}")
            print(f"以下是得分明细：")
            for detail in details:
                print(f"- {detail[0]} {detail[1]}")
        else:
            print(f"未找到项目 {path}")
    elif type == "user":
        if os.path.isdir(path):
            score_details, min_score_program = score_user(path)
            print(f"以下是得分明细：")
            for project, detail in score_details.items():
                print(f"- {project} {detail['score']}")
            print(f"最佳项目: {min_score_program[0]} ;得分： {min_score_program[1]}")
        else:
            print(f"未找到用户 {path}")
    elif type == "all":
        score_details = score_all()
        user_list = []
        for username, details in score_details.items():
            best_program = details.get("best_program")
            if len(best_program) > 1:
                best_score = best_program[1]
                user_list.append([username, best_program[0], best_score])
        # 排序
        user_list.sort(key=lambda x: x[2])
        print("以下是得分明细（按分数从低到高排序，分数越低越好）：")
        print("用户|最佳项目|得分")
        for u in user_list:
            print(*u, sep="|")
        with open("score.json", "w") as f:
            json.dump(score_details, f, indent=4)
        print(f"已将结果保存到 score.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, help="计算某个项目的得分")
    parser.add_argument("--user", type=str, help="计算某个用户的得分明细")
    parser.add_argument("--all", action="store_true", help="计算所有用户的得分")
    args = parser.parse_args()
    if args.project:
        coculate("project", args.project)
    elif args.user:
        coculate("user", args.user)
    elif args.all:
        coculate("all", "")
    else:
        _ = input("请输入要统计的用户/项目，留空则统计所有：")
        if "/" in _:
            coculate("user", _)
        elif _:
            coculate("project", _)
        else:
            coculate("all", "")
