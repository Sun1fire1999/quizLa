import streamlit as st

# استيراد البيانات
try:
    from data_part1 import questions_1
    from data_part2 import questions_2
    from data_part3 import questions_3
    questions = questions_1 + questions_2 + questions_3
except ImportError:
    st.error("⚠️ يرجى التأكد من وجود ملفات البيانات (data_part1.py, data_part2.py, data_part3.py) في نفس المجلد.")
    st.stop()

# إعدادات الصفحة
st.set_page_config(page_title="اختبار قانون العمل الأردني", layout="centered")
st.title("📝 اختبارات قانون العمل الأردني - حسب الموضوع")
st.markdown("اختر الموضوع من القائمة الجانبية، وتنقل بين الأسئلة بحرية.")

# --- 1. استخراج قائمة المواضيع الفريدة من البيانات ---
all_topics = sorted(list(set(q.get('topic', 'عام') for q in questions)))
# إضافة خيار "الكل"
all_topics.insert(0, "جميع المواضيع")

# --- 2. عرض قائمة اختيار الموضوع في الشريط الجانبي ---
with st.sidebar:
    st.header("🧭 اختيار الموضوع")
    selected_topic = st.selectbox("الموضوع:", all_topics)

    # تصفية الأسئلة حسب الموضوع المختار
    if selected_topic == "جميع المواضيع":
        filtered_questions = questions
    else:
        filtered_questions = [q for q in questions if q.get('topic', 'عام') == selected_topic]

    st.divider()
    st.write(f"عدد الأسئلة في هذا الاختبار: **{len(filtered_questions)}**")

# --- 3. تهيئة حالة الجلسة ---
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

# التأكد من أن الفهرس لا يتجاوز عدد الأسئلة
if st.session_state.current_index >= len(filtered_questions):
    st.session_state.current_index = len(filtered_questions) - 1

# --- 4. عرض السؤال الحالي ---
current_q = filtered_questions[st.session_state.current_index]

# شريط التقدم
st.progress((st.session_state.current_index + 1) / len(filtered_questions))

# عرض الموضوع الحالي
st.write(f"**الموضوع:** {selected_topic}")
st.write(f"**السؤال {st.session_state.current_index + 1} من {len(filtered_questions)}**")
st.write(f"**{current_q['q']}**")

# عرض الخيارات (بدون خلط - كما هي في البيانات)
user_choice = st.radio(
    "اختر الإجابة:",
    current_q['op'],
    key=f"radio_{st.session_state.current_index}",
    index=0  # يمكنك تغيير هذا إذا أردت البدء بخيار معين
)

# --- 5. أزرار التحكم (السابق / تأكيد / التالي) ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ السابق", disabled=(st.session_state.current_index == 0)):
        st.session_state.current_index -= 1
        st.session_state.answered = False
        st.rerun()

with col2:
    if st.button("✅ تأكيد الإجابة"):
        st.session_state.answered = True
        st.session_state.user_choice = user_choice
        if user_choice == current_q['a']:
            st.session_state.score += 1
        # لا نعيد تعيين الاختيار، نبقيه كما هو

with col3:
    if st.button("التالي ➡️", disabled=(st.session_state.current_index == len(filtered_questions) - 1)):
        st.session_state.current_index += 1
        st.session_state.answered = False
        st.rerun()

# --- 6. عرض النتيجة ونص المادة بعد التأكيد ---
if st.session_state.answered:
    st.divider()
    
    # التحقق من الإجابة
    if st.session_state.user_choice == current_q['a']:
        st.success("🎉 إجابة صحيحة!")
    else:
        st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة هي: {current_q['a']}")
    
    # عرض نص المادة الكامل (الحقل e)
    if current_q.get('e'):
        st.info(f"📜 **نص المادة:**\n\n{current_q['e']}")
    else:
        st.info("لا يوجد نص مادة مرفق لهذا السؤال.")

# --- 7. عرض النتيجة في الشريط الجانبي ---
with st.sidebar:
    st.divider()
    st.subheader("📊 نتائجك")
    st.write(f"**الإجابات الصحيحة:** {st.session_state.score}")
    st.write(f"**عدد الأسئلة المجاب عنها:** {st.session_state.current_index + 1 if st.session_state.answered else st.session_state.current_index}")
    
    if st.session_state.current_index > 0:
        percentage = (st.session_state.score / st.session_state.current_index) * 100
        st.write(f"**نسبة الإتقان:** {percentage:.1f}%")
    
    # زر إعادة الاختبار
    if st.button("🔄 إعادة الاختبار الحالي"):
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()