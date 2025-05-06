import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from helper.query_building import create_query
import requests
import time
import plotly.express as px

hf_token = st.secrets["HUGGINGFACE_API_TOKEN"]
API_URL = st.secrets["API_URL"]
model_id = st.secrets["MODEL_ID"]

headers = {
    "Authorization": "Bearer "+hf_token
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def type_text(text, delay=0.05):
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(typed_text)
        time.sleep(delay)

def type_text_multi(tab_placeholders, texts, delay=0.01):
    typed_texts = [""] * len(texts)
    max_len = max(len(t) for t in texts)

    for i in range(max_len):
        for j in range(len(texts)):
            if i < len(texts[j]):
                typed_texts[j] += texts[j][i]
                tab_placeholders[j].markdown(typed_texts[j])
        time.sleep(delay)

def loading_spinner_with_gif(gif_url="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif"):
    # Display loading GIF and message
    gif_placeholder = st.empty()
    with gif_placeholder.container():
        st.markdown(f"""
        <div style="text-align: center;">
            <br></br>
            <img src="{gif_url}" width="60" style="background: transparent;">
            <p style="font-size: 1.2em;">LOADING</p>
        </div>
        """, unsafe_allow_html=True)
    return gif_placeholder

# def task_query_for_branding(sample_query):
#     time.sleep(2)


#     # Placeholder for the task
#     return "Branding Task Completed"






# if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
#     st.warning("⚠️ Please set your Hugging Face API token as the environment variable `HUGGINGFACEHUB_API_TOKEN`.")
#     st.stop()


# # Define prompt template
# prompt_template = PromptTemplate(
#     input_variables=["chat_history", "input"],
#     template="""
# You are a seasoned digital marketing strategist who provides expert advice on SEO, advertising, social media, and analytics.

# {chat_history}
# User: {input}
# Expert:"""
# )


st.set_page_config(page_title="Marketing Strategy Assistant", page_icon="📊", layout="wide")
st.title("📊 Marketing Strategy Dashboard")

# Sidebar

uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

vertical = st.sidebar.selectbox("Select Vertical", ["FMCG", "BFSI", "Automobile","QSR","Lifestyle","Healthcare","eCommerce","Real Estate","Education"])
month = st.sidebar.selectbox("Select Month", ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])
year = st.sidebar.selectbox("Select Year", ["2023", "2024", "2025"])
campaign_type = st.sidebar.selectbox("Select Campaign Type", ["Branding", "Performance", "Branding and Performance"])
analyze_button = st.sidebar.button("📈 Analyze", key="submit_button")

