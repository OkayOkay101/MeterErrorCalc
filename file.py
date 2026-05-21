import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าตาของโปรแกรม
st.set_page_config(page_title="โปรแกรมหาค่าความคลาดเคลื่อนมิเตอร์", page_icon="⚡", layout="wide")

st.title("⚡ โปรแกรมหาค่าความคลาดเคลื่อนมิเตอร์ (% Error)")
st.write("เปรียบเทียบ **🔴 ก่อนแก้ไขผิดปกติ** และ **🟢 หลังแก้ไขผิดปกติ** เพื่อหาค่า Error")

# 2. สร้างหน้า (Tabs) แยกกันอย่างชัดเจน
tab_old, tab_new, tab_summary = st.tabs([
    "🔴 หน้ากรอกข้อมูล: ก่อนแก้ไขผิดปกติ", 
    "🟢 หน้ากรอกข้อมูล: หลังแก้ไขผิดปกติ", 
    "📊 หน้าสรุปผลความคลาดเคลื่อน"
])

# ==========================================
# หน้าที่ 1: กรอกข้อมูลก่อนแก้ไขผิดปกติ
# ==========================================
with tab_old:
    st.header("🔴 บันทึกข้อมูลรายละเอียดก่อนแก้ไขผิดปกติ")
    st.caption("💡 ทุกช่องเป็นค่าว่างแล้ว สามารถคลิกแล้วพิมพ์ตัวเลขลงไปได้ทันที ไม่ต้องกดลบของเก่า")
    
    col1, col2, col3 = st.columns(3)
    
    def get_old_inputs(rate_name, idx):
        st.subheader(f"📝 Rate {rate_name}")
        # ปรับใช้ value=None และใส่ placeholder เพื่อให้คลิกแล้วพิมพ์ได้เลย
        v_in = st.number_input(f"1. Voltage (V{idx})", value=None, placeholder="เช่น 220.0000", format="%.4f", step=0.0001, key=f"v_old_{rate_name}")
        i_in = st.number_input(f"2. Current (I{idx})", value=None, placeholder="เช่น 10.0000", format="%.4f", step=0.0001, key=f"i_old_{rate_name}")
        pf_in = st.number_input(f"3. Power Factor (PF{idx})", value=None, placeholder="เช่น 0.8000", format="%.4f", step=0.0001, key=f"pf_old_{rate_name}")
        
        # ดักจับถ้าเป็นค่าว่าง (None) ให้คิดเป็น 0.0 แทน เพื่อป้องกันโปรแกรมแครช
        v = v_in if v_in is not None else 0.0
        i = i_in if i_in is not None else 0.0
        pf = pf_in if pf_in is not None else 0.0
        
        kw = (v * i * pf) / 1000
        st.info(f"กำลังไฟฟ้า Rate {rate_name}: **{kw:.6f} kW**") 
        return kw

    with col1: kw_old_A = get_old_inputs("A", 1)
    with col2: kw_old_B = get_old_inputs("B", 2)
    with col3: kw_old_C = get_old_inputs("C", 3)

# ==========================================
# หน้าที่ 2: กรอกข้อมูลหลังแก้ไขผิดปกติ
# ==========================================
with tab_new:
    st.header("🟢 บันทึกข้อมูลรายละเอียดหลังแก้ไขผิดปกติ")
    st.caption("💡 ทุกช่องเป็นค่าว่างแล้ว สามารถคลิกแล้วพิมพ์ตัวเลขลงไปได้ทันที ไม่ต้องกดลบของเก่า")
    
    col1, col2, col3 = st.columns(3)
    
    def get_new_inputs(rate_name, idx):
        st.subheader(f"📝 Rate {rate_name}")
        v_in = st.number_input(f"1. Voltage (V{idx}) ", value=None, placeholder="เช่น 220.0000", format="%.4f", step=0.0001, key=f"v_new_{rate_name}")
        i_in = st.number_input(f"2. Current (I{idx}) ", value=None, placeholder="เช่น 10.0000", format="%.4f", step=0.0001, key=f"i_new_{rate_name}")
        pf_in = st.number_input(f"3. Power Factor (PF{idx}) ", value=None, placeholder="เช่น 0.9500", format="%.4f", step=0.0001, key=f"pf_new_{rate_name}")
        
        v = v_in if v_in is not None else 0.0
        i = i_in if i_in is not None else 0.0
        pf = pf_in if pf_in is not None else 0.0
        
        kw = (v * i * pf) / 1000
        st.success(f"กำลังไฟฟ้า Rate {rate_name}: **{kw:.6f} kW**")
        return kw

    with col1: kw_new_A = get_new_inputs("A", 1)
    with col2: kw_new_B = get_new_inputs("B", 2)
    with col3: kw_new_C = get_new_inputs("C", 3)

