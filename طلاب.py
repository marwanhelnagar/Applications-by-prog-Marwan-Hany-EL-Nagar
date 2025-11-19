import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
import os

# ======================================================================
# القسم 1: الإعدادات والثوابت
# ======================================================================

# اسم الملف لحفظ البيانات
DATA_FILE = 'students_data.json'

# خيارات طرق الدفع المطلوبة (عربي/إنجليزي)
PAYMENT_METHODS = {
    "كاش (Cash)": "Cash",
    "انستا باي (InstaPay)": "InstaPay",
    "فودافون كاش (Vodafone Cash)": "Vodafone Cash",
    "e& money (e& money)": "EandMoney",
    "اورنج كاش (Orange Cash)": "Orange Cash",
    "وي باي (We Pay)": "We Pay"
}

# بيانات الطالب الافتراضية للمثال (مطابقة للصورة المرفقة)
INITIAL_STUDENTS = [
    {
        "id": 1,
        "name": "أحمد محمد محمود",
        "phone": "01011112222",
        "level": "الصف الأول الثانوي",
        "section": "مجموعة الأحد",
        "lastPaymentDate": "2025-01-01",
        "paidAmount": 400.0,
        "paymentMethod": "كاش (Cash)",
        "regDate": "2024-09-01",
        "birthYear": 2007,
        "birthMonth": 5,
        "birthDay": 15
    },
    {
        "id": 2,
        "name": "مروة علي حسن",
        "phone": "01233334444",
        "level": "الصف الثالث الإعدادي",
        "section": "مجموعة الخميس",
        "lastPaymentDate": "2024-11-01", # تاريخ متأخر لغرض التجربة
        "paidAmount": 350.0,
        "paymentMethod": "فودافون كاش (Vodafone Cash)",
        "regDate": "2024-10-10",
        "birthYear": 2009,
        "birthMonth": 1,
        "birthDay": 20
    }
]

# ======================================================================
# القسم 2: دالة إدارة البيانات (الحفظ والتحميل)
# ======================================================================