if uploaded_file and vertical and month and year:
    overall_performance = pd.read_excel(uploaded_file, sheet_name="overall_performance")
    summary = pd.read_excel(uploaded_file, sheet_name="summary")
    ctr = overall_performance["ctr"].values[0]
    conv_rate = overall_performance["conv_rate"].values[0]
    roas = overall_performance["roas"].values[0]
    if analyze_button:
        col1, col2, col3 = st.columns(3)
        col1.metric("CTR", str(ctr), " %")
        col2.metric("Conversion Rate", str(conv_rate), " %")
        col3.metric("ROAS", str(roas))
        query_text = create_query(vertical, campaign_type, month, year, overall_performance, summary)
        # query_text_branding = create_query(vertical, "Branding", month, year, overall_performance, summary)
        # query_text_performance = create_query(vertical, "Performance", month, year, overall_performance, summary)
        # query_text_branding_and_performance = create_query(vertical, "Branding and Performance", month, year, overall_performance, summary)

        #query_all = [query_text_branding, query_text_performance, query_text_branding_and_performance]

        st.divider()

        tab1, tab2 = st.tabs(["Analysis", "Recommendations"])

        with tab1:
            st.markdown("<h3 style='font-size: 26px;'>📈 Graphical representation</h3>", unsafe_allow_html=True)
            #st.subheader("📈 Graphical representation")
            tab_graph1, tab_graph2, tab_graph3, tab_graph4, tab_graph5 = st.tabs(["Media Spend by Platform", "Media Spend by Ad type","Media Spend by Ad - Demand Side","Media Spend by Ad - Biddable","Media Spend by Ad - Social"])
            with tab_graph1:
                #st.subheader("💸 Media Spend by Platform")
                spend_by_platform = summary.groupby("platform")["media_cost"].sum().reset_index()

                fig1 = px.pie(
                spend_by_platform,
                names="platform",
                values="media_cost",
                title="Media Spend Distribution by Platform",
                color_discrete_sequence=px.colors.qualitative.Set3,
                #hole=0.4  # Makes it a donut chart (optional)
            )

                fig1.update_traces(textinfo="percent+label", pull=[0.05]*len(spend_by_platform))
                fig1.update_layout(showlegend=True,autosize=True)

                st.plotly_chart(fig1, use_container_width=True)
            
            with tab_graph2:
                #st.subheader("💸 Media Spend by Ad type")
                #summary["estimated_ctr"] = summary["estimated_ctr"].astype(str)
                #summary["estimated_ctr"] = pd.to_numeric(summary["estimated_ctr"], errors="coerce")
                spend_by_ad_type = summary.groupby("type")["media_cost"].sum().reset_index()

                fig2 = px.pie(
                spend_by_ad_type,
                names="type",
                values="media_cost",
                title="Media Spend Distribution by Ad type",
                color_discrete_sequence=px.colors.qualitative.Set3,
                #hole=0.4  # Makes it a donut chart (optional)
            )

                fig2.update_traces(textinfo="percent+label", pull=[0.05]*len(spend_by_ad_type))
                fig2.update_layout(showlegend=True,autosize=True)

                st.plotly_chart(fig2, use_container_width=True)

            with tab_graph3:
                #st.subheader("💸 Media Spend - Demand Side")
                #summary["estimated_ctr"] = summary["estimated_ctr"].astype(str)
                #summary["estimated_ctr"] = pd.to_numeric(summary["estimated_ctr"], errors="coerce")
                summary_demand_side = summary[summary["platform"]=="demand-side"]
                spend_by_ad_demand_side = summary_demand_side.groupby("ad_name")["media_cost"].sum().reset_index()

                fig3 = px.pie(
                spend_by_ad_demand_side,
                names="ad_name",
                values="media_cost",
                title="Media Spend Distribution by Ad - Demand Side",
                color_discrete_sequence=px.colors.qualitative.Set3,
                #hole=0.4  # Makes it a donut chart (optional)
            )

                fig3.update_traces(textinfo="percent+label", pull=[0.05]*len(spend_by_ad_demand_side))
                fig3.update_layout(showlegend=True,autosize=True)

                st.plotly_chart(fig3, use_container_width=True)

            with tab_graph4:
                #st.subheader("💸 Media Spend - Biddable")
                #summary["estimated_ctr"] = summary["estimated_ctr"].astype(str)
                #summary["estimated_ctr"] = pd.to_numeric(summary["estimated_ctr"], errors="coerce")
                summary_biddable = summary[summary["platform"]=="biddable"]
                spend_by_ad_biddable = summary_biddable.groupby("ad_name")["media_cost"].sum().reset_index()

                fig4 = px.pie(
                spend_by_ad_biddable,
                names="ad_name",
                values="media_cost",
                title="Media Spend Distribution by Ad - Biddble",
                color_discrete_sequence=px.colors.qualitative.Set3,
                #hole=0.4  # Makes it a donut chart (optional)
            )

                fig4.update_traces(textinfo="percent+label", pull=[0.05]*len(spend_by_ad_biddable))
                fig4.update_layout(showlegend=True,autosize=True)

                st.plotly_chart(fig4, use_container_width=True)

            with tab_graph5:
                #st.subheader("💸 Media Spend - Social")
                #summary["estimated_ctr"] = summary["estimated_ctr"].astype(str)
                #summary["estimated_ctr"] = pd.to_numeric(summary["estimated_ctr"], errors="coerce")
                summary_social = summary[summary["platform"]=="social"]
                spend_by_ad_social = summary_social.groupby("ad_name")["media_cost"].sum().reset_index()

                fig5 = px.pie(
                spend_by_ad_social,
                names="ad_name",
                values="media_cost",
                title="Media Spend Distribution by Ad - Social",
                color_discrete_sequence=px.colors.qualitative.Set3,
                #hole=0.4  # Makes it a donut chart (optional)
            )

                fig5.update_traces(textinfo="percent+label", pull=[0.05]*len(spend_by_ad_social))
                fig5.update_layout(showlegend=True,autosize=True)

                st.plotly_chart(fig5, use_container_width=True)


        with tab2:
            st.markdown("<h3 style='font-size: 26px;'>💬 Future Recommendation</h3>", unsafe_allow_html=True)
            #st.subheader("💬 Future Recommendation for different campaigns")
            #tab3 = st.tabs(["Branding", "Performance", "Branding + Performance"])

            #with tab3:
            spinner = loading_spinner_with_gif(
        gif_url="https://media.tenor.com/WX_LDjYUrMsAAAAj/loading.gif"  # Choose any large GIF
    )
            placeholder1 = st.empty()
            #with st.spinner("Analyzing..."):
            response = query({
            "messages": [
                {
                    "role": "user",
                    "content": query_text
                }
            ],
            "model": model_id
            })
            spinner.empty()
                #time.sleep(2)
            response_text = response["choices"][0]["message"]["content"].strip()
            type_text(response_text, delay=0.01)
            
