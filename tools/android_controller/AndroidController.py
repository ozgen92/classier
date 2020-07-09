import subprocess


class AndroidController:
    emulator_process = None

    def __init__(self, device_name="Pixel3a"):
        self.open_device(device_name=device_name)

    def open_device(self, device_name="Pixel3a"):
        self.close_device()
        # ~/Library/Android/sdk/emulator/emulator -avd Pixel3a
        self.emulator_process = subprocess.Popen(f"~/Library/Android/sdk/emulator/emulator -avd {device_name}", shell=True)

    def close_device(self):
        if self.emulator_process is not None:
            self.emulator_process.kill()

    @staticmethod
    def run_shell_command(shell_command):
        return subprocess.check_output(f"adb shell {shell_command}", shell=True).decode()

    @staticmethod
    def stop_app(app_name="ch.post.it.pcc"):
        # adb shell am force-stop ch.post.it.pcc
        subprocess.call(f"adb shell am force-stop {app_name}", shell=True)

    @classmethod
    def start_app(cls, app_name="ch.post.it.pcc"):
        # adb shell am start -n ch.post.it.pcc
        return subprocess.check_output(f"adb shell am start -n {cls._get_main_activity_name(app_name)}", shell=True).decode()

    @staticmethod
    def list_packages():
        # adb shell pm list packages
        return subprocess.check_output("adb shell pm list packages", shell=True).decode()

    @classmethod
    def start_google_play(cls):
        return cls.start_app("com.android.vending/com.google.android.finsky.activities.MainActivity")

    @classmethod
    def press_home_button(cls):
        # input keyevent 3
        return cls.run_shell_command("input keyevent 3")

    @staticmethod
    def _get_main_activity_name(app_name="ch.post.it.pcc"):
        return subprocess.check_output(f'adb shell "cmd package resolve-activity --brief {app_name} | tail -n 1"', shell=True).decode()

    @staticmethod
    def get_screen_size():  # width x height: 1080x2220
        return subprocess.check_output("adb shell wm size", shell=True).decode()

    @staticmethod
    def touch(x, y):
        # adb shell input tap 200 1700
        subprocess.call(f"adb shell input tap {x} {y}", shell=True)

    @staticmethod
    def write(text):
        # adb shell input text "8048"
        subprocess.call(f"adb shell input text {text}", shell=True)

    @staticmethod
    # adb push ~/Desktop/Backup/Pictures/postcard/pauls-birthday.jpeg /sdcard/Pictures
    def push_file(file_path, target_path="/sdcard/Pictures"):
        subprocess.call(f"adb push {file_path} {target_path}", shell=True)

    @staticmethod
    # adb shell rm /sdcard/Pictures/pauls-birthday.jpeg
    def remove_file(file_path="/sdcard/Pictures/pauls-birthday.jpeg"):
        subprocess.call(f"adb shell rm {file_path}", shell=True)


# import os
# FILE_PATH="~/Desktop/Backup/Pictures/postcard/pauls-birthday.jpeg"
# FILE_NAME=os.path.basename(FILE_PATH)
# FILE_NAME_NICE=os.path.splitext(FILE_NAME)[0].replace("-", " ").replace("_", " ")
# from classier.tools.android_controller.AndroidController import AndroidController
# controller = AndroidController(device_name="Pixel3a")
# controller.stop_app(app_name="ch.post.it.pcc")
# controller.start_app(app_name="ch.post.it.pcc")
# controller.push_file(file_path=FILE_PATH, target_path="/sdcard/Pictures")
# controller.touch(500, 1200)  # Create free postcard button
# controller.touch(500, 1700)  # Select image button
# controller.touch(800, 400)  # Photos
# controller.touch(500, 600)  # Pictures
# controller.touch(200, 400)  # left top picture
# controller.touch(200, 1200)  # ok
# controller.touch(500, 2000)  # next
## controller.touch(500, 1800)  # sender
# controller.touch(500, 1700)  # recipient
# controller.touch(500, 300)  # address book
# controller.touch(500, 300)  # ozgen
# controller.touch(150, 1450)  # postcode
# controller.write("8048")  # postcode
# controller.touch(950, 2000)  # ok
# controller.touch(500, 1550)  # enter message
# controller.write(FILE_NAME_NICE)  # postcode
# controller.touch(500, 700)  # ok
# controller.touch(500, 1900)  # next
# controller.touch(950, 1340)  # gtc accept
# controller.touch(500, 1900)  # send
# controller.remove_file(target_path=f"/sdcard/Pictures/{FILE_NAME}")
# controller.stop_app(app_name="ch.post.it.pcc")
# controller.close_device()
