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
st.set_page_config(page_title="اختبار قانون العمل الأردني (Modules)", layout="centered")
st.title("📚 اختبار قانون العمل الأردني - حسب المواضيع")
st.markdown("اختر الموضوع الذي تريد التدرب عليه، واختبر معرفتك في كل فرع على حدة.")

# --- استخراج قائمة المواضيع الفريدة من البيانات ---
all_topics = sorted(list(set([q.get('topic', 'مواضيع عامة') for q in questions])))
all_topics.insert(0, "☑️ الكل (جميع المواضيع)") # إضافة خيار الاختبار الشامل

# --- عرض قائمة اختيار الموضوع ---
selected_topic = st.selectbox("اختر الموضوع الذي تريد التدرب عليه:", all_topics)

# --- تصفية الأسئلة حسب الموضوع المختار ---
if selected_topic == "☑️ الكل (جميع المواضيع)":
    filtered_questions = questions
else:
    filtered_questions = [q for q in questions if q.get('topic', 'مواضيع عامة') == selected_topic]

# --- التحقق من وجود أسئلة في الموضوع المختار ---
if len(filtered_questions) == 0:
    st.warning("لا توجد أسئلة في هذا الموضوع حالياً. يرجى إضافة وسوم (topic) للأسئلة في ملفات البيانات.")
    st.stop()

# --- تهيئة حالة الجلسة (Session State) ---
# إعادة التعيين إذا تغير الموضوع
if "current_topic" not in st.session_state or st.session_state.current_topic != selected_topic:
    st.session_state.current_topic = selected_topic
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.submitted = False
    st.session_state.shuffled_questions = random.sample(filtered_questions, len(filtered_questions))

# التحقق من انتهاء الأسئلة في هذا الموضوع
if st.session_state.index >= len(st.session_state.shuffled_questions):
    st.balloons()
    st.success(f"🎉 لقد أكملت اختبار موضوع '{selected_topic}' بنجاح!")
    
    # عرض النتيجة الخاصة بهذا الموضوع فقط
    total_q = len(st.session_state.shuffled_questions)
    st.write(f"**نتيجتك في هذا القسم:** {st.session_state.score} من {total_q}")
    
    # حساب النسبة المئوية
    if total_q > 0:
        percentage = (st.session_state.score / total_q) * 100
        st.write(f"**نسبة الإتقان:** {percentage:.1f}%")
    
    if st.button("🔄 إعادة اختبار هذا الموضوع"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # عرض السؤال الحالي
    current_q = st.session_state.shuffled_questions[st.session_state.index]
    total_q = len(st.session_state.shuffled_questions)
    st.progress((st.session_state.index + 1) / total_q)
    st.write(f"**السؤال {st.session_state.index + 1} من {total_q}**")
    st.write(f"**{current_q['q']}**")

    # خلط الخيارات عشوائياً (حل مشكلة توقع الإجابة)
    shuffled_options = current_q['op'].copy()
    random.shuffle(shuffled_options)

    st.session_state.selected_option = st.radio(
        "اختر الإجابة الصحيحة:",
        shuffled_options,
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

# --- عرض ملخص النتيجة العامة في الشريط الجانبي ---
with st.sidebar:
    st.header("📊 إحصائياتك")
    st.write(f"**الموضوع الحالي:** {selected_topic}")
    if st.session_state.index > 0:
        st.write(f"**تقدمك في هذا القسم:** {st.session_state.index} / {len(st.session_state.shuffled_questions)}")
        st.write(f"**عدد الإجابات الصحيحة:** {st.session_state.score}")
        if len(st.session_state.shuffled_questions) > 0:
            percentage = (st.session_state.score / len(st.session_state.shuffled_questions)) * 100
            st.write(f"**نسبة الإتقان الحالية:** {percentage:.1f}%")
    else:
        st.write("لم تبدأ الاختبار بعد...")