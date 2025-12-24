import os
from datetime import datetime
import subprocess

# 定义要处理的目录
dir_path = "content/posts"  # 请确保这里的路径与你项目中的实际路径一致

# 定义用于生成 Front Matter 的模板
def generate_front_matter(filename):
    # 获取当前文件的创建时间作为日期
    creation_time = datetime.fromtimestamp(os.path.getctime(filename))
    date_str = creation_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    # 生成 Front Matter
    title = filename.split('.')[0]  # 简单地将文件名作为标题
    front_matter = f"---\ntitle: \"{title}\"\ndate: {date_str}\ntags: []\ncategories: []\n---\n"
    return front_matter

# 遍历目录中的所有 markdown 文件
for filename in os.listdir(dir_path):
    if filename.endswith(".md"):
        file_path = os.path.join(dir_path, filename)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 检查是否已有 Front Matter
        if not content.startswith("---\n"):
            # 如果没有 Front Matter，则生成并添加它
            front_matter = generate_front_matter(file_path)

            # 写入 Front Matter 到文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(front_matter + content)
            
            print(f"Added Front Matter to: {filename}")
        else:
            print(f"Front Matter already exists for: {filename}")

# 提交和推送到 Git 仓库
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', 'Auto-generated or updated Front Matter'])
subprocess.run(['git', 'push', 'origin', 'main'])

print("Changes have been pushed to the repository.")
