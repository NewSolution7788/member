from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 회원 정보를 저장할 딕셔너리
members = {}

def save_members_to_json(members):
    try:
        with open('members.json', 'w', encoding='utf-8') as file:
            json.dump(members, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")

@app.route('/')
def index():
    return render_template('index.html', members=members)

@app.route('/add_member', methods=['POST'])
def add_member():
    member_id = request.form.get('id')
    name = request.form.get('name')
    dob = request.form.get('dob')
    carrier = request.form.get('carrier')
    phone = request.form.get('phone')
    bank_name = request.form.get('bank_name')
    account = request.form.get('account')
    note = request.form.get('note')
    image = request.files.get('image')
    
    if not member_id or not name or not dob or not carrier or not phone or not bank_name or not account:
        flash("모든 필드를 채워주세요.")
        return redirect(url_for('index'))
    
    if member_id in members:
        flash("이미 존재하는 회원 ID입니다.")
        return redirect(url_for('index'))

    # 이미지 파일 저장 로직 추가 (예: image.save("static/images/" + filename))
    
    members[member_id] = {
        'name': name,
        'dob': dob,
        'carrier': carrier,
        'phone': phone,
        'bank_name': bank_name,
        'account': account,
        'note': note,
        'image': image.filename if image else ''
    }
    save_members_to_json(members)
    return redirect(url_for('index'))

@app.route('/view_member', methods=['POST'])
def view_member():
    search_id = request.form.get('search_id')
    if search_id not in members:
        flash("존재하지 않는 회원 ID입니다.")
        return redirect(url_for('index'))

    member = members[search_id]
    flash(f"회원 정보: {member}")
    return redirect(url_for('index'))

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    excel_file = request.files.get('excel_file')
    if not excel_file:
        flash("엑셀 파일을 선택해주세요.")
        return redirect(url_for('index'))

    try:
        df = pd.read_excel(excel_file)
        for _, row in df.iterrows():
            member_id = row['아이디']
            if member_id in members:
                flash(f"이미 존재하는 회원 ID입니다: {member_id}")
                continue
            members[member_id] = {
                'name': row['이름'],
                'dob': row['생년월일'],
                'carrier': row['통신사'],
                'phone': row['휴대폰'],
                'bank_name': row['은행명'],
                'account': row['계좌번호'],
                'note': row['비고'],
                'image': ''
            }
        save_members_to_json(members)
        flash("엑셀 파일로부터 회원 정보를 일괄 등록하였습니다.")
    except Exception as e:
        flash(f"엑셀 파일을 읽는 중 오류가 발생하였습니다: {e}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
