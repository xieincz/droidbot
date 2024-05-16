import subprocess as sp
import os
from glob import glob
import shutil
import random
import argparse


# droidbot -keep_env -grant_perm -ignore_ad -count 10800 -a "Firefox Fast & Private Browser_125.3.0_APKPure.apk" -o output_dir_apk_name
# If you are using multiple devices, you may need to use -d <device_serial> to specify the target device.
# The easiest way to determine a device's serial number is calling `adb devices`.
def run_droidbot(apk_path: str, output_dir_path: str, device_serial: str):
    assert os.path.exists(apk_path), "APK file not found"
    ret = sp.run(
        [
            "droidbot",
            "-keep_env",
            "-grant_perm",
            "-ignore_ad",
            "-count",
            # "10800",# about 3 hours
            "18000",  # about 5 hours
            "-a",
            apk_path,
            "-o",
            output_dir_path,
            "-d",
            device_serial,
        ],
        capture_output=True,
    )
    if ret.returncode != 0:
        print(ret.stdout.decode("utf-8"))
        print("\n")
        print(ret.stderr.decode("utf-8"))
        return False
    return True


def contains_apk_files(directory: str):
    return len(glob(os.path.join(directory, "*.apk"))) > 0


def process_one_apk(
    input_category_dir, processing_dir, finished_dir, output_category_dir, device_serial
):
    apk_fps = glob(os.path.join(input_category_dir, "*.apk"))

    if len(apk_fps) > 0:
        # apk_fp = apk_fps[0]
        # randomly select an apk file in order to distribute the workload
        apk_fp = random.choice(apk_fps)
        apk_fn = os.path.basename(apk_fp)
        processing_fp = os.path.join(processing_dir, apk_fn)
        if os.path.exists(processing_fp):
            os.remove(apk_fp)
            print(f"Already processing {apk_fp}, removing it from input dir")
            return True
        finished_fp = os.path.join(finished_dir, apk_fn)
        if os.path.exists(finished_fp):
            os.remove(apk_fp)
            print(f"Already finished {apk_fp}, removing it from input dir")
            return True
        # begin processing
        shutil.move(apk_fp, processing_fp)
        print(f"Processing {apk_fp}")
        ok = run_droidbot(
            processing_fp, os.path.join(output_category_dir, apk_fn), device_serial
        )
        if ok:
            shutil.move(processing_fp, finished_fp)
        else:
            shutil.move(processing_fp, apk_fp)
        return ok


def worker(
    category: str = "tools",  # need to change this
    device_serial: str = "HA1PZJW9",  # need to change this, use `adb devices` to get the serial number
    input_root_dir: str = "apks",
    output_root_dir: str = "utg",
):
    input_category_dir = os.path.join(input_root_dir, category)
    output_category_dir = os.path.join(output_root_dir, category)
    os.makedirs(output_category_dir, exist_ok=True)

    processing_dir = os.path.join(input_category_dir, "processing")
    os.makedirs(processing_dir, exist_ok=True)
    finished_dir = os.path.join(input_category_dir, "finished")
    os.makedirs(finished_dir, exist_ok=True)

    cnt = 0
    while contains_apk_files(input_category_dir):
        if not process_one_apk(
            input_category_dir,
            processing_dir,
            finished_dir,
            output_category_dir,
            device_serial,
        ):
            print(f"Error encountered when processing {category} apks")
            break
        cnt += 1
        if cnt % 10 == 0:
            print(f"Processed {cnt} {category} apks")
    print(f"Processed {cnt} {category} apks")
    exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DroidBot on APKs")
    parser.add_argument(
        "-d",
        action="store",
        dest="device_serial",
        #required=True,
        default="HA1PZJW9",
        help="The serial number of target device (use `adb devices` to find)",
    )
    parser.add_argument(
        "-i",
        action="store",
        dest="input_root",
        #required=True,
        default="apks",
        help="directory of input",
    )
    parser.add_argument(
        "-o",
        action="store",
        dest="output_dir",
        #required=True,
        default="utg",
        help="directory of output",
    )
    parser.add_argument(
        "-c",
        action="store",
        dest="category",
        #required=True,
        default="tools",
        help="category of APKs, must be a subdirectory of the input folder",
    )

    args = parser.parse_args()
    category = args.category
    device_serial = args.device_serial
    input_root_dir = args.input_root
    output_root_dir = args.output_dir
    worker(category, device_serial, input_root_dir, output_root_dir)
