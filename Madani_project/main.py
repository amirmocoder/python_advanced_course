# امیرعلی محمدی (4011833239)
# پروژه مدیریت لیگ فوتبال
# درس برنامه سازی پیشرفته استاد ترحیب


# وارد کردن کتابخانه ها در پروژه

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import mysql.connector

# راه اندازی دیتابیس

mydb = mysql.connector.connect(
  host="localhost",
  port="3306", # پورت
  user="root",
  password="", # رمز عبور دیتابیس
  database="manage_league" # نام دیتابیس
) 

cursor = mydb.cursor()


# لیست هدرس حاوی عناوین ستون ها

headers = ('امتیاز', 'ت.گ', 'گ.خ', 'گ.ز', 'باخت', 'تساوی', 'برد', 'بازی', 'تیم', 'رتبه')

# بررسی و ایجاد جدول لیگ در دیتابیس

sel_query = "SHOW TABLES LIKE 'league1'"
cursor.execute(sel_query)
isthere = cursor.fetchone()
if not isthere:
    create_query ='''
        CREATE TABLE league1 (
            `امتیاز` INT,
            `ت.گ` INT,
            `گ.خ` INT,
            `گ.ز` INT,
            `باخت` INT,
            `تساوی` INT,
            `برد` INT,
            `بازی` INT,
            `تیم` VARCHAR(255),
            `رتبه` INT
        );
    '''

    cursor.execute(create_query)


# تعریف کردن لیست حاوی جدول و نام تیم ها

data = []
team = ['']

# دریافت جدول از دیتابیس و وارد کردن اطلاعات به برنامه

get_query = "SELECT * FROM league1"
cursor.execute(get_query)
for row in cursor:
    data.append(list(row))
    team.append(row[8])

# تعریف کردن رنگ پس زمینه و فونت های برنامه

Main_BG = "#eaece5"
Main_font1 = "MRT_Liner XXL"
Main_font2 = "MRT_Liner XL"

# تعریف کردن صفحه اصلی برنامه حاول جدول و دکمه ها

root = tk.Tk()
root.title("مدیریت لیـــگ فوتبال")
root.geometry('1000x650')
root.geometry("+100+10")
root.configure(bg=Main_BG)
root.resizable(False, False)

# دادن تم به صفحه و تعریف انواع استایل ها برای ویجت ها

style = ttk.Style()
style.theme_use("clam")
style.configure("CustomFrame1.TFrame", background=Main_BG)
style.configure("CustomButton1.TButton", width=40, font=(Main_font2, 12))
style.configure("CustomButton2.TButton", width=15, font=(Main_font2, 12))
style.configure("CustomoptMenu.TMenubutton", width = 15 ,font=(Main_font2, 12))

# ساختن فریم اول برای نمایش جدول لیگ

frame1 = ttk.Frame(root)
frame1.configure(style="CustomFrame1.TFrame")
frame1.pack(side=tk.LEFT, fill=tk.Y, padx=50)

# ساختن فریم دوم برای دکمه ها و تصویر برنامه

frame2 = ttk.Frame(root)
frame2.configure(style="CustomFrame1.TFrame")
frame2.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=20, pady=40)


# تعریف تابع جدول سازی طبق داده های لیست دیتا

def create_table(root,data,headers):
        global label_list
        label_list = []
        total_rows = len(data) + 1
        total_columns = len(headers)

        # هدر جدول

        top_header = 'جدول لیـــگ'
        label_header = tk.Label(root,fg='black', font=(Main_font1, 18, "underline"), justify='center', bg=Main_BG)
        label_header.grid(row=0, column=0, columnspan=total_columns, pady=10)
        label_header.config(text=top_header)
        
        # سطر اصلی حاوی عناوین موجود در لیست هدرس

        for j in range(total_columns):
            header = headers[j]
            if header == headers[-2]:
                e = Label(root, width=8, fg='black', font=(Main_font2, 15), justify='center', relief=tk.SOLID, borderwidth=1, bg="#ffcf40")
            else:
                e = Label(root, width=4, fg='black', font=(Main_font2, 15), justify='center', relief=tk.SOLID, borderwidth=1, bg="#ffcf40")
            e.grid(row=1, column=j)
            e.config(text=header)
        
        # فرایند تغییر رنگ سطر ها برای تیم اول و دو تیم آخر و سطر های یک در میان به ترتیب آبی ، قرمز ، خاکستری

        for i in range(len(data)):
            if i == 0:
                var_col = "#87CEFA"
            elif i == len(data) - 1 or i == len(data) - 2:
                var_col = "#EA4335"
            elif i % 2 == 0:
                var_col = "#D3D3D3"
            else:
                var_col = "white"

            # تعیین اندازه ستون ها

            for j in range(total_columns):
                if j == 8:
                    e = Label(root, width=8, fg='black', font=(Main_font2, 15), justify='center', relief=tk.SOLID, borderwidth=1, bg=var_col)
                else:
                    e = Label(root, width=4, fg='black', font=(Main_font2, 15), justify='center', relief=tk.SOLID, borderwidth=1, bg=var_col)
                e.grid(row=i + 2, column=j)
                label_list.append(e)
                e.config(text=data[i][j])


