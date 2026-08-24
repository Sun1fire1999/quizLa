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
st.set_page_config(page_title="منصة الحفظ الذكي لقانون العمل", layout="centered")
st.title("⚡ منصة الحفظ والاختبار الذكي لقانون العمل")
st.markdown("اختر الموضوع، ثم اختر وضع الحفظ أو الاختبار. سيتم حفظ أخطائك تلقائياً لمراجعتها.")

# --- قائمة الفئات بالترتيب القانوني ---
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

def get_topic_order(topic):
    try:
        return ORDERED_TOPICS.index(topic)
    except ValueError:
        return 999

SORTED_QUESTIONS = sorted(questions, key=lambda q: get_topic_order(q.get('topic', '')))

# --- استخراج المواضيع المتاحة ---
all_topics = sorted(list(set(q.get('topic', 'عام') for q in SORTED_QUESTIONS)))
all_topics.insert(0, "جميع المواضيع")

# --- الشريط الجانبي: الإعدادات ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    selected_topic = st.selectbox("اختر الفئة:", all_topics)

    if selected_topic == "جميع المواضيع":
        filtered_questions = SORTED_QUESTIONS
    else:
        filtered_questions = [q for q in SORTED_QUESTIONS if q.get('topic', '') == selected_topic]

    st.divider()
    
    # وضع التدريب
    mode = st.radio("وضع التدريب:", ["📖 وضع الحفظ", "📝 وضع الاختبار"])
    
    st.divider()
    st.subheader("📊 إحصائياتك")
    if "mistakes" not in st.session_state:
        st.session_state.mistakes = []
    
    st.write(f"**عدد الأخطاء:** {len(st.session_state.mistakes)}")
    if len(st.session_state.mistakes) > 0:
        if st.button("🔄 مراجعة الأخطاء (إعادة الحل)"):
            # إعادة تعيين الأسئلة لتشمل الأخطاء فقط
            pass  # سنتعامل معها لاحقاً في الكود

# --- تهيئة حالة الجلسة ---
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "reveal" not in st.session_state:
    st.session_state.reveal = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None
if "mistakes" not in st.session_state:
    st.session_state.mistakes = []

# التأكد من أن الفهرس صحيح
if len(filtered_questions) > 0:
    if st.session_state.current_index >= len(filtered_questions):
        st.session_state.current_index = 0

    current_q = filtered_questions[st.session_state.current_index]

    # عرض تقدم
    st.progress((st.session_state.current_index + 1) / len(filtered_questions))
    st.write(f"**الموضوع:** {selected_topic}")
    st.write(f"**السؤال {st.session_state.current_index + 1} من {len(filtered_questions)}**")

    # ===== وضع الحفظ (الاستذكار) =====
    if mode == "📖 وضع الحفظ":
        st.info(f"**{current_q['q']}**")
        
        if st.session_state.reveal:
            # عرض النص الكامل للمادة
            if current_q.get('e'):
                st.success(f"📜 **نص المادة:**\n\n{current_q['e']}")
            else:
                st.warning("لا يوجد نص مادة في البيانات لهذا السؤال. تأكد من تعبئة الحقل 'e'.")
            
            if st.button("السؤال التالي ➡️"):
                st.session_state.current_index += 1
                st.session_state.reveal = False
                st.rerun()
        else:
            if st.button("👁️ إظهار الإجابة والنص"):
                st.session_state.reveal = True
                st.rerun()
    
    # ===== وضع الاختبار =====
    elif mode == "📝 وضع الاختبار":
        st.write(f"**{current_q['q']}**")
        
        # عرض الخيارات بترتيبها الثابت
        user_choice = st.radio(
            "اختر الإجابة الصحيحة:",
            current_q['op'],
            key=f"radio_{st.session_state.current_index}",
            index=None  # لا يوجد خيار محدد مسبقاً
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ السابق", disabled=(st.session_state.current_index == 0)):
                st.session_state.current_index -= 1
                st.session_state.answered = False
                st.session_state.reveal = False
                st.rerun()
        
        with col2:
            if st.button("✅ تأكيد الإجابة"):
                st.session_state.answered = True
                st.session_state.user_choice = user_choice
                if user_choice == current_q['a']:
                    st.session_state.score += 1
                else:
                    # حفظ الخطأ في قائمة الأخطاء
                    st.session_state.mistakes.append(current_q)
                st.rerun()
        
        with col3:
            if st.button("التالي ➡️", disabled=(st.session_state.current_index == len(filtered_questions) - 1)):
                st.session_state.current_index += 1
                st.session_state.answered = False
                st.session_state.reveal = False
                st.rerun()

        # عرض نتيجة التصحيح ونص المادة
        if st.session_state.answered:
            st.divider()
            if st.session_state.user_choice == current_q['a']:
                st.success("🎉 إجابة صحيحة!")
            else:
                st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة هي: {current_q['a']}")
                st.warning("تمت إضافة هذا السؤال إلى مجلد الأخطاء.")
            
            if current_q.get('e'):
                st.info(f"📜 **نص المادة:**\n\n{current_q['e']}")
            else:
                st.info("لا يوجد نص مادة مرفق.")

    # ===== نهاية الاختبار =====
    if st.session_state.current_index == len(filtered_questions) - 1 and st.session_state.answered:
        st.divider()
        st.subheader("🏁 نتيجة الاختبار النهائية")
        st.write(f"**النتيجة:** {st.session_state.score} من {len(filtered_questions)}")
        if len(filtered_questions) > 0:
            pct = (st.session_state.score / len(filtered_questions)) * 100
            st.write(f"**نسبة الإتقان:** {pct:.1f}%")
        
        if len(st.session_state.mistakes) > 0:
            st.warning(f"⚠️ لديك **{len(st.session_state.mistakes)}** سؤالاً خاطئاً.")
            if st.button("🔁 إعادة حل الأخطاء"):
                # عرض الأسئلة الخاطئة فقط
                # سنقوم بتحديث state ليدخل في وضع مراجعة الأخطاء
                st.session_state.filtered_questions = st.session_state.mistakes
                st.session_state.current_index = 0
                st.session_state.mistakes = []
                st.session_state.answered = False
                st.rerun()

# عرض زر إعادة الاختبار
with st.sidebar:
    if st.button("🔄 إعادة من الصفر"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()