![DroidBot UTG](droidbot/resources/dummy_documents/droidbot_utg.png)

# DroidBot

## Prerequisite

1. `Python` (Python 3.10 is recommended)
2. `Java` (JDK1.8 is recommended)
3. `Android SDK`
4. Add `platform_tools` directory in Android SDK to `PATH`

## How to install

Clone this repo and install with `pip`:

```shell
conda create -n droidbot python=3.10 -y
conda activate droidbot
cd droidbot/
pip install -e .
```

If successfully installed, you should be able to execute `droidbot -h`.

## How to use

Place the apk according to the following directory structure: 

```bash
apks_dir
├─communication
├───com.whatsapp.w4b.apk
├───com.google.android.contacts.apk
├───......
├─entertainment
├─productivity
├─shopping
├─social
├─tools
└─video_players
```

Connect your android devices to that computer via adb, you should be able to see them via the `adb devices` command, the string like "HA1PZJW9" in there is device_serial, you need to replace the "HA1PZJW9".

```bash
conda activate droidbot
cd droidbot/
python run.py -d HA1PZJW9 -i path/to/apks_dir -o path/to/output_dir -c tools
#-d: The serial number of target device (use `adb devices` to find)
#-i: directory of input
#-o: directory of output
#-c: category of APKs, must be a subdirectory of the input folder
```



## Acknowledgement

1. [AndroidViewClient](https://github.com/dtmilano/AndroidViewClient)
2. [Androguard](http://code.google.com/p/androguard/)
3. [The Honeynet project](https://www.honeynet.org/)
4. [Google Summer of Code](https://summerofcode.withgoogle.com/)
5. [DroidBot](https://github.com/honeynet/droidbot)
