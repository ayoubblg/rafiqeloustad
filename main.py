import pandas as pd
from datetime import datetime

class DZStudentGradeProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        try:
            if self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            else:
                self.df = pd.read_excel(self.file_path)
            print("[+] تم تحميل ملف الطلبة بنجاح.")
            return True
        except Exception as e:
            print(f"[-] خطأ أثناء تحميل الملف: {e}")
            return False

    def calculate_grades_and_averages(self):
        if self.df is None:
            print("[-] لا توجد بيانات لمعالجتها.")
            return

        grade_columns = ["المراقبة المستمرة", "الأعمال الموجهة", "الامتحان"]
        for col in grade_columns:
            if col not in self.df.columns:
                self.df[col] = 10.0

        self.df["المعدل النهائي"] = (
            self.df["المراقبة المستمرة"] * 0.2 + 
            self.df["الأعمال الموجهة"] * 0.2 + 
            self.df["الامتحان"] * 0.6
        ).round(2)

        self.df["الحالة البيداغوجية"] = self.df["المعدل النهائي"].apply(
            lambda x: "ناجح" if x >= 10 else "راسب / معوض"
        )
        print("[+] تم حساب المعدلات والحالات البيداغوجية بنجاح.")

    def get_pedagogical_summary(self):
        if self.df is None or "المعدل النهائي" not in self.df.columns:
            print("[-] يرجى حساب المعدلات أولاً.")
            return

        total_students = len(self.df)
        successful_students = len(self.df[self.df["الحالة البيداغوجية"] == "ناجح"])
        success_rate = (successful_students / total_students * 100) if total_students > 0 else 0
        
        highest_grade = self.df["المعدل النهائي"].max()
        lowest_grade = self.df["المعدل النهائي"].min()
        class_average = self.df["المعدل النهائي"].mean()

        print("\n" + "="*45)
        print("     التقرير الإحصائي والمعدلات والنسب للبيداغوجيا")
        print("="*45)
        print(f"📊 إجمالي عدد الطلبة المسجلين : {total_students}")
        print(f"✅ عدد الطلبة الناجحين (>= 10): {successful_students}")
        print(f"📈 نسبة النجاح العامة بالفوج   : {success_rate:.2f}%")
        print(f"📐 المتوسط الحسابي العام للفوج : {class_average:.2f} / 20")
        print(f"🏆 أعلى معدل مسجل في الفوج    : {highest_grade} / 20")
        print(f"⚠️ أدنى معدل مسجل في الفوج    : {lowest_grade} / 20")
        print("="*45 + "\n")

    def export_to_new_excel(self, output_path="student_grades_report.xlsx"):
        if self.df is not None:
            self.df.to_excel(output_path, index=False)
            print(f"[+] تم تصدير التقرير الشامل بنجاح إلى: {output_path}")

if __name__ == "__main__":
    processor = DZStudentGradeProcessor("sample_data.xlsx")
    # if processor.load_data():
    #     processor.calculate_grades_and_averages()
    #     processor.get_pedagogical_summary()
    #     processor.export_to_new_excel()
    print("برنامج معالجة القوائم الرسمية الجزائرية جاهز للتشغيل!")