def load_data():
    """تحميل بيانات الطلاب والمجموعات من الملف، أو استخدام البيانات الافتراضية."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('students', []), data.get('sections', ['غير محدد']), data.get('next_id', 3)
        except Exception as e:
            print(f"Error loading data: {e}")
            messagebox.showerror("خطأ في التحميل", "حدث خطأ أثناء تحميل البيانات المحفوظة.")
    
    # تحميل البيانات الافتراضية إذا لم يتم العثور على ملف أو حدث خطأ
    return INITIAL_STUDENTS, ['غير محدد', 'مجموعة الأحد', 'مجموعة الخميس'], 3

def save_data(students, sections, next_id):
    """حفظ بيانات الطلاب والمجموعات في ملف JSON."""
    data = {
        'students': students,
        'sections': sections,
        'next_id': next_id,
        'save_time': datetime.now().isoformat()
    }
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")
        messagebox.showerror("خطأ في الحفظ", "حدث خطأ أثناء حفظ البيانات.")

# ======================================================================
# القسم 3: الكلاس الرئيسي للتطبيق
# ======================================================================

class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("نظام إدارة الطلاب الشامل - Python GUI")
        master.geometry("1000x700")
        master.resizable(True, True)

        # ضبط اتجاه الكتابة من اليمين لليسار
        master.option_add('*tearOff', tk.FALSE)

        # تحميل البيانات
        self.students, self.sections, self.next_id = load_data()
        self.current_student_id = None # لتحديد وضع التعديل

        # إنشاء واجهة التبويبات
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # إنشاء التبويبات
        self.create_dashboard_tab()
        self.create_registration_tab()
        self.create_list_tab()
        self.create_sections_tab()

        # تحديث الواجهة عند البدء
        self.update_all_views()

    # ------------------------------------------------------------------
    # 3.1 إنشاء لوحة القيادة (Dashboard)
    # ------------------------------------------------------------------
    def create_dashboard_tab(self):
        self.dashboard_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.dashboard_frame, text="📊 لوحة القيادة")

        tk.Label(self.dashboard_frame, text="ملخص الأداء والمتابعة", font=("Arial", 16, "bold"), fg="#3498db").pack(pady=10)
        
        # إطار لبطاقات الملخص
        self.summary_frame = tk.Frame(self.dashboard_frame)
        self.summary_frame.pack(fill='x', pady=10)

        self.summary_labels = {}
        cards_data = [
            ("إجمالي الطلاب", "total", "#2ecc71"),
            ("طلاب متأخرون", "late", "#e74c3c"),
            ("مستحق الدفع قريباً", "due_soon", "#f1c40f"),
            ("إجمالي الرسوم (تقديري)", "fees", "#3498db")
        ]
        
        for i, (title, key, color) in enumerate(cards_data):
            card = tk.Frame(self.summary_frame, bg=color, bd=5, relief=tk.RIDGE)
            card.pack(side=tk.LEFT, expand=True, fill='x', padx=5)
            
            tk.Label(card, text=title, bg=color, fg="white", font=("Arial", 12, "bold")).pack(pady=5)
            label = tk.Label(card, text="0", bg=color, fg="white", font=("Arial", 20, "bold"))
            label.pack(pady=5)
            self.summary_labels[key] = label
        
        # جدول المتابعة
        tk.Label(self.dashboard_frame, text="جدول متابعة الأقساط القادمة والمتأخرة", font=("Arial", 14, "bold"), fg="#3498db").pack(pady=10)
        
        self.follow_up_tree = ttk.Treeview(self.dashboard_frame, columns=("name", "section", "phone", "dueDate", "status"), show="headings")
        self.follow_up_tree.heading("name", text="الاسم")
        self.follow_up_tree.heading("section", text="المجموعة")
        self.follow_up_tree.heading("phone", text="هاتف ولي الأمر")
        self.follow_up_tree.heading("dueDate", text="آخر دفع/استحقاق")
        self.follow_up_tree.heading("status", text="الحالة")
        
        # عرض أزرار التعديل والحذف مباشرة من الجدول
        self.follow_up_tree.column("name", width=150, anchor=tk.E)
        self.follow_up_tree.column("section", width=100, anchor=tk.E)
        self.follow_up_tree.column("phone", width=100, anchor=tk.E)
        self.follow_up_tree.column("dueDate", width=100, anchor=tk.E)
        self.follow_up_tree.column("status", width=120, anchor=tk.E)

        self.follow_up_tree.pack(fill='both', expand=True)

    # ------------------------------------------------------------------
    # 3.2 إنشاء تبويب التسجيل/التعديل (Registration)
    # ------------------------------------------------------------------
    def create_registration_tab(self):
        self.reg_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.reg_frame, text="➕ تسجيل / تعديل طالب")
        
        self.form_title = tk.Label(self.reg_frame, text="تسجيل طالب جديد", font=("Arial", 16, "bold"), fg="#3498db")
        self.form_title.pack(pady=10)

        # استخدام إطار للنموذج لتنظيم العناصر في شبكة
        form_container = ttk.Frame(self.reg_frame)
        form_container.pack(fill='x', pady=10)

        # تعريف حقول الإدخال
        self.entry_fields = {}
        fields = [
            ("الاسم الثلاثي للطالب (إلزامي):", "name", 'entry'),
            ("رقم هاتف ولي الأمر:", "phone", 'entry'),
            ("المستوى الدراسي:", "level", 'entry'),
            ("القسم / المجموعة:", "section", 'combo'),
            ("تاريخ استحقاق الدفعة القادمة:", "lastPaymentDate", 'entry'),
            ("المبلغ المدفوع (بالأرقام):", "paidAmount", 'entry'),
            ("طريقة الدفع:", "paymentMethod", 'combo'),
            ("تاريخ التسجيل الأول (YYYY-MM-DD):", "regDate", 'entry'),
        ]
        
        # حقول تاريخ الميلاد بثلاث خانات
        birth_frame = ttk.Frame(form_container)
        birth_frame.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        
        tk.Label(birth_frame, text="تاريخ الميلاد (سنة/شهر/يوم):").pack(side=tk.RIGHT, padx=5)
        
        self.entry_fields["birthDay"] = tk.Entry(birth_frame, width=4)
        self.entry_fields["birthDay"].pack(side=tk.LEFT, padx=2, fill='x', expand=True)
        tk.Label(birth_frame, text="اليوم").pack(side=tk.LEFT)
        
        self.entry_fields["birthMonth"] = tk.Entry(birth_frame, width=4)
        self.entry_fields["birthMonth"].pack(side=tk.LEFT, padx=2, fill='x', expand=True)
        tk.Label(birth_frame, text="الشهر").pack(side=tk.LEFT)
        
        self.entry_fields["birthYear"] = tk.Entry(birth_frame, width=6)
        self.entry_fields["birthYear"].pack(side=tk.LEFT, padx=2, fill='x', expand=True)
        tk.Label(birth_frame, text="السنة").pack(side=tk.LEFT)
        

        row_num = 0
        for label_text, key, field_type in fields:
            # تخطي حقول التاريخ التي سيتم إضافتها لاحقاً
            if key == "birthYear":
                continue 

            tk.Label(form_container, text=label_text, anchor='e', width=30).grid(row=row_num, column=1, sticky='w', padx=5, pady=5)
            
            if field_type == 'entry':
                entry = tk.Entry(form_container, width=50)
                entry.grid(row=row_num, column=0, sticky='e', padx=5, pady=5)
                self.entry_fields[key] = entry
            elif field_type == 'combo':
                combo = ttk.Combobox(form_container, width=47, state="readonly")
                combo.grid(row=row_num, column=0, sticky='e', padx=5, pady=5)
                self.entry_fields[key] = combo
                if key == 'section':
                    combo['values'] = self.sections
                    combo.set(self.sections[0])
                elif key == 'paymentMethod':
                    combo['values'] = list(PAYMENT_METHODS.keys())
                    combo.set(list(PAYMENT_METHODS.keys())[0])

            row_num += 1

        # إضافة حقول التاريخ في الشبكة بشكل يدوي
        birth_frame.grid(row=row_num, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # أزرار الإجراءات
        self.save_btn = tk.Button(self.reg_frame, text="➕ تسجيل الطالب", command=self.save_or_update_student, bg="#2ecc71", fg="white", font=("Arial", 12, "bold"))
        self.save_btn.pack(pady=10, padx=5, side=tk.LEFT)
        
        tk.Button(self.reg_frame, text="مسح النموذج", command=self.reset_form, bg="#e74c3c", fg="white", font=("Arial", 12)).pack(pady=10, padx=5, side=tk.LEFT)

    # ------------------------------------------------------------------
    # 3.3 إنشاء تبويب قائمة الطلاب (List)
    # ------------------------------------------------------------------
    def create_list_tab(self):
        self.list_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.list_frame, text="📋 قائمة الطلاب والمتابعة")

        # شريط البحث
        search_frame = ttk.Frame(self.list_frame)
        search_frame.pack(fill='x', pady=10)
        
        tk.Label(search_frame, text="🔍 بحث:", font=("Arial", 12)).pack(side=tk.RIGHT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.RIGHT, padx=5, fill='x', expand=True)
        self.search_entry.bind('<KeyRelease>', self.render_list)

        tk.Button(search_frame, text="✉️ رسالة متابعة للمتأخرين", command=self.generate_late_payment_message, bg="#f1c40f", fg="black").pack(side=tk.LEFT, padx=5)
        
        # الجدول الرئيسي
        self.list_tree = ttk.Treeview(self.list_frame, columns=("id", "name", "phone", "section", "dueDate", "paidAmount", "status", "actions"), show="headings")
        self.list_tree.heading("id", text="ID")
        self.list_tree.heading("name", text="الاسم")
        self.list_tree.heading("phone", text="هاتف ولي الأمر")
        self.list_tree.heading("section", text="المجموعة")
        self.list_tree.heading("dueDate", text="آخر دفع/استحقاق")
        self.list_tree.heading("paidAmount", text="المبلغ المدفوع")
        self.list_tree.heading("status", text="حالة الدفع")
        self.list_tree.heading("actions", text="الإجراءات")

        self.list_tree.column("id", width=30, stretch=tk.NO, anchor=tk.CENTER)
        self.list_tree.column("name", width=150, anchor=tk.E)
        self.list_tree.column("phone", width=100, anchor=tk.E)
        self.list_tree.column("section", width=100, anchor=tk.E)
        self.list_tree.column("dueDate", width=100, anchor=tk.E)
        self.list_tree.column("paidAmount", width=80, anchor=tk.E)
        self.list_tree.column("status", width=120, anchor=tk.E)
        self.list_tree.column("actions", width=120, stretch=tk.NO, anchor=tk.CENTER)
        
        self.list_tree.pack(fill='both', expand=True)

        # ربط حدث النقر المزدوج لفتح نموذج التعديل
        self.list_tree.bind('<Double-1>', self.on_double_click)
        self.list_tree.bind('<ButtonRelease-1>', self.on_action_click) # لربط أزرار الإجراءات في عمود الإجراءات

    # ------------------------------------------------------------------
    # 3.4 إنشاء تبويب إدارة الأقسام (Sections)
    # ------------------------------------------------------------------
    def create_sections_tab(self):
        self.sections_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.sections_frame, text="📂 إدارة الأقسام")

        tk.Label(self.sections_frame, text="إضافة قسم جديد:", font=("Arial", 14, "bold"), fg="#3498db").pack(pady=10)
        
        input_frame = ttk.Frame(self.sections_frame)
        input_frame.pack(pady=5, fill='x')
        
        self.new_section_entry = tk.Entry(input_frame, width=50)
        self.new_section_entry.pack(side=tk.RIGHT, padx=5, fill='x', expand=True)
        tk.Button(input_frame, text="➕ إضافة قسم", command=self.add_section, bg="#2ecc71", fg="white").pack(side=tk.RIGHT, padx=5)

        tk.Label(self.sections_frame, text="قائمة الأقسام الموجودة:", font=("Arial", 14, "bold"), fg="#3498db").pack(pady=10)
        self.sections_listbox = tk.Listbox(self.sections_frame, height=10)
        self.sections_listbox.pack(fill='x', padx=5, expand=False)
        
        tk.Button(self.sections_frame, text="🗑️ حذف القسم المحدد", command=self.delete_section, bg="#e74c3c", fg="white").pack(pady=10)


    # ------------------------------------------------------------------
    # 3.5 تحديثات الواجهة الشاملة
    # ------------------------------------------------------------------
    def update_all_views(self):
        """تحديث جميع عناصر الواجهة."""
        self.calculate_and_render_dashboard()
        self.render_list()
        self.render_section_list()
        self.update_section_combobox()

    def update_section_combobox(self):
        """تحديث قائمة الأقسام المنسدلة في نموذج التسجيل."""
        section_combo = self.entry_fields.get("section")
        if section_combo:
            section_combo['values'] = self.sections
            if not section_combo.get() or section_combo.get() not in self.sections:
                section_combo.set(self.sections[0])

    # ------------------------------------------------------------------
    # 3.6 دوال إدارة النماذج
    # ------------------------------------------------------------------
    def reset_form(self):
        """إعادة ضبط النموذج لوضع التسجيل الجديد."""
        self.current_student_id = None
        self.form_title.config(text="تسجيل طالب جديد")
        self.save_btn.config(text="➕ تسجيل الطالب")
        
        for key, entry in self.entry_fields.items():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                if key == 'section':
                    entry.set(self.sections[0])
                elif key == 'paymentMethod':
                    entry.set(list(PAYMENT_METHODS.keys())[0])

        # ضبط التواريخ الافتراضية
        today = datetime.now().strftime("%Y-%m-%d")
        self.entry_fields["lastPaymentDate"].insert(0, today)
        self.entry_fields["regDate"].insert(0, today)
        self.entry_fields["paidAmount"].insert(0, 0)
        
        # توجيه المستخدم لتبويب التسجيل
        self.notebook.select(1)
        
    def load_student_to_form(self, student_id):
        """تحميل بيانات طالب معين إلى النموذج للتعديل."""
        student = next((s for s in self.students if s["id"] == student_id), None)
        if not student:
            messagebox.showerror("خطأ", "لم يتم العثور على الطالب.")
            return

        self.reset_form() # مسح النموذج أولاً
        self.current_student_id = student_id
        self.form_title.config(text=f"تعديل بيانات الطالب: {student['name']}")
        self.save_btn.config(text="💾 حفظ التعديلات")
        
        for key, entry in self.entry_fields.items():
            if key in student:
                value = student[key]
                if isinstance(entry, tk.Entry):
                    entry.insert(0, str(value))
                elif isinstance(entry, ttk.Combobox):
                    entry.set(value)

        # إعادة ضبط حقول الميلاد المنفصلة
        self.entry_fields["birthYear"].delete(0, tk.END)
        self.entry_fields["birthMonth"].delete(0, tk.END)
        self.entry_fields["birthDay"].delete(0, tk.END)

        self.entry_fields["birthYear"].insert(0, student.get("birthYear", ""))
        self.entry_fields["birthMonth"].insert(0, student.get("birthMonth", ""))
        self.entry_fields["birthDay"].insert(0, student.get("birthDay", ""))
        
        self.notebook.select(1) # الانتقال لتبويب التسجيل
        
    def save_or_update_student(self):
        """حفظ أو تحديث بيانات الطالب."""
        data = {}
        for key, entry in self.entry_fields.items():
            value = entry.get()
            # محاولة تحويل الأرقام إلى float أو int حسب الحاجة
            if key in ["paidAmount", "birthYear", "birthMonth", "birthDay"]:
                try:
                    if key == "paidAmount":
                        data[key] = float(value)
                    else:
                        data[key] = int(value)
                except ValueError:
                    messagebox.showerror("خطأ في البيانات", f"يرجى إدخال أرقام صحيحة في حقل {key}.")
                    return
            else:
                data[key] = value

        if not data["name"]:
            messagebox.showerror("خطأ", "الرجاء إدخال اسم الطالب.")
            return

        # التحقق من صحة تاريخ الميلاد
        try:
            birth_date_str = f"{data['birthYear']}-{data['birthMonth']}-{data['birthDay']}"
            datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("خطأ في التاريخ", "يرجى إدخال تاريخ ميلاد صحيح (سنة، شهر، يوم).")
            return

        if self.current_student_id is not None:
            # وضع التعديل
            index = next((i for i, s in enumerate(self.students) if s["id"] == self.current_student_id), -1)
            if index != -1:
                data["id"] = self.current_student_id
                data["timestamp"] = datetime.now().isoformat()
                self.students[index] = data
                messagebox.showinfo("نجاح", f"تم تعديل بيانات الطالب {data['name']} بنجاح.")
        else:
            # وضع التسجيل الجديد
            data["id"] = self.next_id
            data["timestamp"] = datetime.now().isoformat()
            self.students.append(data)
            self.next_id += 1
            messagebox.showinfo("نجاح", f"تم تسجيل الطالب {data['name']} بنجاح.")

        self.reset_form()
        self.save_data_and_update()

    def delete_student(self, student_id):
        """حذف طالب من القائمة."""
        student = next((s for s in self.students if s["id"] == student_id), None)
        if not student: return

        if messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف الطالب {student['name']} نهائياً؟"):
            self.students = [s for s in self.students if s["id"] != student_id]
            self.save_data_and_update()
            messagebox.showinfo("نجاح", f"تم حذف الطالب {student['name']} بنجاح.")

    # ------------------------------------------------------------------
    # 3.7 دوال إدارة الأقسام
    # ------------------------------------------------------------------
    def add_section(self):
        """إضافة قسم جديد."""
        name = self.new_section_entry.get().strip()
        if name and name not in self.sections:
            self.sections.append(name)
            self.new_section_entry.delete(0, tk.END)
            self.save_data_and_update()
            messagebox.showinfo("نجاح", f"تم إضافة القسم '{name}' بنجاح.")
        elif name:
            messagebox.showwarning("تنبيه", "القسم موجود بالفعل.")
        else:
            messagebox.showwarning("تنبيه", "الرجاء إدخال اسم القسم.")

    def delete_section(self):
        """حذف القسم المحدد من القائمة."""
        try:
            selected_index = self.sections_listbox.curselection()[0]
            section_name = self.sections_listbox.get(selected_index)
        except IndexError:
            messagebox.showwarning("تنبيه", "الرجاء تحديد قسم لحذفه.")
            return

        if section_name == 'غير محدد':
            messagebox.showerror("خطأ", "لا يمكن حذف القسم الافتراضي 'غير محدد'.")
            return

        students_in_section = [s for s in self.students if s.get('section') == section_name]
        if students_in_section:
            if not messagebox.askyesno("تحذير", f"يوجد {len(students_in_section)} طلاب مسجلين في هذا القسم. هل تريد حذفه ونقل الطلاب إلى 'غير محدد'؟"):
                return
            
            # نقل الطلاب
            for student in students_in_section:
                student['section'] = 'غير محدد'

        self.sections.pop(selected_index)
        self.save_data_and_update()
        messagebox.showinfo("نجاح", f"تم حذف القسم '{section_name}' بنجاح.")
        
    def render_section_list(self):
        """عرض قائمة الأقسام في تبويب الإدارة."""
        self.sections_listbox.delete(0, tk.END)
        for section in self.sections:
            student_count = len([s for s in self.students if s.get('section') == section])
            self.sections_listbox.insert(tk.END, f"{section} ({student_count} طلاب)")

    # ------------------------------------------------------------------
    # 3.8 دوال العرض والتقارير
    # ------------------------------------------------------------------
    def get_payment_status(self, date_str):
        """حساب حالة الدفع بالاعتماد على تاريخ الاستحقاق."""
        try:
            due_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            diff = (due_date - today).days
            
            if diff < 0:
                return f"متأخر ({-diff} يوم)", diff, '#e74c3c' # أحمر
            elif diff == 0:
                return "مستحق اليوم!", diff, '#f1c40f' # أصفر
            elif diff <= 7:
                return f"مستحق خلال {diff} أيام", diff, '#f1c40f' # أصفر
            else:
                return f"نشط (متبقي {diff} يوم)", diff, '#2ecc71' # أخضر
        except ValueError:
            return "تاريخ غير صالح", 9999, '#7f8c8d' # رمادي

    def calculate_and_render_dashboard(self):
        """حساب وتحديث بطاقات وملخص لوحة القيادة."""
        total_students = len(self.students)
        late_payments = 0
        due_soon = 0
        total_fees = sum(s.get('paidAmount', 0) for s in self.students)
        
        # مسح بيانات الجدول القديمة
        for i in self.follow_up_tree.get_children():
            self.follow_up_tree.delete(i)
            
        follow_up_list = []

        for student in self.students:
            status, days_diff, color = self.get_payment_status(student.get('lastPaymentDate', ''))
            
            if days_diff < 0:
                late_payments += 1
            elif days_diff <= 7:
                due_soon += 1
                
            if days_diff <= 7 and days_diff >= -30: # متابعة المتأخرين حتى شهر والمستحقين قريباً
                follow_up_list.append((student, status, color))

        # تحديث بطاقات الملخص
        self.summary_labels["total"].config(text=f"{total_students} طالب")
        self.summary_labels["late"].config(text=f"{late_payments} متأخر")
        self.summary_labels["due_soon"].config(text=f"{due_soon} قريباً")
        self.summary_labels["fees"].config(text=f"{total_fees:,.2f} ج.م")

        # عرض جدول المتابعة (ترتيب حسب أيام التأخير/الاستحقاق)
        follow_up_list.sort(key=lambda x: self.get_payment_status(x[0].get('lastPaymentDate', ''))[1])

        for student, status, color in follow_up_list:
            item_id = self.follow_up_tree.insert("", tk.END, values=(
                student.get('name', 'N/A'),
                student.get('section', 'N/A'),
                student.get('phone', 'N/A'),
                student.get('lastPaymentDate', 'N/A'),
                status
            ))
            # يمكن إضافة علامات للتمييز اللوني
            # self.follow_up_tree.tag_configure(item_id, background=color) # لا يعمل بشكل جيد في كل الأنظمة
            # يمكن وضع علامة في نهاية الصف لسهولة القراءة
            pass

    def render_list(self, event=None):
        """عرض قائمة الطلاب في تبويب القائمة، مع تطبيق البحث."""
        search_term = self.search_entry.get().lower()
        
        # مسح الجدول القديم
        for i in self.list_tree.get_children():
            self.list_tree.delete(i)

        filtered_students = [
            s for s in self.students 
            if search_term in s.get('name', '').lower() or 
               search_term in s.get('phone', '').lower() or
               search_term in s.get('section', '').lower()
        ]
        
        # عرض الطلاب (الأحدث تسجيلاً أولاً)
        filtered_students.sort(key=lambda s: s.get('timestamp', ''), reverse=True)

        for student in filtered_students:
            status, _, _ = self.get_payment_status(student.get('lastPaymentDate', ''))
            
            # إنشاء الأزرار كنص مؤقت في العمود، سيتم معالجته عند النقر
            actions = f"تعديل|{student['id']}|حذف" 

            self.list_tree.insert("", tk.END, values=(
                student['id'],
                student['name'],
                student.get('phone', 'N/A'),
                student.get('section', 'غير محدد'),
                student.get('lastPaymentDate', 'N/A'),
                f"{student.get('paidAmount', 0.0):,.2f}",
                status,
                actions
            ))
            
    def on_double_click(self, event):
        """معالجة النقر المزدوج لفتح نموذج التعديل."""
        item_id = self.list_tree.focus()
        if item_id:
            values = self.list_tree.item(item_id, 'values')
            if values:
                self.load_student_to_form(int(values[0])) # ID هو العنصر الأول

    def on_action_click(self, event):
        """معالجة النقر على عمود الإجراءات."""
        # الحصول على العنصر الذي تم النقر عليه
        item_id = self.list_tree.focus()
        if not item_id: return

        # تحديد مكان النقر داخل العنصر
        region = self.list_tree.identify_region(event.x, event.y)
        if region != "cell": return
        
        column_index = self.list_tree.identify_column(event.x)
        if self.list_tree.heading(column_index, 'text') != "الإجراءات": return

        # استخراج القيم من الصف
        values = self.list_tree.item(item_id, 'values')
        if not values: return

        # ID هو العنصر الأول
        student_id = int(values[0])
        action_text = self.list_tree.set(item_id, 'actions')
        
        # تحديد موقع النقر بدقة داخل خلية الإجراءات
        # هذا حل تقريبي لأنه لا يمكن وضع أزرار حقيقية داخل Treeview في tkinter بسهولة
        
        # افتراض: النصف الأول من الخلية للنقر هو 'تعديل'، النصف الثاني هو 'حذف'
        bbox = self.list_tree.bbox(item_id, 'actions')
        if not bbox: return
        cell_width = bbox[2]
        
        # حساب النقر (هل في النصف الأيمن أم الأيسر من خلية الإجراءات)
        # Note: In RTL, the first action ('تعديل') should be visually on the right
        click_x_relative = event.x - bbox[0]
        
        if click_x_relative < cell_width / 2:
             # النصف الأيسر (حذف)
             self.delete_student(student_id)
        else:
            # النصف الأيمن (تعديل)
             self.load_student_to_form(student_id)
        
    def generate_late_payment_message(self):
        """إنشاء رسالة متابعة مجمعة للطلاب المتأخرين."""
        late_students = [
            s for s in self.students 
            if self.get_payment_status(s.get('lastPaymentDate', ''))[1] < 0
        ]

        if not late_students:
            messagebox.showinfo("تنبيه", "🥳 لا يوجد طلاب متأخرين عن الدفع حالياً. كل شيء تمام!")
            return

        message_lines = [
            "**ملخص متابعة الأقساط المتأخرة**",
            f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}",
            f"إجمالي عدد الطلاب المتأخرين: {len(late_students)} طالب.",
            "-" * 50
        ]
        
        for student in late_students:
            status, days_diff, _ = self.get_payment_status(student.get('lastPaymentDate', ''))
            days_late = abs(days_diff)
            
            message_lines.append(f"الطالب: {student['name']}")
            message_lines.append(f"هاتف ولي الأمر: {student.get('phone', 'N/A')}")
            message_lines.append(f"تأخير: {days_late} يوم (استحقاق: {student.get('lastPaymentDate')})")
            message_lines.append("-" * 50)
            
        message_box_content = "\n".join(message_lines)
        
        # عرض الرسالة في نافذة جديدة قابلة للنسخ
        top = tk.Toplevel(self.master)
        top.title("رسالة متابعة جماعية")
        
        tk.Label(top, text="الرسالة جاهزة للنسخ:", font=("Arial", 12, "bold")).pack(padx=10, pady=5)
        
        text_widget = tk.Text(top, height=20, width=80, font=("Courier", 10))
        text_widget.insert(tk.END, message_box_content)
        text_widget.pack(padx=10, pady=5)
        
        def copy_to_clipboard():
            top.clipboard_clear()
            top.clipboard_append(message_box_content)
            messagebox.showinfo("نجاح", "تم نسخ الرسالة إلى الحافظة!")

        tk.Button(top, text="نسخ إلى الحافظة", command=copy_to_clipboard, bg="#3498db", fg="white").pack(pady=10)

    # ------------------------------------------------------------------
    # 3.9 دالة الحفظ وإعادة تحديث الواجهة
    # ------------------------------------------------------------------
    def save_data_and_update(self):
        """حفظ البيانات وإعادة تحديث جميع مكونات الواجهة."""
        save_data(self.students, self.sections, self.next_id)
        self.update_all_views()


# ======================================================================
# القسم 4: بدء تشغيل التطبيق
# ======================================================================

if __name__ == '__main__':
    # تهيئة الواجهة الرئيسية
    root = tk.Tk()
    
    # ضبط الخط واللغة لدعم العربية بشكل أفضل
    try:
        root.tk.call('font', 'create', 'ArialRTL', '-family', 'Cairo', '-size', 10)
        root.option_add('*Font', 'ArialRTL')
        # محاولة تعيين الاتجاه العام للواجهة (قد لا يعمل في كل الأنظمة)
        root.tk.call('tk', 'option', 'add', '*TextDirection', 'rtl') 
        root.tk.call('tk', 'option', 'add', '*TCombobox*Listbox.TextDirection', 'rtl')

    except Exception as e:
        print(f"Warning: Could not set Arabic font/RTL options: {e}")

    app = StudentManagerApp(root)
    root.mainloop()