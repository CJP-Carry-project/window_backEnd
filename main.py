import base64

from flask import Flask, request, jsonify
import os
import tempfile
from sheet_service import create_sheet, midi_to_sheet, logging_midi_to_sheet, read_file_as_string
app = Flask(__name__)
import asyncio
import os
import glob



def delete_result(audio_title, path):
    # 특정 디렉토리 경로 설정
    directory = path

    # 디렉토리 내의 모든 파일 수집
    all_files = glob.glob(os.path.join(directory, '*'))
    print(all_files)
    print(audio_title)
    # 조건문으로 특정 파일을 삭제
    for file_path in all_files:
        # 파일 이름에서 확장자를 제외한 부분을 추출
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # 파일 이름에 audio_title이 포함되어 있다면 삭제
        if audio_title in file_name:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
@app.route('/get_file', methods=['POST'])
def get_file():
    # 요청으로부터 바이너리 데이터와 파일 이름 받아오기qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
    binary_data = request.data
    file_name = request.headers.get('file-name')

    # 현재 디렉토리에 .mid 형식으로 파일을 저장
    save_path = os.path.join('./midi/', file_name + '.mid')
    with open(save_path, 'wb') as f:
        f.write(binary_data)

    create_sheet(save_path)

    print("끝났습니동")

    # 해당 파일 이름을 포함하는 악보 이미지 파일들을 읽어서 byte 배열로 리스트 만들기
    sheet_files = []
    for file in os.listdir('./sheets/'):
        if file_name in file:
            with open(os.path.join('./sheets/', file), 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')
                sheet_files.append({'name': file, 'content': content})

    delete_result(file_name, './midi/')
    delete_result(file_name, './sheets/')
    return jsonify({'files': sheet_files})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 디버그 모드로 실행, 외부 접속 허용