# ==========================================
# หน้าที่ 3: สรุปผลความคลาดเคลื่อน (% Error)
# ==========================================
with tab_summary:
    st.header("📊 สรุปผลหาค่าความคลาดเคลื่อนมิเตอร์")
    
    # รวมค่า kW ทั้ง 3 Rate
    total_old = kw_old_A + kw_old_B + kw_old_C
    total_new = kw_new_A + kw_new_B + kw_new_C
    
    # คำนวณส่วนต่าง (ดิบ)
    diff_kw = total_old - total_new
    
    # คำนวณ % Error ตามสูตร: ((ก่อนแก้ไข / หลังแก้ไข) - 1) * 100
    if total_new > 0:
        percent_error = ((total_old / total_new) - 1) * 100
    else:
        percent_error = 0.0

    # สร้าง Dashboard ด้านบน
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("🔴 ก่อนแก้ไขผิดปกติ", f"{total_old:.6f} kW")
    col_b.metric("🟢 หลังแก้ไขผิดปกติ", f"{total_new:.6f} kW")
    
    # แสดงผลตามค่า % Error
    if percent_error > 0:
        col_c.metric("📈 ค่าความคลาดเคลื่อน (% Error)", f"+{percent_error:.4f}%", f"+{diff_kw:.6f} kW", delta_color="inverse")
        st.warning(f"⚠️ **มิเตอร์หมุนเร็วไป (Fast):** มิเตอร์อ่านค่าได้มากกว่าความเป็นจริง **{percent_error:.4f}%**")
    elif percent_error < 0:
        col_c.metric("📉 ค่าความคลาดเคลื่อน (% Error)", f"{percent_error:.4f}%", f"{diff_kw:.6f} kW", delta_color="normal")
        st.info(f"⚠️ **มิเตอร์หมุนช้าไป (Slow):** มิเตอร์อ่านค่าได้น้อยกว่าความเป็นจริง **{percent_error:.4f}%**")
    else:
        col_c.metric("⚖️ ค่าความคลาดเคลื่อน (% Error)", "0.0000%", "0.0000 kW", delta_color="off")
        st.success("✅ **ผลลัพธ์:** มิเตอร์มีความเที่ยงตรงสมบูรณ์ (Error = 0%)")

    st.markdown("---")
    
    # สร้างตารางแจกแจงตาม Rate A, B, C
    st.subheader("ตารางแจกแจงรายละเอียดราย Rate (kW)")
    
    data = {
        "รายการ": ["Rate A", "Rate B", "Rate C", "รวมทั้งหมด (Total)"],
        "🔴 ก่อนแก้ไขผิดปกติ": [f"{kw_old_A:.6f}", f"{kw_old_B:.6f}", f"{kw_old_C:.6f}", f"{total_old:.6f}"],
        "🟢 หลังแก้ไขผิดปกติ": [f"{kw_new_A:.6f}", f"{kw_new_B:.6f}", f"{kw_new_C:.6f}", f"{total_new:.6f}"],
        "⚖️ ผลต่าง (kW)": [f"{(kw_old_A - kw_new_A):.6f}", f"{(kw_old_B - kw_new_B):.6f}", f"{(kw_old_C - kw_new_C):.6f}", f"{diff_kw:.6f}"]
    }
    
    # แสดงตาราง
    df = pd.DataFrame(data)
    st.table(df)