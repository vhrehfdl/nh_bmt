import re
import base64
import streamlit as st
import pandas as pd


def extract_contexts(context_text):
    context_data = re.findall(r'\(context \d+\)= Title:.*?\n(.*?)(?=\(context \d+\)=|$)', context_text, re.S)
    return context_data


def remove_human_sections(context_text):
    if not isinstance(context_text, str):  # 문자열이 아닌 경우 처리
        return ""
    cleaned_text = re.sub(r'"""[\s\S]*?Human:.*?(?=\n\n|$)', '', context_text, flags=re.S)
    return cleaned_text


def download(dataframe):
    csv_data = dataframe.to_csv(index=False).encode("utf-8-sig")
    b64 = base64.b64encode(csv_data).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download</a>'
    st.markdown(href, unsafe_allow_html=True)


st.markdown("### Alli → NH BMT")
uploaded_file = st.file_uploader("GA Bulk 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    idx = []
    question = df["question"].tolist()
    generate_answer_prompt = df["generate_answer_prompt"].tolist()
    generated_answer = df["generated_answer"].tolist()
    target_answer = df["target_answer"].tolist()

    chunk1, chunk2, chunk3, chunk4, chunk5 = [], [], [], [], []
    for i in range(len(generate_answer_prompt)):
        idx.append(i + 1)
        extracted_contexts = extract_contexts(generate_answer_prompt[i])

        chunk1.append(remove_human_sections(extracted_contexts[0] if len(extracted_contexts) > 0 else None))
        chunk2.append(remove_human_sections(extracted_contexts[1] if len(extracted_contexts) > 1 else None))
        chunk3.append(remove_human_sections(extracted_contexts[2] if len(extracted_contexts) > 2 else None))
        chunk4.append(remove_human_sections(extracted_contexts[3] if len(extracted_contexts) > 3 else None))
        chunk5.append(remove_human_sections(extracted_contexts[4] if len(extracted_contexts) > 4 else None))

    new_df = pd.DataFrame({
        "순번": idx,
        "질문": question,
        "청크1": chunk1,
        "청크2": chunk2,
        "청크3": chunk3,
        "청크4": chunk4,
        "청크5": chunk5,
        "LLM 생성 답변": generated_answer,
        "모범답안": target_answer,
    })

    download(new_df)


for _ in range(5):
    st.write("")


st.markdown("### NH BMT → Alli")
# uploaded_file = st.file_uploader("제출용 파일을 업로드하세요", type=["csv"])
st.markdown("형식을 어떻게 변환해야 하는지 논믜 필요함")
