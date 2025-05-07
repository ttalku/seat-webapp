import streamlit as st
import pandas as pd
import numpy as np
import random

st.title("📋 자리 배치 생성기")
st.write("이전 자리배치를 업로드하면 새로운 자리배치를 조건에 따라 생성합니다.")

uploaded_file = st.file_uploader("이전 자리 배치 파일 업로드 (pre_seat.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=None)
    st.write("📌 이전 자리배치:")
    st.dataframe(df)

    # 자리 정보
    rows, cols = df.shape
    available = [(r, c) for r in range(rows) for c in range(cols) if pd.notna(df.iat[r, c])]
    students = [int(df.iat[r, c]) for r, c in available]

    # 조건: 같은 줄(세로), 같은 행(가로)을 피하도록 시도
    max_attempts = 1000
    for attempt in range(max_attempts):
        new_positions = random.sample(available, len(students))
        fail_count = 0
        for (r1, c1), (r2, c2) in zip(available, new_positions):
            if r1 == r2 or c1 == c2:  # 같은 행 or 같은 열
                fail_count += 1
        if fail_count <= 5:  # 조건을 어느 정도 만족하면 채택
            break

    # 새 배치 만들기
    new_df = pd.DataFrame(index=range(rows), columns=range(cols))
    for (r, c), num in zip(new_positions, students):
        new_df.iat[r, c] = num

    st.write("✅ 새로 생성된 자리배치:")
    st.dataframe(new_df)

    # 다운로드용 Excel 파일 저장
    output_filename = "new_seat.xlsx"
    new_df.to_excel(output_filename, index=False, header=False)
    with open(output_filename, "rb") as f:
        st.download_button("📥 새 자리배치 다운로드", f, file_name=output_filename)
