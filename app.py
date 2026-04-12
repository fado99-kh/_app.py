import streamlit as st
from datetime import datetime, date
import pandas as pd

st.set_page_config(
    page_title="منظّم حياتي",
    page_icon="🗓️",
    layout="wide"
)

# ----------------------------
# Helpers
# ----------------------------
def init_state():
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            {"title": "الذهاب إلى النادي", "category": "نادي", "time": "18:00", "done": False},
            {"title": "بدء أوبر", "category": "أوبر", "time": "19:30", "done": False},
            {"title": "قراءة 20 دقيقة", "category": "شخصي", "time": "22:00", "done": False},
        ]

    if "goals" not in st.session_state:
        st.session_state.goals = [
            {"title": "الصلاة 5/5 يوميًا", "type": "يومي", "target": 5, "current": 0},
            {"title": "النادي 5 مرات أسبوعيًا", "type": "أسبوعي", "target": 5, "current": 1},
            {"title": "20 ساعة أوبر أسبوعيًا", "type": "أسبوعي", "target": 20, "current": 4},
        ]

    if "prayers" not in st.session_state:
        st.session_state.prayers = {
            "الفجر": {"time": "05:20", "done": False},
            "الظهر": {"time": "13:20", "done": False},
            "العصر": {"time": "16:45", "done": False},
            "المغرب": {"time": "19:55", "done": False},
            "العشاء": {"time": "21:30", "done": False},
        }

    if "water" not in st.session_state:
        st.session_state.water = 0

    if "uber_hours" not in st.session_state:
        st.session_state.uber_hours = 0.0

    if "gym_done" not in st.session_state:
        st.session_state.gym_done = False

    if "username" not in st.session_state:
        st.session_state.username = "فؤاد"

    if "city" not in st.session_state:
        st.session_state.city = "Edmonton"

    if "motivation" not in st.session_state:
        st.session_state.motivation = "ابدأ يومك بخطة واضحة."

init_state()

def get_next_prayer():
    now = datetime.now().strftime("%H:%M")
    for prayer_name, prayer_data in st.session_state.prayers.items():
        if prayer_data["time"] >= now:
            return prayer_name, prayer_data["time"]
    # If all prayers passed, show first prayer tomorrow
    first_prayer = list(st.session_state.prayers.items())[0]
    return f"{first_prayer[0]} (غدًا)", first_prayer[1]["time"]

def calc_daily_progress():
    task_total = len(st.session_state.tasks)
    task_done = sum(1 for t in st.session_state.tasks if t["done"])

    prayer_total = len(st.session_state.prayers)
    prayer_done = sum(1 for p in st.session_state.prayers.values() if p["done"])

    gym_score = 1 if st.session_state.gym_done else 0
    gym_total = 1

    total_items = task_total + prayer_total + gym_total
    done_items = task_done + prayer_done + gym_score

    if total_items == 0:
        return 0
    return int((done_items / total_items) * 100)

def get_motivation_message(progress):
    if progress >= 85:
        return "ممتاز جدًا، التزامك اليوم قوي 👏"
    elif progress >= 60:
        return "أنت ماشي بشكل جيد، كمل 👍"
    elif progress >= 30:
        return "بداية جيدة، شد حيلك شوي 💪"
    else:
        return "ابدأ بمهمة صغيرة الآن حتى تدخل جو الإنجاز."

def category_color(cat):
    colors = {
        "نادي": "💪",
        "أوبر": "🚗",
        "عمل": "💼",
        "صلاة": "🕌",
        "شخصي": "📝"
    }
    return colors.get(cat, "📌")

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.session_state.username = st.text_input("اسم المستخدم", value=st.session_state.username)
    st.session_state.city = st.text_input("المدينة", value=st.session_state.city)
    st.session_state.motivation = st.text_input("رسالة ترحيب", value=st.session_state.motivation)

    st.markdown("---")
    st.subheader("🕌 أوقات الصلاة")
    for prayer in st.session_state.prayers:
        st.session_state.prayers[prayer]["time"] = st.text_input(
            f"وقت {prayer}",
            value=st.session_state.prayers[prayer]["time"],
            key=f"time_{prayer}"
        )

# ----------------------------
# Header
# ----------------------------
today_str = date.today().strftime("%Y-%m-%d")
progress = calc_daily_progress()
next_prayer_name, next_prayer_time = get_next_prayer()

st.title("🗓️ منظّم حياتي")
st.caption(f"اليوم: {today_str} | المدينة: {st.session_state.city}")

