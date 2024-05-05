import base64

from flask import Flask, request, jsonify
import os
import tempfile
from sheet_service import create_sheet, midi_to_sheet, logging_midi_to_sheet, read_file_as_string
app = Flask(__name__)
import asyncio

@app.route('/get_file', methods=['POST'])
def get_file():
    # 요청으로부터 바이너리 데이터와 파일 이름 받아오기
    binary_data = request.data
    file_name = request.headers.get('file-name')

    # 현재 디렉토리에 .mid 형식으로 파일을 저장
    save_path = os.path.join(os.getcwd(), file_name + '.mid')
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
    return jsonify({'files': sheet_files})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 디버그 모드로 실행, 외부 접속 허용