#             with tab4:
#                 placeholder2 = st.empty()
#                 # with st.spinner("Analyzing..."):
#                 #     response = query({
#                 #     "messages": [
#                 #         {
#                 #             "role": "user",
#                 #             "content": query_text_performance
#                 #         }
#                 #     ],
#                 #     "model": "Qwen/Qwen2.5-Coder-32B-Instruct"
#                 #     })
#                 #     time.sleep(2)
#                 # response_text_performance = response["choices"][0]["message"]["content"].strip()
#                 # #type_text(response_text_performance, delay=0.01)
#                 # #type_text(query_text_performance, delay=0.01)

#             with tab5:
#                 placeholder3 = st.empty()
#                 # with st.spinner("Analyzing..."):
#                 #     response = query({
#                 #     "messages": [
#                 #         {
#                 #             "role": "user",
#                 #             "content": query_text_branding_and_performance
#                 #         }
#                 #     ],
#                 #     "model": "Qwen/Qwen2.5-Coder-32B-Instruct"
#                 #     })
#                 #     time.sleep(2)
#                 # response_text_branding_and_performance = response["choices"][0]["message"]["content"].strip()
#                 # #type_text(response_text_branding_and_performance, delay=0.01)
#                 # #type_text(query_text_branding_and_performance, delay=0.01)
#             # response_text_all = [response_text_branding, response_text_performance, response_text_branding_and_performance]
#             # type_text_multi([placeholder1, placeholder2, placeholder3], response_text_all)

# # # Strategy Generation
# # if st.button("🧠 Generate Marketing Strategy"):
# #     #if df is not None:
# #     #try:
# #     # Prepare the prompt based on uploaded data
# #     #query_text = create_query(vertical, month, year, overall_performance, summary)
# #     file_path = "digital marketing prompt.txt"
# #     with open(file_path, 'r', encoding='utf-8') as file:
# #       query_text = file.read()
# #     with st.spinner("Analyzing..."):
# #         response = query({
# # "messages": [
# #     {
# #         "role": "user",
# #         "content": query_text
# #     }
# # ],
# # "model": "Qwen/Qwen2.5-Coder-32B-Instruct"
# # #"model": "accounts/fireworks/models/qwen3-30b-a3b"
# # })
# #         # response = conversation.predict(input=query)
# #         #response = llm.invoke(query)
# #     response_text = response["choices"][0]["message"]["content"].strip()
# #     type_text(response_text, delay=0.03)
# #     #st.write(response["choices"][0]["message"]["content"])

# #     # with st.expander("📜 Conversation History"):
# #     #     st.text(memory.buffer)
# #     # summary = df.describe(include='all').to_string()
# #     # prompt = (
# #     #     f"The performance data for {brand} in {month} {year} is as follows:\n\n"
# #     #     f"{summary}\n\n"
# #     #     "Based on the above metrics, suggest a marketing strategy to improve CTR, Conversion Rate, and ROAS."
# #     # )

# #     # with st.spinner("Analyzing..."):
# #     #     response = openai.ChatCompletion.create(
# #     #         model="gpt-3.5-turbo",
# #     #         messages=[
# #     #             {"role": "system", "content": "You are a marketing strategist."},
# #     #             {"role": "user", "content": prompt}
# #     #         ]
# #     #     )
# #     #     suggestion = response.choices[0].message.content.strip()
# #     #     st.subheader("📋 Suggested Strategy")
# #     #     st.write(suggestion)

# #     # except Exception as e:
# #     #     st.error(f"Error generating strategy: {e}")
# #     # else:
# #     #     st.warning("Upload an Excel file first.")