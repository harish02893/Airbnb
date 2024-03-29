import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis ", page_icon=":bar_chart:", layout="wide")


import streamlit as st

# Display the title with the Airbnb icon using Markdown syntax
st.markdown("<h1 style='text-align: center;'><img src='https://logodownload.org/wp-content/uploads/2016/10/airbnb-logo-0.png' alt='Airbnb Icon' style='vertical-align: middle;' width='120' height='120'> AirBnb-Analysis</h1>", unsafe_allow_html=True)

def app_bg():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://wallpapercave.com/wp/wp8268600.jpg");
                        background-size: cover}}
                     </style>""",unsafe_allow_html=True)
app_bg()


#st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# with st.headbar:
SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data", "Contact"],
    icons=["house", "bar-chart", "at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})

#----------------Home----------------------#

if SELECT == "Home":

 st.header('Airbnb Analysis')
 st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
 st.subheader('Skills take away From This Project:')
 st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
 st.subheader('Domain:')
 st.subheader('Travel Industry, Property management and Tourism')

if SELECT == "Explore Data":
 fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
 
 if fl is not None:
    df = pd.read_csv(fl, encoding="ISO-8859-1")
 else:
    st.warning("Please upload a file.")

 st.sidebar.header("Choose your filter: ")

if 'df' in locals():
 # Create for neighbourhood_group
 neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
 if not neighbourhood_group:
     df2 = df.copy()
 else:
     df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

 # Create for neighbourhood
 neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
 if not neighbourhood:
     df3 = df2.copy()
 else:
     df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

 # Filter the data based on neighbourhood_group, neighbourhood

 if not neighbourhood_group and not neighbourhood:
     filtered_df = df
 elif not neighbourhood:
     filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
 elif not neighbourhood_group:
     filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
 elif neighbourhood:
     filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
 elif neighbourhood_group:
     filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
 elif neighbourhood_group and neighbourhood:
     filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
 else:
     filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

 room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

 col1, col2 = st.columns(2)
 with col1:
    st.subheader("room_type_ViewData")
    fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

 with col2:
    st.subheader("neighbourhood_group_ViewData")
    fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
    fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

 cl1, cl2 = st.columns((2))
 with cl1:
    with st.expander("room_type wise price"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 with cl2:
    with st.expander("neighbourhood_group wise price"):
        neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
        st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
        csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 # Create a scatter plot
 data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
 data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
 st.plotly_chart(data1, use_container_width=True)

 with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
     st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

 # Download orginal DataSet
 csv = df.to_csv(index=False).encode('utf-8')
 st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

 import plotly.figure_factory as ff

 st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
 with st.expander("Summary_Table"):
    df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

 # map function for room_type

# If your DataFrame has columns 'Latitude' and 'Longitude':
 st.subheader("Airbnb Analysis in Map view")
 df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

 st.map(df)

# ----------------------Contact---------------#

if SELECT == "Contact":
    Name = (f'{"Name :"}  {"Kesavan sekar"}')
    mail = (f'{"Mail :"}  {"harishu02893@gmail.com"}')
    social_media = {
        "GITHUB": "https://github.com/harish02893",
        "LINKEDIN": "https://www.linkedin.com/in/kesavan-sekar-2aaa3325b/"}

    col1, col2 = st.columns(2)
    col1.image(Image.open("D:\\air bnb\\New folder\\q.jpg"), width=500)

    with col2:
        st.header('Airbnb Analysis')
        st.subheader(
            "This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        st.write("---")
        st.subheader(Name)
        st.subheader(mail)

    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")
        
import streamlit as st

def main():
    #st.title("Kesavan sekar DT1819")

    # Define image URLs
    images = [
        "https://a0.muscache.com/im/pictures/ddee2102-9257-43e2-bbdc-2d576f9abd45.jpg?im_w=1200",
        "https://a0.muscache.com/im/pictures/0dc6d460-c22d-489f-813b-48edbe902465.jpg?im_w=720",
        "https://a0.muscache.com/im/pictures/6ba72c1c-9fb0-48d6-b3ed-5f7823457a39.jpg?im_w=720",
        "https://a0.muscache.com/im/pictures/29b26141-72e6-4e39-9969-ad8b8c0deeb3.jpg?im_w=720",
        "https://a0.muscache.com/im/pictures/97ce1fa6-e2bf-42fa-b919-82d99d33cc6f.jpg?im_w=720",
        "https://tse2.mm.bing.net/th?id=OIP.AWLv6Dhr9E3r0zH7jdjIrgHaEK&pid=Api&P=0&h=220",
        "https://a0.muscache.com/im/pictures/ddee2102-9257-43e2-bbdc-2d576f9abd45.jpg?im_w=1200",
        "https://a0.muscache.com/im/pictures/0dc6d460-c22d-489f-813b-48edbe902465.jpg?im_w=720",
        "https://a0.muscache.com/im/pictures/6ba72c1c-9fb0-48d6-b3ed-5f7823457a39.jpg?im_w=720",
        "https://a0.muscache.com/im/pictures/29b26141-72e6-4e39-9969-ad8b8c0deeb3.jpg?im_w=720",
        "https://a0.muscache.com/im/pictures/97ce1fa6-e2bf-42fa-b919-82d99d33cc6f.jpg?im_w=720",
        "https://tse2.mm.bing.net/th?id=OIP.AWLv6Dhr9E3r0zH7jdjIrgHaEK&pid=Api&P=0&h=220",

    ]

    # Create HTML for scrolling images
    html = """
    <style>
    #footer {
        width: 100%;
        overflow: hidden;
        position: fixed;
        bottom: 0;
        background-color: #f1f1f1;
        white-space: nowrap;
        height: 100px; 
    }

    .scrolling-wrapper {
        animation: scroll 30s linear infinite;
    }

    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .image-wrapper {
        display: inline-block;
        margin: 0 20px;
    }

    .image-wrapper img {
        width: 150px; /* Set width of image */
        height: auto; /* Maintain aspect ratio */
    }
    </style>

    <div id="footer">
        <div class="scrolling-wrapper">
            """
    for image in images:
        html += f'<div class="image-wrapper"><img src="{image}" alt="image"></div>'
    html += """
        </div>
    </div>
    """

    # Display scrolling images using st.markdown
    st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
