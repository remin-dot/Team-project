##  จัดทำโดย

- นายชัชนันท์ บุญส่ง รหัสนักศึกษา 6810110055
- นายพลกฤต บัวลอย รหัสนักศึกษา 6810110223
- นายศุภกิตต์ เชี่ยวหมอน รหัสนักศึกษา 6810110354

---

## โครงสร้างโปรเจกต์

```

Team-project/
├── data/
│   ├── predict/
│   │   └── predictions.csv
│   ├── processed/
│   │   └── datas_cleaned.csv
│   └── raw/
│       └── datas.csv
├── notebooks/
│     ├── cleaning.ipynb
│     ├── modeling_timeseries_future_prediction.ipynb
│     └── modeling_timeseries_present_prediction.ipynb
├── app.py
├── README.md
└── requirements.txt

```

---

##  โครงสร้างไฟล์

`app.py`
-  เป็นเว็บแอป Dash ที่แสดงกราฟรายได้จริงและพยากรณ์พร้อมตัวเลือกในการพยากรณ์

`datas.csv`
-  ข้อมูลดิบที่รวบรวมจากแหล่งข้อมูลต้นทาง

`datas_cleaned.csv`
-  ข้อมูลที่ผ่านการทำความสะอาดและเตรียมสำหรับโมเดล

`predictions.csv`
-  ผลลัพธ์การพยากรณ์ที่ถูกนำมาใช้ในแดชบอร์ด

`cleaning.ipynb`
-  กระบวนการเตรียมข้อมูลและการเตรียม dataset สำหรับโมเดล

`modeling_timeseries_present_prediction.ipynb`
-  สร้างโมเดลพยากรณ์สำหรับช่วงปัจจุบันใน dataset พร้อมการประเมินความแม่นยำ

`modeling_timeseries_future_prediction.ipynb`
-  สร้างโมเดลพยากรณ์อนาคตและบันทึก predictions.csv

---

## วิธีการใช้หน้า dashboard
1. เลือกภูมิภาค
2. เลือกขนาดหอพัก
3. เลือกการเพิ่มขึ้นหรือลดลงของนักท่องเทียว

---

## ไลบรารีหลักที่ใช้
- `autogluon` – สำหรับสร้างโมเดล Machine Learning
- `dash` – สร้างเว็บแดชบอร์ด
- `plotly` – วาดกราฟ
- `jupyter` – รันโน้ตบุ๊ก

---

##  เริ่มใช้งาน (Run)

1. สร้าง Virtual Environment

```
python venv venv
```

2. Activate Virtual Environment

```
venv/Scripts/activate
```

3. Install Package

```
pip install -r requirements.txt
```

4. รัน jupyter ก่อนรัน app

```
cleaning.ipynb
modeling_timeseries_present_prediction.ipynb
modeling_timeseries_future_prediction.ipynb
```

5. รันแอป:

```bash
python app.py
```

6. เปิดเบราว์เซอร์ไปที่:

```
http://127.0.0.1:8050
```

---

## ที่มาของข้อมูล

https://data.go.th/dataset/os_17_0007_01

---

## การทำความสะอาดข้อมูล (Data Cleaning)
กระบวนการนี้รันใน `notebooks/cleaning.ipynb` 

1. **โหลดและกรองข้อมูล**
   - อ่านไฟล์ `data/raw/datas.csv`
   - ตัดแถวที่มีค่าที่ไม่สมบูรณ์ในคอลัมน์ `region`หรือ `size_estabish` 

2. **ปรับโครงสร้างข้อมูล**
   - ลบช่องว่างรอบชื่อคอลัมน์เพื่อให้เรียกใช้งานได้ตรง
   - แปลงชื่อภูมิภาคจากภาษาไทยเป็นกลุ่มภูมิภาคมาตรฐาน: Bangkok, Central, Northern, Northeastern, Southern

3. **ปรับหน่วยและสเกล**
   - แปลงค่าในคอลัมน์ `value` โดยคูณด้วย 1,000 เพื่อให้เป็นจำนวนเต็มที่สอดคล้องกับหน่วย 

4. **สร้างฟีเจอร์ใหม่**
   - สร้าง `size_rank` จากค่า `size_estabish` เพื่อให้โมเดลรับค่าตัวเลขได้ง่ายขึ้น

5. **ลบคอลัมน์ไม่จำเป็น**
   - ตัดคอลัมน์ `unit`, `source`, `size_estabish` ออกเพราะไม่ได้ใช้ในการเทรนโมเดล

6. **จำลองข้อมูลเสริม**
   - สร้างคอลัมน์ `tourists_mn` โดยจำลองจำนวนผู้มาเยือนตามปีและภูมิภาค 

7. **บันทึกผลลัพธ์**
   - เก็บไฟล์ชุดข้อมูลสุดท้ายเป็น `data/processed/datas_cleaned.csv` เพื่อให้โมเดลและแดชบอร์ดเรียกใช้งานได้ทันที

