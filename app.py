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
st.set_page_config(page_title="اختبار قانون العمل الأردني (تدرج قانوني)", layout="centered")
st.title("📚 اختبار قانون العمل الأردني - تدريب متسلسل")
st.markdown("تم ترتيب المواضيع حسب تسلسل المواد في القانون. ابدأ بالتدرب من البداية وحتى النهاية.")

# --- الترتيب القانوني الثابت للمواضيع ---
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

# --- تصفية وترتيب المواضيع المتاحة بناءً على البيانات الموجودة ---
all_topics = set([q.get('topic', 'أحكام عامة وتعريفات (المواد 1-4)') for q in questions])
# نقوم بترتيب المواضيع المتاحة حسب القائمة القانونية الثابتة
available_topics = [topic for topic in ORDERED_TOPICS if topic in all_topics]

# إضافة خيار الاختبار الشامل في البداية
if len(available_topics) == 0:
    st.warning("⚠️ لم يتم العثور على مواضيع معرفة. تأكد من إضافة حقل 'topic' للأسئلة في ملفات البيانات.")
    available_topics = ["جميع الأسئلة"] # حماية من التعطل

topic_options = ["☑️ اختبار شامل (كل المواضيع)"] + available_topics

# --- تهيئة حالة الجلسة (Session State) ---
if "current_topic_index" not in st.session_state:
    st.session_state.current_topic_index = 0

# دالة للحصول على قائمة الأسئلة للموضوع الحالي
def get_questions_for_topic(topic):
    if topic == "☑️ اختبار شامل (كل المواضيع)":
        return questions
    return [q for q in questions if q.get('topic', 'أحكام عامة وتعريفات (المواد 1-4)') == topic]

# --- الشريط الجانبي للتنقل بين المواضيع ---
with st.sidebar:
    st.header("🧭 التنقل في القانون")
    
    # تحديث الفهرس بناءً على القائمة المنسدلة
    current_topic = st.selectbox(
        "الموضوع الحالي:",
        topic_options,
        index=st.session_state.current_topic_index
    )

    # أزرار التنقل للانتقال إلى الموضوع التالي أو السابق
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⏪ الموضوع السابق") and st.session_state.current_topic_index > 0:
            st.session_state.current_topic_index -= 1
            # إعادة تعيين الاختبار عند تغيير الموضوع
            for key in list(st.session_state.keys()):
                if key not in ["current_topic_index"]:
                    del st.session_state[key]
            st.rerun()
    with col_next:
        if st.button("الموضوع التالي ⏩") and st.session_state.current_topic_index < len(topic_options) - 1:
            st.session_state.current_topic_index += 1
            # إعادة تعيين الاختبار عند تغيير الموضوع
            for key in list(st.session_state.keys()):
                if key not in ["current_topic_index"]:
                    del st.session_state[key]
            st.rerun()

# --- تصفية الأسئلة حسب الموضوع المختار ---
filtered_questions = get_questions_for_topic(current_topic)

# --- التحقق من وجود أسئلة ---
if len(filtered_questions) == 0:
    st.warning("لا توجد أسئلة في هذا الموضوع حالياً.")
    st.stop()

# --- تهيئة حالة الاختبار ---
if "current_topic" not in st.session_state or st.session_state.current_topic != current_topic:
    st.session_state.current_topic = current_topic
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.submitted = False
    st.session_state.shuffled_questions = random.sample(filtered_questions, len(filtered_questions))

# التحقق من انتهاء الأسئلة في هذا الموضوع
if st.session_state.index >= len(st.session_state.shuffled_questions):
    st.balloons()
    st.success(f"🎉 لقد أكملت موضوع '{current_topic}' بنجاح!")
    total_q = len(st.session_state.shuffled_questions)
    st.write(f"**نتيجة هذا القسم:** {st.session_state.score} من {total_q}")
    if total_q > 0:
        percentage = (st.session_state.score / total_q) * 100
        st.write(f"**نسبة الإتقان:** {percentage:.1f}%")
    
    if st.button("🔄 إعادة اختبار هذا الموضوع"):
        for key in list(st.session_state.keys()):
            if key != "current_topic_index":
                del st.session_state[key]
        st.rerun()
else:
    # عرض السؤال الحالي
    current_q = st.session_state.shuffled_questions[st.session_state.index]
    total_q = len(st.session_state.shuffled_questions)
    st.progress((st.session_state.index + 1) / total_q)
    st.write(f"**السؤال {st.session_state.index + 1} من {total_q}**")
    st.write(f"**{current_q['q']}**")

    # خلط الخيارات
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