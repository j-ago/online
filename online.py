import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the questions from the Excel file

file_path = 'https://github.com/j-ago/online.git/20240806_アンバランス度質問シート_rawdata.xlsx'
df = pd.read_excel(file_path, sheet_name='体質バランス乱れ度')

# Map to hold the scores for Vata, Pitta, and Kapha
dosha_scores = {'Vata': 0, 'Pitta': 0, 'Kapha': 0}

# Define the maximum score per dosha
max_score = 40

# Instructions
st.title("アーユルベーダ診断アプリ")
st.write("以下の質問にお答えください。各質問に対して該当する項目を選んでください。")

# Function to calculate percentage and determine the stability status
def calculate_status(score, max_score):
    percentage = (score / max_score) * 100
    if percentage <= 20:
        return percentage, "安定している状態です。この状態を維持するように心がけてください。"
    elif percentage <= 40:
        return percentage, "比較的安定している状態です。乱れが多く出ないように心がけてください。"
    elif percentage <= 60:
        return percentage, "乱れが少し出ている状態です。安定化に向けて心がけてください。"
    elif percentage <= 80:
        return percentage, "乱れが多く出ている状態です。安定化に向けて積極的に対応してください。"
    else:
        return percentage, "とても乱れている状態です。改善に向けて迅速に対応してください。"

# User input form
options = [
    ("4: 当てはまる", 4),
    ("3: まあまあ当てはまる", 3),
    ("2: どちらともいえない", 2),
    ("1: あまり当てはまらない", 1),
    ("0: 当てはまらない", 0)
]

for index, row in df.iterrows():
    question = row['Unnamed: 0']
    st.markdown(f"**<span style='font-size:18px;'>{question}</span>**", unsafe_allow_html=True)
    score = st.radio('', options, format_func=lambda x: x[0], key=f'question_{index}')[1]
    
    # Assign the scores to Vata, Pitta, and Kapha based on the question index
    if index < 10:
        dosha_scores['Vata'] += score
    elif index < 20:
        dosha_scores['Pitta'] += score
    else:
        dosha_scores['Kapha'] += score

# Calculate and display results
if st.button('診断結果を見る'):
    for dosha, score in dosha_scores.items():
        percentage, status = calculate_status(score, max_score)
        st.write(f"{dosha} のスコア: {score} / {max_score} ({percentage:.2f}%)")
        st.write(status)
    
    # Create a pie chart for the results
    labels = dosha_scores.keys()
    sizes = dosha_scores.values()
    colors = ['#ff9999','#66b3ff','#99ff99']
    explode = (0.1, 0, 0)  # explode 1st slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)
