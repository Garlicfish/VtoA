import os
import PySimpleGUI as sg
from core import download_video, extract_audio_from_video, move_file

sg.theme('Dark Teal 7')


def get_filename_from_filepath(filepath):
    return os.path.basename(filepath).split('.')[0]


layout = [
    [sg.Text('请输入资源网址:', font=("Helvetica", 13)), sg.InputText(
        key='URL', size=(51, 1), font=("Helvetica", 13))],
    [
        sg.Text('视频文件所在文件夹: ', font=("Helvetica", 13)),
        sg.In(font=("Helvetica", 13), key='video_folder', size=(41, 1)),
        sg.FolderBrowse(' 选择 '),
    ],
    [
        sg.Text('视频文件路径:  ', font=("Helvetica", 13)),
        sg.In(font=("Helvetica", 13), key='video_path', size=(46, 1)),
        sg.FileBrowse(' 选择 ')
    ],
    [
        sg.Text('音频文件所在文件夹: ', font=("Helvetica", 13)),
        sg.In(font=("Helvetica", 13), key='audio_folder', size=(41, 1)),
        sg.FolderBrowse(' 选择 ')
    ],
    # [sg.Output(size=(83, 10))],
    [
        sg.T(size=(19, 1)),
        sg.Button('    下载    ', font=("Helvetica", 11)),
        sg.T(size=(12, 1)),
        sg.Button('提取音频', font=("Helvetica", 11))
    ],
]


window = sg.Window('视频下载/音频提取器', layout, alpha_channel=0.95)

# ---===--- Loop taking in user input and using it to call scripts --- #

cwd = os.getcwd()
while True:
    (event, value) = window.read()
    if event == sg.WIN_CLOSED:
        break  # exit button clicked
    if event == '    下载    ':
        ret = download_video(value['URL'])
        if ret['status'] == 0:
            print("无法下载资源≧ ﹏ ≦")
        else:
            video_folder = cwd
            if value['video_folder']:
                if os.path.exists(value['video_folder']):
                    video_folder = value['video_folder']
                else:
                    print("文件夹不存在")
                    continue
            else:
                window['video_folder'].update(video_folder)
            video_path = os.path.join(video_folder, f"{ret['title']}.{ret['ext']}")
            move_file(os.path.join(cwd, ret['title']+f"-{ret['id']}.{ret['ext']}"), video_path)
            window['video_path'].update(video_path)
            print(f"下载{ret['title']}成功O(∩_∩)O")
    elif event == '提取音频':
        if value['video_path'] and value['audio_folder'] and os.path.exists(value['video_path']) and os.path.exists(value['audio_folder']):
            audio_path = os.path.join(value['audio_folder'], get_filename_from_filepath(value['video_path']))+".mp3"
            try:
                extract_audio_from_video(value['video_path'], audio_path)
                print(f"提取音频成功O(∩_∩)O")
                print(f"音频文件保存在{audio_path}")
            except Exception as e:
                print("提取音频失败≧ ﹏ ≦")