# ایجاد جدول اولیه

table = create_table(frame1,data=data,headers=headers)

# تعریف تابع ریست کردن جدول لیگ

def reset_table():
    for label in label_list:
        label.destroy()

# تعریف تابع مرتب کردن به ترتیب اولویت عناوین جدول لیگ

def sort_table():
    global data

    # به ترتیب بیشترین امتیاز، بیشترین تفاضل گل، بیشترین برد، کمترین باخت، حروف الفبا

    sorted_name = sorted(data, key=lambda x: (x[8]), reverse=False)
    sorted_lose = sorted(sorted_name, key=lambda x: (x[4]), reverse=False)
    sorted_win = sorted(sorted_lose, key=lambda x: (x[6]), reverse=True)
    sorted_gd = sorted(sorted_win, key=lambda x: (x[1]), reverse=True)
    sorted_pts = sorted(sorted_gd, key=lambda x: (x[0]), reverse=True)
    data = sorted_pts
    n = 0
    for d in data:
        n += 1
        d[9] = n

# تعریف تابع حذف دیتای موجود در کل برنامه

def drop_table():
    global team, data
    reset_table()
    team = ['']
    data = []

# تعریف تابع عملیات افزودن یا حذف تیم

def add_drop_team():

    # ساختن یک زیرصفحه برای عملیات افزودن یا حذف تیم

    tl = tk.Toplevel(root)
    tl.title("اضافه یا حذف تیم")
    tl.geometry('500x250')
    tl.geometry("+350+100")
    tl.configure(bg=Main_BG)
    tl.resizable(False, False)

    # ساختن فریم اول برای افزودن تیم
    
    tlframe1 = ttk.Frame(tl)
    tlframe1.configure(style="CustomFrame1.TFrame")
    tlframe1.pack(side=tk.LEFT, fill=tk.Y, padx=20)

    # ساختن فریم دوم برای حذف تیم

    tlframe2 = ttk.Frame(tl)
    tlframe2.configure(style="CustomFrame1.TFrame")
    tlframe2.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=20)


    header1 = tk.Label(tlframe2, text='افزودن تیـم', fg='black', font=(Main_font1, 16 ,'bold', "underline"), justify='center', bg=Main_BG)
    header1.pack(pady=20,padx=50)

    # تعریف تابع افزودن یک تیم به لیست تیم و جدول لیگ

    def save_team():
        global team, data
        team.append(entry.get())
        data.append([0, 0, 0, 0, 0, 0, 0, 0, entry.get(),0])
        entry.delete(0, tk.END)
        reset_table()
        sort_table()
        table = create_table(frame1,data=data,headers=headers)
        update_option_menu()


    entry = ttk.Entry(tlframe2,style="CustomEntry.TEntry",font=(Main_font2, 12),width=15,justify='center')
    entry.pack(pady=20)

    button1 = ttk.Button(tlframe2, text="ثبـــت", command=save_team, style="CustomButton2.TButton")
    button1.pack(pady=5)


    header2 = tk.Label(tlframe1, text='حذف تیـم', fg='black', font=(Main_font1, 16 ,'bold', "underline"), justify='center', bg=Main_BG)
    header2.pack(pady=20,padx=50)

    # تعریف تابع آپدیت کردن لیست تیم های موجود

    def update_option_menu():
        option_menu['menu'].delete(0, 'end')
        for option in team:
            option_menu['menu'].add_command(label=option, command=tk._setit(option_var, option))

    # تعریف تابع حذف تیم از لیست تیم ها و از جدول لیگ

    def drop_team():
        global team, data
        selected_team = option_var.get()
        if selected_team in team and selected_team != '':
            team.remove(selected_team)
        for d in data:
            if selected_team in d:
                data.remove(d)
        option_var.set("")
        reset_table()
        sort_table()
        table = create_table(frame1,data=data,headers=headers)
        update_option_menu()

    option_var = tk.StringVar()
    option_menu = ttk.OptionMenu(tlframe1, option_var, team[0], *team, style="CustomoptMenu.TMenubutton")
    option_menu.pack(pady=15)


    button2 = ttk.Button(tlframe1, text="حذف", command=drop_team, style="CustomButton2.TButton")
    button2.pack(pady=5)


