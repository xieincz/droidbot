import shutil
import os
import json
from tqdm import tqdm

input_root_dir = "/home/xb/data/datasets/apks/unziped"
need_login_dir = "/home/xb/data/datasets/apks/unziped/need_login"

if __name__ == "__main__":
    categorys = os.listdir(input_root_dir)
    # 过滤出文件夹
    categorys = [
        category
        for category in categorys
        if os.path.isdir(os.path.join(input_root_dir, category))
    ]
    for category in categorys:
        if category == "need_login":
            continue
        src_apk_dir = os.path.join(input_root_dir, category)
        need_login_apk_dir = os.path.join(need_login_dir, category)
        os.makedirs(need_login_apk_dir, exist_ok=True)
        js_fp = os.path.join(need_login_dir, category + "_need_login.json")
        need_login_apks = []
        with open(js_fp, "r", encoding="utf-8") as f:
            need_login_apks = json.load(f)
        for apk_fn in tqdm(need_login_apks, desc=category):
            shutil.move(
                os.path.join(src_apk_dir, apk_fn),
                os.path.join(need_login_apk_dir, apk_fn),
            )

    print("All done")
