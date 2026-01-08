import streamlit as st
import requests
import os

API_KEY = st.secrets["CHATBOT_API_KEY"] 
MODEL = "mistralai/mistral-7b-instruct"

SYSTEM_PROMPT = (
    "Bạn là một chuyên gia kinh tế và kinh doanh có 10 năm kinh nghiệm. "
    "Hãy trả lời ngắn gọn, rõ ràng, dùng ví dụ thực tế (quán cà phê, startup, v.v.). "
    "Không bịa thông tin. Nếu không biết, hãy nói 'Tôi không chắc'."
)

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://yourname.streamlit.app", 
                "X-Title": "Business Expert Chatbot"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Lỗi API ({response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

# giao diện
st.set_page_config(page_title="CHUYÊN GIA KINH DOANH AI", page_icon="💼")
st.title("Chuyên Gia Kinh Doanh AI")
st.caption("Hỏi bất kỳ điều gì về kinh tế, tài chính, khởi nghiệp...")

# lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# hiện thị lịch sử chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# xử lý input
if prompt := st.chat_input("Ví dụ: 'Làm thế nào để tính điểm hòa vốn?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Đang suy nghĩ..."):
        reply = ask_ai(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.chat_message("assistant").write(reply)