# تعریف تابع ثبت نتایج مسابقات

def match():

    # ساختن یک زیرصفحه برای ثبت نتایج مسابقات

    global entry_a, entry_b
    tl = tk.Toplevel(root)
    tl.title("ثبت نتیجه یک تقابل")
    tl.geometry('500x450')
    tl.geometry("+350+100")
    tl.configure(bg=Main_BG)
    tl.resizable(False, False)

    # تعریف تابع گرفتن نام دو تیمی که با هم بازی کردند

    def on_team_selected(*args):
        global selected_team_b, selected_team_a
        selected_team_a = option_var1.get()
        selected_team_b = option_var2.get()

    # دریافت نتیجه مسابقه از کاربر

    header1 = tk.Label(tl, text='ثبت نتیجه مسابقه', fg='black', font=(Main_font1, 16 ,'bold', "underline"), justify='center', bg=Main_BG)
    header1.pack(pady=10,padx=50)

    header2 = tk.Label(tl, text='تیم میزبان', fg='black', font=(Main_font1, 12 ,'bold', "underline"), justify='center', bg=Main_BG)
    header2.pack(pady=1,padx=50)
    
    option_var1 = tk.StringVar()
    option_menu = ttk.OptionMenu(tl, option_var1, *team, style="CustomoptMenu.TMenubutton")
    option_menu.pack(pady=15)

    entry_a = ttk.Entry(tl, style="CustomEntry.TEntry",font=(Main_font2, 12),width=15,justify='center')
    entry_a.pack(pady=10)

    header3 = tk.Label(tl, text='تیم مهمان', fg='black', font=(Main_font1, 12 ,'bold', "underline"), justify='center', bg=Main_BG)
    header3.pack(pady=1,padx=50)

    option_var2 = tk.StringVar()
    option_menu = ttk.OptionMenu(tl, option_var2, *team, style="CustomoptMenu.TMenubutton", command=on_team_selected)
    option_menu.pack(pady=15)

    entry_b = ttk.Entry(tl, style="CustomEntry.TEntry",font=(Main_font2, 12),width=15,justify='center')
    entry_b.pack(pady=10)

    # تعریف تابع انجام محاسبات جدول

    def calculate():
        global team, data

        # ذخیره سازی نتیجه یک تقابل در یک تاپل

        res = (selected_team_a,a,selected_team_b,b)

        # ثبت تعداد بازی های انجام شده هر تیم در جدول

        for d in data:
            if res[0] in d or res[2] in d:
                d[7] += 1

        # ثبت برد، باخت یا تساوی هر تیم در جدول

        if a > b:
            for d in data:
                if res[0] in d:
                    d[6] += 1 # برد
                if res[2] in d:
                    d[4] += 1 # باخت
        if a == b:
            for d in data:
                if res[0] in d or res[2] in d:
                    d[5] += 1 # تساوی
        if b > a:
            for d in data:
                if res[2] in d:
                    d[6] += 1 # برد
                if res[0] in d:
                    d[4] += 1 # باخت

        # ثبت گل زده و گل خورده هر تیم در جدول

        for d in data:
            if res[0] in d:
                d[3] += a # گل زده
                d[2] += b # گل خورده
            if res[2] in d:
                d[3] += b # گل زده
                d[2] += a # گل خورده

        # محاسبه و ثبت تفاضل گل (گل خورده - گل زده) هر تیم در جدول

        for d in data:
            if res[0] in d or res[2] in d:
                d[1] = d[3] - d[2]
        for d in data:
            if res[0] in d or res[2] in d:
                d[1] = d[3] - d[2]
        
        # محاسبه و ثبت امتیاز هر تیم در جدول (برد در سه بعلاوه تساوی)
        
        for d in data:
            if res[0] in d or res[2] in d:
                d[0] = (3*d[6]) + (d[5])


        reset_table()
        sort_table()
        table = create_table(frame1,data=data,headers=headers)
        option_var1.set("")
        option_var2.set("")
        entry_a.delete(0, tk.END)
        entry_b.delete(0, tk.END)

    # تعریف تابع بررسی ورودی و ثبت تغییرات جدول

    def res_match():
        global a,b

        # بررسی اینکه ورودی یک عدد است

        try:
            a = int(entry_a.get())
            b = int(entry_b.get())
        except:
            messagebox.showinfo(title= "مشکل در ثبت تقابل", message= "!نتیجه وارد شده باید یک عدد صحیح مثبت باشد", parent = tl)
        else:

            # بررسی اینکه ورودی مثبت است

            if (a < 0) or (b < 0):
                messagebox.showinfo(title= "مشکل در ثبت تقابل", message= "!نتیجه وارد شده باید یک عدد صحیح مثبت باشد", parent = tl)
            else:

                # بررسی اینکه تیم اول و تیم دوم یکی نباشد

                if selected_team_a == selected_team_b:
                    messagebox.showinfo(title= "مشکل در ثبت تقابل", message= "!یک تیم نمی تواند با خودش بازی داشته باشد", parent = tl)
                else:
                    calculate()


    button = ttk.Button(tl, text="ثبت نتیجه", style="CustomButton2.TButton",command=res_match)
    button.pack(pady=5)