colA, colB, colC = st.columns([2, 1, 1])

with colA:
    st.subheader(f"السلام عليكم، {st.session_state.username}")
    st.write(st.session_state.motivation)

with colB:
    st.metric("الصلاة القادمة", next_prayer_name, next_prayer_time)

with colC:
    st.metric("نسبة إنجاز اليوم", f"{progress}%")

st.progress(progress / 100)
st.info(get_motivation_message(progress))

# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 الرئيسية",
    "✅ المهام",
    "🕌 الصلاة",
    "🎯 الأهداف",
    "📊 التقارير"
])

# ----------------------------
# Home Tab
# ----------------------------
with tab1:
    st.subheader("ملخص اليوم")

    c1, c2, c3, c4 = st.columns(4)

    tasks_done = sum(1 for t in st.session_state.tasks if t["done"])
    prayers_done = sum(1 for p in st.session_state.prayers.values() if p["done"])

    c1.metric("المهام المكتملة", f"{tasks_done}/{len(st.session_state.tasks)}")
    c2.metric("الصلوات", f"{prayers_done}/5")
    c3.metric("ساعات أوبر", f"{st.session_state.uber_hours}")
    c4.metric("النادي", "تم" if st.session_state.gym_done else "لم يتم")

    st.markdown("### أهم مهام اليوم")
    if st.session_state.tasks:
        for task in st.session_state.tasks[:3]:
            status = "✅" if task["done"] else "⏳"
            st.write(f"{status} {category_color(task['category'])} **{task['title']}** - {task['time']}")
    else:
        st.write("لا توجد مهام حتى الآن.")

    st.markdown("### الجدول الزمني")
    timeline = []

    for prayer_name, prayer_data in st.session_state.prayers.items():
        timeline.append({"الوقت": prayer_data["time"], "العنصر": prayer_name, "النوع": "صلاة"})

    for task in st.session_state.tasks:
        timeline.append({"الوقت": task["time"], "العنصر": task["title"], "النوع": task["category"]})

    timeline_df = pd.DataFrame(timeline).sort_values("الوقت")
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)

# ----------------------------
# Tasks Tab
# ----------------------------
with tab2:
    st.subheader("إدارة المهام والأنشطة")

    with st.expander("➕ إضافة مهمة جديدة", expanded=False):
        with st.form("add_task_form"):
            title = st.text_input("اسم المهمة")
            category = st.selectbox("الفئة", ["شخصي", "عمل", "أوبر", "نادي"])
            time_value = st.text_input("الوقت", value="18:00")
            submitted = st.form_submit_button("إضافة")

            if submitted and title.strip():
                st.session_state.tasks.append({
                    "title": title.strip(),
                    "category": category,
                    "time": time_value,
                    "done": False
                })
                st.success("تمت إضافة المهمة.")

    st.markdown("### قائمة المهام")
    if not st.session_state.tasks:
        st.write("لا توجد مهام.")
    else:
        delete_index = None
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.write(f"{category_color(task['category'])} **{task['title']}**")
                st.caption(f"{task['category']} - {task['time']}")

            with col2:
                checked = st.checkbox("تم", value=task["done"], key=f"task_done_{i}")
                st.session_state.tasks[i]["done"] = checked

            with col3:
                new_time = st.text_input("الوقت", value=task["time"], key=f"task_time_{i}")
                st.session_state.tasks[i]["time"] = new_time

            with col4:
                if st.button("🗑️", key=f"delete_task_{i}"):
                    delete_index = i

        if delete_index is not None:
            st.session_state.tasks.pop(delete_index)
            st.rerun()

    st.markdown("### متابعة سريعة")
    st.session_state.gym_done = st.checkbox("تم الذهاب إلى النادي اليوم", value=st.session_state.gym_done)
    st.session_state.uber_hours = st.number_input("عدد ساعات أوبر اليوم", min_value=0.0, max_value=24.0, value=float(st.session_state.uber_hours), step=0.5)
    st.session_state.water = st.number_input("كم كوب ماء شربت اليوم؟", min_value=0, max_value=30, value=int(st.session_state.water), step=1)

