from androguard.util import set_log

set_log("ERROR")  # 关闭琐碎的DEBUG输出
from androguard.misc import (
    AnalyzeAPK,
)  # https://androguard.readthedocs.io/en/latest/intro/gettingstarted.html
from glob import glob
import os
from tqdm import tqdm
import json
import multiprocessing as mp

# List of keywords to search for
keywords = [
    "login",
    "signin",
    "sign_in",
    "log_in",
    "loginactivity",
    "signinactivity",
    "loginscreen",
    "loginpage",
    "account",
    "accountactivity",
    "accountscreen",
    "accountpage",
    "myaccount",
    "register",
    "signup",
    "sign_up",
    "registration",
    "registeractivity",
    "signupactivity",
    "registrationactivity",
    "auth",
    "authentication",
    "authactivity",
    "authenticate",
    "credential",
    "password",
    "passcode",
    "pin",
    "pincode",
]


def is_login_required(apk_fp):
    """
    Check if the APK needs login
    :param apk_fp: APK file path
    :return: True if the APK needs login, False otherwise
    """
    a, d, dx = AnalyzeAPK(apk_fp)
    activity_list = a.get_activities()
    # Check if any activity contains any of the keywords, case-insensitively
    contains_keyword = any(
        any(keyword.lower() in activity.lower() for keyword in keywords)
        for activity in activity_list
    )
    return contains_keyword


def process_dir(apk_dir, tqdm_pos=0):
    apk_fps = glob(os.path.join(apk_dir, "*.apk"))
    folder_name = os.path.basename(apk_dir)
    res = []
    for apk_fp in tqdm(apk_fps, desc=folder_name, position=tqdm_pos):
        if is_login_required(apk_fp):
            fn = os.path.basename(apk_fp)
            res.append(fn)
    return res


def process_category(category, input_root_dir, output_root_dir, tqdm_pos=0):
    apk_dir = os.path.join(input_root_dir, category)
    res = process_dir(apk_dir, tqdm_pos)
    with open(
        os.path.join(output_root_dir, category + "_need_login.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


def main():
    input_root_dir = "apks"
    output_root_dir = "need_login"
    os.makedirs(output_root_dir, exist_ok=True)
    categorys = os.listdir(input_root_dir)
    # 过滤出文件夹
    categorys = [
        category
        for category in categorys
        if os.path.isdir(os.path.join(input_root_dir, category))
    ]
    # for category in categorys:
    #    process_category(category, input_root_dir, output_root_dir)
    processes = []
    tqdm_pos = 0
    try:
        for category in categorys:
            p = mp.Process(
                target=process_category,
                args=(category, input_root_dir, output_root_dir, tqdm_pos),
            )
            tqdm_pos += 1
            p.daemon = True
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("Interrupted by user, cleaning up...")
        for p in processes:
            p.terminate()
    print("All done")


if __name__ == "__main__":
    main()
