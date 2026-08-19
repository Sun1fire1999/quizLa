import streamlit as st
import random

# استيراد البيانات من الملفات المنفصلة
try:
    from data_part1 import questions_1
    from data_part2 import questions_2
    from data_part3 import questions_3
    questions = questions_1 + questions_2 + questions_3
except ImportError:
    st.error("⚠️ يرجى التأكد من وجود ملفات البيانات (data_part1.py, data_part2.py, data_part3.py) في نفس المجلد.")
    st.stop()

# إعدادات الصفحة
st.set_page_config(page_title="اختبار قانون العمل الأردني (100%)", layout="centered")
st.title("📝 اختبار شامل في قانون العمل الأردني (526 سؤال)")
st.markdown("تغطية 100% لنصوص قانون العمل رقم 8 لسنة 1996 وقانون العمل المهني رقم 11 لسنة 2019.")

# تهيئة حالة الجلسة (Session State)
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))

# التحقق من انتهاء الأسئلة
if st.session_state.index >= len(st.session_state.shuffled_questions):
    st.balloons()
    st.success("🎉 لقد أكملت الاختبار بنجاح!")
    st.write(f"**نتيجتك النهائية:** {st.session_state.score} من {len(st.session_state.shuffled_questions)}")
    if st.button("إعادة الاختبار من البداية 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # عرض السؤال الحالي
    current_q = st.session_state.shuffled_questions[st.session_state.index]
    st.progress((st.session_state.index + 1) / len(st.session_state.shuffled_questions))
    st.write(f"**السؤال {st.session_state.index + 1} من {len(st.session_state.shuffled_questions)}**")
    
    st.write(f"**{current_q['q']}**")
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