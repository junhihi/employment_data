import pandas as pd
import json

def excel_to_json(excel_file_path, json_file_path):
    try:
        # Excel 파일 읽기
        df = pd.read_excel(excel_file_path)

        # 데이터프레임을 JSON으로 변환
        data = df.to_dict(orient='records')

        # JSON 파일로 저장
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print("Excel 파일이 성공적으로 JSON 파일로 변환되었습니다.")
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 경로를 확인하세요.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

# 변환할 Excel 파일 경로와 저장할 JSON 파일 경로
excel_file_path = '/Users/junhi/Desktop/company_data/dataset.xlsx'
json_file_path = '/Users/junhi/Desktop/result.json'

# Excel을 JSON으로 변환하여 저장
excel_to_json(excel_file_path, json_file_path)
