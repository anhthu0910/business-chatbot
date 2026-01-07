import streamlit as st
import requests
import os

# === CẤU HÌNH ===
# Streamlit sẽ đọc API key từ biến môi trường (an toàn hơn khi deploy)
API_KEY = st.secrets["CHATBOT_API_KEY"]  # ← sẽ cấu hình sau
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
                "HTTP-Referer": "https://yourname.streamlit.app",  # thay bằng link của bạn sau
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

# === GIAO DIỆN STREAMLIT ===
st.set_page_config(page_title="Chuyên Gia Kinh Doanh AI", page_icon="💼")
st.title("💼 Chuyên Gia Kinh Doanh AI")
st.caption("Hỏi bất kỳ điều gì về kinh tế, tài chính, khởi nghiệp...")

# Lưu lịch sử chat trong session
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Hiển thị lịch sử
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Xử lý input
if prompt := st.chat_input("Ví dụ: 'Làm sao tính điểm hòa vốn?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Chuyên gia đang suy nghĩ..."):
        reply = ask_ai(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)