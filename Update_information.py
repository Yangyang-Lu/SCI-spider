import os
import shutil


def copy_allfiles(src, dest):
#src:原文件夹；dest:目标文件夹
  src_files = os.listdir(src)
  for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, dest)


def Update_information():
    src = str(str(os.path.split(os.path.realpath(__file__))[0]) + "\\data\\Temp")
    dest = str(str(os.path.split(os.path.realpath(__file__))[0]) + "\\data")
    copy_allfiles(src, dest)

