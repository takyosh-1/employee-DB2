from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

employees_data = [
    {
        "id": 1,
        "name": "佐藤 花子",
        "furigana": "サトウ ハナコ",
        "birth_date": "1985/03/15",
        "employee_id": "JP0000001",
        "department": "人事部",
        "employment_type": "正社員",
        "prefecture": "東京都",
        "city": "渋谷区",
        "address": "神南1-1-1 渋谷ビル301",
        "retirement_date": "2025/12/31",
        "last_work_date": "2025/12/15"
    },
    {
        "id": 2,
        "name": "田中 次郎",
        "furigana": "タナカ ジロウ",
        "birth_date": "1978/07/22",
        "employee_id": "JP0000002",
        "department": "経理部",
        "employment_type": "正社員",
        "prefecture": "神奈川県",
        "city": "横浜市",
        "address": "西区みなとみらい2-3-4 ランドマークタワー1205",
        "retirement_date": "2025/11/30",
        "last_work_date": "2025/11/20"
    },
    {
        "id": 3,
        "name": "山田 太郎",
        "furigana": "ヤマダ タロウ",
        "birth_date": "1980/10/10",
        "employee_id": "JP0000000",
        "department": "第一営業部",
        "employment_type": "正社員",
        "prefecture": "東京都",
        "city": "中央区",
        "address": "八重洲2-2-3　ドミトリートーキョー５０５",
        "retirement_date": "2025/10/30",
        "last_work_date": "2025/10/01"
    },
    {
        "id": 4,
        "name": "鈴木 美咲",
        "furigana": "スズキ ミサキ",
        "birth_date": "1990/12/05",
        "employee_id": "JP0000003",
        "department": "マーケティング部",
        "employment_type": "契約社員",
        "prefecture": "大阪府",
        "city": "大阪市",
        "address": "北区梅田1-2-3 梅田スカイビル4F",
        "retirement_date": "2025/09/30",
        "last_work_date": "2025/09/25"
    },
    {
        "id": 5,
        "name": "高橋 健一",
        "furigana": "タカハシ ケンイチ",
        "birth_date": "1982/04/18",
        "employee_id": "JP0000004",
        "department": "IT部",
        "employment_type": "正社員",
        "prefecture": "愛知県",
        "city": "名古屋市",
        "address": "中区栄3-4-5 名古屋センタービル8F",
        "retirement_date": "2026/01/31",
        "last_work_date": "2026/01/20"
    },
    {
        "id": 6,
        "name": "伊藤 由美",
        "furigana": "イトウ ユミ",
        "birth_date": "1987/09/12",
        "employee_id": "JP0000005",
        "department": "総務部",
        "employment_type": "正社員",
        "prefecture": "福岡県",
        "city": "福岡市",
        "address": "博多区博多駅前2-1-1 博多駅前ビル12F",
        "retirement_date": "2025/08/31",
        "last_work_date": "2025/08/25"
    },
    {
        "id": 7,
        "name": "渡辺 雄介",
        "furigana": "ワタナベ ユウスケ",
        "birth_date": "1975/11/30",
        "employee_id": "JP0000006",
        "department": "製造部",
        "employment_type": "正社員",
        "prefecture": "静岡県",
        "city": "浜松市",
        "address": "中区板屋町1-2-3 浜松工業ビル5F",
        "retirement_date": "2025/07/31",
        "last_work_date": "2025/07/20"
    },
    {
        "id": 8,
        "name": "中村 恵子",
        "furigana": "ナカムラ ケイコ",
        "birth_date": "1983/06/08",
        "employee_id": "JP0000007",
        "department": "法務部",
        "employment_type": "契約社員",
        "prefecture": "京都府",
        "city": "京都市",
        "address": "下京区烏丸通四条下ル 京都タワービル9F",
        "retirement_date": "2025/12/15",
        "last_work_date": "2025/12/10"
    },
    {
        "id": 9,
        "name": "小林 直樹",
        "furigana": "コバヤシ ナオキ",
        "birth_date": "1979/02/14",
        "employee_id": "JP0000008",
        "department": "第二営業部",
        "employment_type": "正社員",
        "prefecture": "北海道",
        "city": "札幌市",
        "address": "中央区大通西3-4-5 札幌センタービル7F",
        "retirement_date": "2025/06/30",
        "last_work_date": "2025/06/25"
    },
    {
        "id": 10,
        "name": "加藤 麻衣",
        "furigana": "カトウ マイ",
        "birth_date": "1992/01/25",
        "employee_id": "JP0000009",
        "department": "企画部",
        "employment_type": "正社員",
        "prefecture": "宮城県",
        "city": "仙台市",
        "address": "青葉区中央1-2-3 仙台パルコ10F",
        "retirement_date": "2025/11/15",
        "last_work_date": "2025/11/10"
    }
]

@app.route('/')
def index():
    return render_template('index.html', employees=employees_data)

@app.route('/api/employee/<int:employee_id>')
def get_employee(employee_id):
    employee = next((emp for emp in employees_data if emp['id'] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({'error': 'Employee not found'}), 404

@app.route('/api/employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = next((emp for emp in employees_data if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    data = request.json
    employee.update(data)
    return jsonify(employee)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