# ----------------------------
# Prayer Tab
# ----------------------------
with tab3:
    st.subheader("متابعة الصلاة")

    prayer_count = 0
    for prayer_name, prayer_data in st.session_state.prayers.items():
        c1, c2, c3 = st.columns([3, 2, 2])

        with c1:
            st.write(f"🕌 **{prayer_name}**")

        with c2:
            st.write(f"الوقت: {prayer_data['time']}")

        with c3:
            done = st.checkbox("تمت", value=prayer_data["done"], key=f"prayer_done_{prayer_name}")
            st.session_state.prayers[prayer_name]["done"] = done
            if done:
                prayer_count += 1

    st.markdown("---")
    st.metric("عدد الصلوات المكتملة", f"{prayer_count}/5")
    st.progress(prayer_count / 5)

    if prayer_count == 5:
        st.success("ما شاء الله، أتممت كل الصلوات اليوم 🤍")
    elif prayer_count >= 3:
        st.info("أحسنت، كمل باقي الصلوات.")
    else:
        st.warning("ابدأ من الصلاة القادمة وامشِ خطوة خطوة.")

# ----------------------------
# Goals Tab
# ----------------------------
with tab4:
    st.subheader("الأهداف")

    with st.expander("➕ إضافة هدف جديد", expanded=False):
        with st.form("add_goal_form"):
            g_title = st.text_input("اسم الهدف")
            g_type = st.selectbox("نوع الهدف", ["يومي", "أسبوعي", "شهري"])
            g_target = st.number_input("العدد المستهدف", min_value=1, max_value=1000, value=5, step=1)
            g_current = st.number_input("المنجز حاليًا", min_value=0, max_value=1000, value=0, step=1)
            g_submit = st.form_submit_button("إضافة الهدف")

            if g_submit and g_title.strip():
                st.session_state.goals.append({
                    "title": g_title.strip(),
                    "type": g_type,
                    "target": int(g_target),
                    "current": int(g_current)
                })
                st.success("تمت إضافة الهدف.")

    if not st.session_state.goals:
        st.write("لا توجد أهداف.")
    else:
        remove_goal_idx = None
        for i, goal in enumerate(st.session_state.goals):
            st.markdown(f"### {goal['title']}")
            st.caption(f"النوع: {goal['type']}")

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                current_val = st.number_input(
                    f"المنجز - {goal['title']}",
                    min_value=0,
                    max_value=100000,
                    value=int(goal["current"]),
                    step=1,
                    key=f"goal_current_{i}"
                )
                st.session_state.goals[i]["current"] = current_val

            with col2:
                target_val = st.number_input(
                    f"المستهدف - {goal['title']}",
                    min_value=1,
                    max_value=100000,
                    value=int(goal["target"]),
                    step=1,
                    key=f"goal_target_{i}"
                )
                st.session_state.goals[i]["target"] = target_val

            with col3:
                if st.button("🗑️ حذف", key=f"delete_goal_{i}"):
                    remove_goal_idx = i

            ratio = min(goal["current"] / goal["target"], 1.0) if goal["target"] > 0 else 0
            st.progress(ratio)
            st.write(f"التقدم: {goal['current']} / {goal['target']}")

        if remove_goal_idx is not None:
            st.session_state.goals.pop(remove_goal_idx)
            st.rerun()

# ----------------------------
# Reports Tab
# ----------------------------
with tab5:
    st.subheader("التقارير")

    tasks_done = sum(1 for t in st.session_state.tasks if t["done"])
    tasks_total = len(st.session_state.tasks)

    prayers_done = sum(1 for p in st.session_state.prayers.values() if p["done"])
    prayers_total = len(st.session_state.prayers)

    report_data = pd.DataFrame({
        "القسم": ["المهام", "الصلاة", "النادي", "أوبر"],
        "القيمة": [
            tasks_done,
            prayers_done,
            1 if st.session_state.gym_done else 0,
            st.session_state.uber_hours
        ]
    })

    st.markdown("### نظرة عامة")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("المهام", f"{tasks_done}/{tasks_total}")
    r2.metric("الصلاة", f"{prayers_done}/{prayers_total}")
    r3.metric("النادي", "1/1" if st.session_state.gym_done else "0/1")
    r4.metric("أوبر", f"{st.session_state.uber_hours} ساعة")

    st.markdown("### رسم بسيط")
    st.bar_chart(report_data.set_index("القسم"))

    st.markdown("### رسالة اليوم")
    if progress >= 80:
        st.success("يومك ممتاز. استمر على نفس الرتم.")
    elif progress >= 50:
        st.info("يوم جيد، وباقي خطوة أو خطوتين ليصير ممتاز.")
    else:
        st.warning("ابدأ الآن بمهمة صغيرة أو صلاة قادمة حتى ترفع نسبة الإنجاز.")

st.markdown("---")
st.caption("تم تصميم هذه النسخة الأولية لتجربة الفكرة بسرعة داخل Streamlit.")