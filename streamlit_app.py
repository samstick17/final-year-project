import streamlit as st
import preprocessor1
import helper
import matplotlib.pyplot as plt
import pandas as pd

# import seaborn as sns

st.sidebar.title("ANALYZER FOR THE IMPACT OF SOCIAL MEDIA PLATFORMS ON INDIVIDUAL’S EMOTION")
st.sidebar.header("BY SAMUEL OJO JOHN (SCI18CSC142)")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("latin-1")
    # st.text(data)
    df = preprocessor1.preprocess(data)
    st.dataframe(df)

    # # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list = [user for user in user_list if user != 'group_notification']
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, r_positive, r_negative, r_neutral = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.write("Positive Messages")
            st.subheader(r_positive)
        with col3:
            st.write("Negative Messages")
            st.subheader(r_negative)
        with col4:
            st.write("Neutral Messages")
            st.subheader(r_neutral)

        num_media_messages = helper.media(df)
        col1, col2 = st.columns(2)

        with col1:
            st.write("Media Shared")
            st.subheader(num_media_messages)

        positive_message = df["positive"].sum()
        negative_message = df["negative"].sum()
        neutral_message = df["neutral"].sum() - df[df['message'] == '<Media omitted>\n'].shape[0]
        col1, col2 = st.columns(2)

        with col1:
            st.write("Bar chat visualization")
            sentiments = ["positive", "negative", "neutral"]
            values = [positive_message, negative_message, neutral_message]
            plt.bar(sentiments, values)
            plt.ylabel("Total value")
            st.pyplot()

        with col2:
            st.write("Pie Chart visuals")
            labels = ["Positive", "Negative", "Neutral"]
            sizes = [positive_message, negative_message, neutral_message]
            colors = ["green", "red", "yellow"]
            plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
            plt.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
            st.pyplot()

    df_wc = helper.create_wordcloud(selected_user, df)
    if df_wc is not None:
        # Display the word cloud using Matplotlib
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    else:
        st.write("No messages available for word cloud. Kindly change your time format to 24hrs before exporting uploaded .txt file")
