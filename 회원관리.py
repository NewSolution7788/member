import json
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# 회원 정보를 저장할 파일 경로
FILE_PATH = 'members.json'

# 회원 정보 로드
def load_members():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# 회원 정보 저장
def save_members(members):
    with open(FILE_PATH, 'w') as file:
        json.dump(members, file, indent=4)

# 이미지 선택 및 표시
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if not file_path:
        return
    img = Image.open(file_path)
    img = img.resize((100, 100))
    img = ImageTk.PhotoImage(img)
    label_image.config(image=img)
    label_image.image = img
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, file_path)

# 회원 등록
def add_member(members, tree):
    member_id = entry_id.get().strip()
    name = entry_name.get().strip()
    dob = entry_dob.get().strip()
    carrier = entry_carrier.get().strip()
    phone = entry_phone.get().strip()
    bank_name = entry_bank_name.get().strip()
    account = entry_account.get().strip()
    note = entry_note.get().strip()
    image_path = entry_image_path.get().strip()

    if not member_id or not name or not dob or not carrier or not phone or not bank_name or not account:
        messagebox.showwarning("경고", "모든 필드를 채워주세요.")
        return

    if member_id in members:
        messagebox.showerror("오류", "이미 존재하는 회원 ID입니다.")
        return

    members[member_id] = {
        'name': name,
        'dob': dob,
        'carrier': carrier,
        'phone': phone,
        'bank_name': bank_name,
        'account': account,
        'note': note,
        'image': image_path
    }
    save_members(members)
    tree.insert("", "end", iid=member_id, values=(member_id, name, dob, carrier, phone, bank_name, account, note))
    clear_entries()

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_carrier.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_bank_name.delete(0, tk.END)
    entry_account.delete(0, tk.END)
    entry_note.delete(0, tk.END)
    entry_image_path.delete(0, tk.END)
    label_image.config(image='')

def load_members_to_tree(tree):
    members = load_members()
    for member_id, info in members.items():
        tree.insert("", "end", iid=member_id, values=(member_id, info['name'], info['dob'], info['carrier'], info['phone'], info['bank_name'], info['account'], info['note']))
    return members

def import_members_from_excel(members, tree):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            member_id = row['아이디']
            if member_id in members:
                messagebox.showerror("오류", f"이미 존재하는 회원 ID입니다: {member_id}")
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
            tree.insert("", "end", iid=member_id, values=(member_id, row['이름'], row['생년월일'], row['통신사'], row['휴대폰'], row['은행명'], row['계좌번호'], row['비고']))
        save_members(members)
        messagebox.showinfo("성공", "엑셀 파일로부터 회원 정보를 일괄 등록하였습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"엑셀 파일을 읽는 중 오류가 발생하였습니다: {e}")

def view_member(members):
    member_id = entry_search_id.get().strip()
    if member_id not in members:
        messagebox.showerror("오류", "존재하지 않는 회원 ID입니다.")
        return

    member = members[member_id]
    messagebox.showinfo("회원 정보", f"ID: {member_id}\n이름: {member['name']}\n생년월일: {member['dob']}\n통신사: {member['carrier']}\n휴대폰: {member['phone']}\n은행명: {member['bank_name']}\n계좌번호: {member['account']}\n비고: {member['note']}")

    image_path = member.get('image')
    if image_path:
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        label_image.config(image=img)
        label_image.image = img
    else:
        label_image.config(image='')

# 메인 프로그램
root = tk.Tk()
root.title("회원관리 프로그램")

# 프레임 설정
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 라벨 및 엔트리
ttk.Label(frame, text="회원 ID").grid(row=0, column=0, sticky=tk.W)
entry_id = ttk.Entry(frame, width=20)
entry_id.grid(row=0, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="이름").grid(row=1, column=0, sticky=tk.W)
entry_name = ttk.Entry(frame, width=20)
entry_name.grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="생년월일").grid(row=2, column=0, sticky=tk.W)
entry_dob = ttk.Entry(frame, width=20)
entry_dob.grid(row=2, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="통신사").grid(row=3, column=0, sticky=tk.W)
entry_carrier = ttk.Entry(frame, width=20)
entry_carrier.grid(row=3, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="휴대폰").grid(row=4, column=0, sticky=tk.W)
entry_phone = ttk.Entry(frame, width=20)
entry_phone.grid(row=4, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="은행명").grid(row=5, column=0, sticky=tk.W)
entry_bank_name = ttk.Entry(frame, width=20)
entry_bank_name.grid(row=5, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="계좌번호").grid(row=6, column=0, sticky=tk.W)
entry_account = ttk.Entry(frame, width=20)
entry_account.grid(row=6, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="비고").grid(row=7, column=0, sticky=tk.W)
entry_note = ttk.Entry(frame, width=20)
entry_note.grid(row=7, column=1, sticky=(tk.W, tk.E))

# 이미지 추가
ttk.Label(frame, text="이미지").grid(row=8, column=0, sticky=tk.W)
ttk.Button(frame, text="이미지 선택", command=select_image).grid(row=8, column=1, sticky=tk.W)
entry_image_path = ttk.Entry(frame, width=20)
entry_image_path.grid(row=8, column=2, sticky=(tk.W, tk.E))
label_image = ttk.Label(frame)
label_image.grid(row=8, column=3, sticky=(tk.W, tk.E))

# 버튼
ttk.Button(frame, text="회원 등록", command=lambda: add_member(members, tree)).grid(row=9, column=0, sticky=tk.W)
ttk.Button(frame, text="엑셀 파일로 회원 일괄 등록", command=lambda: import_members_from_excel(members, tree)).grid(row=9, column=1, sticky=tk.W)

# 트리뷰 설정
columns = ("아이디", "이름", "생년월일", "통신사", "휴대폰", "은행명", "계좌번호", "비고")
tree = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)

tree.grid(row=10, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

# 스크롤바 설정
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=10, column=4, sticky=(tk.N, tk.S))

# 회원 조회
ttk.Label(frame, text="조회할 회원 ID").grid(row=11, column=0, sticky=tk.W)
entry_search_id = ttk.Entry(frame, width=20)
entry_search_id.grid(row=11, column=1, sticky=(tk.W, tk.E))
ttk.Button(frame, text="회원 조회", command=lambda: view_member(members)).grid(row=11, column=2, sticky=tk.W)

# 윈도우 크기 조정 가능하게 설정
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.rowconfigure(10, weight=1)  # 트리뷰가 있는 행의 가중치 설정

# 회원 정보 로드 및 트리뷰 업데이트
members = load_members_to_tree(tree)

root.columnconfigure(0, weight=1)  # 전체 창의 가로 크기 조절 가능
root.rowconfigure(0, weight=1)     # 전체 창의 세로 크기 조절 가능

root.mainloop()