# تعریف تابع ذخیره جدول لیگ در دیتابیس

def save_league():
    send_query_reset = "DELETE FROM league1"
    cursor.execute(send_query_reset)
    for d in data:
        send_query_update = f"INSERT INTO league1 VALUES {tuple(d)}"
        cursor.execute(send_query_update)
    mydb.commit()

# تعریف تابع نمایش آمار تهاجمی لیگ

def attack_rep():
    best_attack = []
    worse_attack = []
    score_sort = sorted(data, key=lambda x: (x[3]), reverse=True)
    best_attack.append(score_sort[0][3])
    best_attack.append(score_sort[0][8])
    worse_attack.append(score_sort[-1][3])
    worse_attack.append(score_sort[-1][8])

    messagebox.showinfo(title= "آمار تهاجمی لیگ",message=f"According to the games played so far; team {best_attack[1]} with scoring {best_attack[0]} goals has the best offensive line and team {worse_attack[1]} with scoring {worse_attack[0]} goals has the worst offensive line among others teams are.", parent = root)

# تعریف تابع نمایش آمار دفاعی لیگ

def defence_rep():
    best_defence = []
    worse_defence = []
    score_sort = sorted(data, key=lambda x: (x[2]), reverse=False)
    best_defence.append(score_sort[0][2])
    best_defence.append(score_sort[0][8])
    worse_defence.append(score_sort[-1][2])
    worse_defence.append(score_sort[-1][8])

    messagebox.showinfo(title= "آمار دفاعی لیگ",message=f"According to the games that have been played so far; team {best_defence[1]} has the best defense line by receiving {best_defence[0]} goals and team {worse_defence[1]} has the worst defense line among other teams by receiving {worse_defence[0]} goals.", parent = root)

# تعریف دکمه های انجام عملیات ها

btn_header = tk.Label(frame2, text='انجـام عملیــات', fg='black', font=(Main_font1, 16 ,'bold', "underline"), justify='center', bg=Main_BG)
btn_header.pack(pady=5)

button1 = ttk.Button(frame2, text='اضافه یا حذف کردن تیم', style="CustomButton1.TButton", command=add_drop_team)
button1.pack(pady=10)

button2 = ttk.Button(frame2, text='ثبت نتیجه یک تقابل', style="CustomButton1.TButton", command=match)
button2.pack(pady=10)

button3 = ttk.Button(frame2, text='پاک سازی داده ها', style="CustomButton1.TButton", command= drop_table)
button3.pack(pady=10)

# فاصله

space = tk.Label(frame2, text="", pady=5, bg=Main_BG)
space.pack()

btn_header2 = tk.Label(frame2, text='آمـار و ذخیره سازی', fg='black', font=(Main_font1, 16 ,'bold', "underline"), justify='center', bg=Main_BG)
btn_header2.pack(pady=5)

button4 = ttk.Button(frame2, text='ذخیرسازی در دیتابیس', style="CustomButton1.TButton", command=save_league)
button4.pack(pady=10)

button5 = ttk.Button(frame2, text='آمار تهاجمی لیگ', style="CustomButton1.TButton", command=attack_rep)
button5.pack(pady=10)

button6 = ttk.Button(frame2, text='آمار دفاعی لیگ', style="CustomButton1.TButton", command=defence_rep)
button6.pack(pady=10)

# فاصله

space = tk.Label(frame2, text="", pady=10, bg=Main_BG)
space.pack()

# نگه داشتن صفحه اصلی برنامه

root.mainloop()


# امیرعلی محمدی (4011833239)
# پروژه مدیریت لیگ فوتبال
# درس برنامه سازی پیشرفته استاد ترحیب