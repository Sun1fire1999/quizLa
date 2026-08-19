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

# --- 1. تعريف الترتيب القانوني الصارم للفئات (مواد القانون) ---
# الترتيب الذي ستظهر به الأسئلة
ORDERED_TOPICS = [
    "أحكام عامة وتعريفات (المواد 1-4)",
    "التفتيش على العمل والرقابة (المواد 5-10)",
    "تنظيم تشغيل العمالة الأجنبية (المواد 11-12)",
    "عقود العمل الفردية والمسؤولية (المواد 13-21)",
    "إنهاء الخدمة وفسخ العقد (المواد 22-30)",
    "الأجور والمزايا المالية (المواد 44-54)",
    "ساعات العمل والعمل الإضافي (المواد 56-60)",
    "الإجازات والراحة (المواد 61-71)",
    "تشغيل الأحداث وحماية المرأة (المواد 72-79)",
    "الصحة والسلامة المهنية (المواد 80-85)",
    "إصابات العمل والتعويضات (المواد 86-96)",
    "النقابات العمالية (المواد 97-124)",
    "المحاكم العمالية والإجراءات القضائية (المواد 125-137)",
    "الملحقات: الأمراض المهنية (الجدول 1)",
    "الملحقات: جداول العجز والإعانة (الجدول 2 و 3)"
]

# --- 2. إعادة ترتيب جميع الأسئلة حسب هذا الترتيب القانوني ---
def get_topic_order(topic):
    try:
        return ORDERED_TOPICS.index(topic)
    except ValueError:
        return 999 # أي موضوع غير معرف يذهب إلى النهاية

# نقوم بترتيب الأسئلة مرة واحدة في الذاكرة
SORTED_QUESTIONS = sorted(questions, key=lambda q: get_topic_order(q.get('topic', '')))

# --- 3. إعدادات الصفحة ---
st.set_page_config(page_title="قانون العمل - تدريب متسلسل", layout="centered")
st.title("📖 التدريب المتسلسل على قانون العمل")
st.markdown("تعتمد هذه الدورة على تسلسل مواد القانون. ركز في كل فئة قبل الانتقال للفئة التالية.")

# --- 4. تهيئة حالة الجلسة (Session State) ---
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- 5. التحقق من انتهاء الأسئلة ---
if st.session_state.index >= len(SORTED_QUESTIONS):
    st.balloons()
    st.success("🎉 لقد أكملت التدريب على تسلسل القانون بالكامل!")
    total_q = len(SORTED_QUESTIONS)
    st.write(f"**النتيجة النهائية:** {st.session_state.score} من {total_q}")
    if total_q > 0:
        percentage = (st.session_state.score / total_q) * 100
        st.write(f"**نسبة الإتقان الكلية:** {percentage:.1f}%")
    
    if st.button("🔄 إعادة الدورة من البداية"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # عرض السؤال الحالي
    current_q = SORTED_QUESTIONS[st.session_state.index]
    total_q = len(SORTED_QUESTIONS)
    
    # شريط التقدم
    st.progress((st.session_state.index + 1) / total_q)

    # --- 6. عرض عنوان الفئة عند بداية كل قسم جديد ---
    # نتحقق من السؤال السابق (إذا كان موجوداً) لنعرف هل تغيرت الفئة
    previous_q = SORTED_QUESTIONS[st.session_state.index - 1] if st.session_state.index > 0 else None
    current_topic = current_q.get('topic', 'أحكام عامة وتعريفات (المواد 1-4)')
    
    if previous_q is None or previous_q.get('topic', '') != current_topic:
        st.divider()
        st.header(f"📍 {current_topic}")
        st.caption(f"هذا القسم يغطي مواد محددة من القانون. تقدم بالترتيب.")
        st.divider()

    # عرض السؤال
    st.write(f"**السؤال {st.session_state.index + 1} من {total_q}**")
    st.write(f"**{current_q['q']}**")

    # عرض الخيارات (بدون خلط عشوائي للحفاظ على تجربة التدريب المنتظمة)
    st.session_state.selected_option = st.radio(
        "اختر الإجابة الصحيحة:",
        current_q['op'],
        key=f"q_{st.session_state.index}"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("تأكيد الإجابة ✅"):
            st.session_state.submitted = True
            if st.session_state.selected_option == current_q['a']:
                st.success("✅ إجابة صحيحة!")
                st.session_state.score += 1
            else:
                st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة هي: {current_q['a']}")
            if current_q.get('e'):
                st.info(f"📖 توضيح: {current_q['e']}")

    with col2:
        if st.button("السؤال التالي ➡️"):
            st.session_state.index += 1
            st.session_state.submitted = False
            st.rerun()

# --- 7. عرض ملخص الحالة في الشريط الجانبي ---
with st.sidebar:
    st.header("📊 ملخص التقدم")
    st.write(f"**الفئة الحالية:** {current_q.get('topic', 'أحكام عامة وتعريفات (المواد 1-4)')}")
    st.write(f"**التقدم:** {st.session_state.index + 1} / {len(SORTED_QUESTIONS)}")
    st.write(f"**الإجابات الصحيحة:** {st.session_state.score}")
    if st.session_state.index > 0:
        percentage = (st.session_state.score / (st.session_state.index + 1)) * 100
        st.write(f"**نسبة الإتقان الحالية:** {percentage:.1f}%")