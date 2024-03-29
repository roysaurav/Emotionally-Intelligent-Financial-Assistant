import streamlit as st
import pandas as pd
import datetime
import cohere
import plotly.graph_objects as go
import textwrap


st.set_page_config( layout="wide")
last_quater_loss = st.sidebar.number_input("Last Quater Loss (%)", value = 15)
with st.sidebar.expander("Portfolio Assumption"):

  starting_portfolio_value = st.number_input("Portfolio Value At Start", value=100000)
  Average_Expected_return = st.number_input("Average Yearly Expected Return (%)", value = 8)



# get the current date
today = datetime.date.today()

# create a date range from 2021-01-01 to the current date with monthly frequency
dates = pd.date_range(start='2016-01-01', end=today, freq='Q')
yrs = int(len(dates)/4)
df = pd.DataFrame({"Date":dates})
df["Portfolio"] = starting_portfolio_value*((1+Average_Expected_return/400)**df.index)
df["Portfolio"].iloc[-1] = df["Portfolio"].iloc[-2]*(1-last_quater_loss/100)
st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
        text-align: center;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: center;
           vertical-align: middle;
        } 
    </style>
    """,unsafe_allow_html=True
)

st.title("Financial Assistant AI Helper")
intro = '''
Do you want to save time and effort on creating (copy pasting graphs) and updating presentations?

AIFInCon is a smart tool that can do it for you.

<b>See here how AIFInCon can assist a financial advisor whose client’s portfolio has declined. 
AIFInCon interpreted graphs, generated talking points, 
and creates powerpoint slides automatically saving hours of time.</b>
'''
st.write(intro, unsafe_allow_html=True)
col1, col2 = st.columns([0.7,0.3])

# display the dataframe
fig = df.plot(kind="line",x="Date",y="Portfolio" ,backend="plotly")



with col1:
  st.subheader("Portoflio Performance")

  st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def getting_answers(yrs,last_quater_loss ):
# ToDo :- get key as environment variable
  co = cohere.Client(st.secrets["COHERE_KEY"])

  response = co.generate(
    prompt=f'''My clients portfolio has worked well for the last {yrs} years. During last quater it took a hit of {last_quater_loss}%. My emotional client is very worried about his future. Please explain my client the situtaion in 50 words.
    ''',
  )
  return response

with col2:

  response = getting_answers(yrs,last_quater_loss )
  
  ans = response[0]
  client_output = ans.split("\n\n")
  start_div = ''''''
  st.subheader("Poor Performance Explaination")
  centering_text = '''
      <style>
      .container {
        display: flex;
        justify-content: center; 
        align-items: center;
      }
      .child {
        width: 200px;
        height: 200px;
      }
      </style>
      <br></br>
      <div class="container">
        <div class="child">
    ''' + client_output[0] + "</div></div>"
  st.write(centering_text , unsafe_allow_html=True)

  #st.plotly_chart(fig, use_container_width=True)



st.subheader("Additional Things to Consider")
for i in range(1, len(client_output)-1):
  st.write(f"<b>{i}.</b> " + client_output[i], unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])

with col2:
  if st.button("Click Here for PowerPoint Format Download", type="primary"):
    st.write('''<p style="font-size: 25px; text-align: center;"><b><a href="https://forms.office.com/r/TWmvm6VMp5"; style="color: green";> Contact us for enabling this feature</a></b> </p>''',unsafe_allow_html=True)
  else:
    st.write('''<p style="font-size: 25px; text-align: center;"><b><a href="https://forms.office.com/r/TWmvm6VMp5" > Contact us for more information</a></b> </p>''',unsafe_allow_html=True)
Discliamer = '''
<p style="font-size: 12px; color: lightgrey;">
This site is for information and entertainment purposes only. The owner of this site is not an investment advisor, financial planner, nor a legal or tax professional. The articles and content on this site are of a general informational nature only and should not be relied upon for individual circumstances. The content and opinions expressed on this site are provided by the authors of this site and are theirs alone. Said content and opinions are not provided by any third party mentioned on this site and have not been reviewed, approved, or otherwise endorsed by any such third parties.
</p>
'''
st.write(Discliamer, unsafe_allow_html=True)