import streamlit as st 
import pandas as pd    
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots



class CollectUserInput():
    def __init__(self,df):
        self.df= df
#         self.months= months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

        self.year = ['1399','1400']
    def user_input(self):
        Customer_Num  = self.df['Customer Num'].unique()
        Customer_Num_selectbox = st.sidebar.selectbox( "Customer Number : ", Customer_Num )
        Year_slider = st.sidebar.selectbox("Year :",self.year,self.year.index('1400'))
        if Year_slider == '1399':
            self.months  = self.months[3:]
        elif Year_slider == '1400':
             self.months  = self.months[:9]

        Month_slider = st.sidebar.selectbox("Month :",self.months,self.months.index('آذر'))
        AVG_Time_slider = st.sidebar.slider("Hours :",0,23,(13,15))
        
        data = {
            'Customer': Customer_Num_selectbox,
            'Year' : Year_slider,
            'Month' : Month_slider,
            'Time' : AVG_Time_slider
                }
        features = pd.DataFrame(data)
        return features
           
    def user_input_all(self):
        Year_slider = st.sidebar.selectbox("Year :",self.year,self.year.index('1400'))
        if Year_slider == '1399':
            self.months  = self.months[3:]
        elif Year_slider == '1400':
             self.months  = self.months[:9]
        Month_slider = st.sidebar.selectbox("Month :",self.months,self.months.index('آذر'))
        AVG_Time_slider = st.sidebar.slider("Hours :",0,23,(13,15))
        
        data = {
            'Year' : Year_slider,
            'Month' : Month_slider,
            'Time' : AVG_Time_slider
                }
        features = pd.DataFrame(data)
        return features
    
    def histoplot_input(self):
        Customer_Num  = self.df['Customer Num'].unique()
        Customer_Num_selectbox = st.sidebar.selectbox( "Customer Number : ", Customer_Num )

        features =Customer_Num_selectbox
        return features

class Plot():
    def __init__(self,df,state):
        self.df= df
        self.df2= df
        self.state= state
        st.title('تحلیل مصرف برق مشترکین بهبهان')
#         self.months = ['None','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.months = ['None','فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

        self.yearmonths =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399', 'دی 1399','بهمن 1399',
                      'اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400', 'تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400',
                       'آبان 1400','آذر 1400', 'دی 1400']
        
#         self.yearmonths =['June 2020', 'July 2020', 'August 2020', 'September 2020', 'October 2020', 'November 2020', 'December 2020','January 2021', 'February 2021', 'March 2021', 'April 2021', 'May 2021', 'June 2021', 'July 2021', 'August 2021', 'September 2021', 'October 2021', 'November 2021', 'December 2021']
#         self.year = ['2020','2021']
#         self.nbins = {'January':31,'February':28, 'March':31,'April':30,'May':31,'June':30,'July':31,
#                      'August':31,'September':30,'October':31,'November':30,'December':31,}
        self.year = ['1399','1400']
        self.nbins = {'فروردین':31,'اردیبهشت':31, 'خرداد':31,'تیر':31,'مرداد':31,'شهریور':31,'مهر':30,'آبان':30,'آذر':30,'دی':30,'بهمن':30,'اسفند':30}

    def histogram_box_month_plot(self):
            
        user_input=CollectUserInput(self.df)
                
        if self.state == 0:
            user = user_input.user_input()
            data=self.df[self.df['Customer Num'] ==user['Customer'][0]]
        elif self.state==1:
            user = user_input.user_input_all()

            data=self.df

        df = data[data['Month']==self.months.index(user['Month'][0])]
        df = df[df['Year']==int(user['Year'][0])]
        data= data.iloc[:,7:]
        time1= user['Time'][0]+2
        time2= user['Time'][1]+2
        newdata= data[['Date','Month','Day','Total Avg. (KW)']]
        
        data= data.iloc[:,time1:time2]
        nbins = self.nbins[user['Month'][0]]

        # df = df[df['Year']==int(user['Year'][0])]
        sumdata = []
        for i in range(time1+7,time2):
            sumdata.append(df.iloc[:,i])
        # st.write(newdata,time1)
        # st.write(df.columns[time1+7:time2+7])
        # st.write("heloo", )

        # st.write(df.iloc[:,time1+7:time2+7])
        df["Total selcted Time"]=pd.DataFrame(df.iloc[:,time1+7:time2+7].sum(axis=1))

        fig5 = px.histogram(df, x='Day',y='Total selcted Time', nbins=nbins)
        st.write(f"Selected Time Chart  **{user['Year'][0]} {user['Month'][0]} from {time1-2}:00 to {time2-2}:00**")
        st.plotly_chart(fig5)

        newdata= pd.concat([newdata,data],axis=1)
        col = data.columns
        y_axis_val = st.selectbox('Select Y_Axis Vlaue', options= data.columns)


        t  = user['Time'][0]
        if user['Time'][0] == 0 and user['Time'][1] ==23: 
            y_axis_val= 'Total Avg. (KW)'
        fig1 = px.histogram(df, x='Day',y=y_axis_val,color ='Day', nbins=nbins)
        fig3 = px.line(df, x='Day',y=y_axis_val,)
        
        fig2 = px.box(df,x=y_axis_val) 
        fig4 = px.histogram(newdata, x='Date',y= y_axis_val)
        
        del newdata
        del data

        st.write('---')
        col = df.iloc[:,time1+7:time2+7].columns
        if user['Time'][0] == 0 and user['Time'][1] ==23:
            st.markdown(f"Daily average, days of  **{user['Year'][0]} {user['Month'][0]}**")

        else:
            st.markdown(f"Daily box data chart of **{user['Year'][0]} {user['Month'][0]} {y_axis_val}**")

        st.plotly_chart(fig1)
        st.plotly_chart(fig3)
        
        st.write('---')
        st.markdown(f"Daily box data chart of **{user['Year'][0]} {user['Month'][0]} {y_axis_val}**")

        st.plotly_chart(fig2)
        st.write('---')
        st.markdown(f"The chart of different months for data for subscriber in **{user['Year'][0]} {user['Month'][0]} {y_axis_val}**")

        # st.write('The chart of different months for ',col[0],"o'clock")
        st.plotly_chart(fig4)
      
    def histogram_box_plot(self):
        user_input=CollectUserInput(self.df)

        if self.state == 0:
            user = user_input.histoplot_input()
            data=self.df[self.df['Customer Num'] ==user]
        elif self.state==1:
            data=self.df

        
        
        data= data.iloc[:,7:]
        y_axis_val = st.selectbox('Select Y_Axis Vlaue', options= data.iloc[:,1:].columns)

        # y_axis_val = st.selectbox('Select Y_Axis Vlaue', options= data.iloc[:,1:].columns)
        data1 = pd.DataFrame(data.groupby(['Year','Month'])[y_axis_val].mean())
        data1['Months'] =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399', 'دی 1399','بهمن 1399',
                      'اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400', 'تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400',
                       'آبان 1400','آذر 1400']
        
        # the histogram and line plot for Date
        fig = px.histogram(data, x='Date', y= y_axis_val)
        
        fig1 = px.line(data, x="Date", y=y_axis_val)

        # the histogram and line plot for Months
        fig2 = px.histogram(data1, x='Months',color=y_axis_val,y=y_axis_val)#['darkred'])
        
        fig3 = px.line(data1, x="Months", y=y_axis_val)
        
        # the box plot for y_axis_val
        fig4 = px.box(data,x=y_axis_val) 

        # the 3d plot for model
        fig5 = go.Figure(data=[go.Mesh3d(z=data[y_axis_val],
                        y=data['Total Avg. (KW)'],
                        x=data['Date'],
                        opacity=0.5,color='rgba(244,23,100,0.6)')])
        fig5.update_layout(scene=dict(xaxis_showspikes=False,
                                    yaxis_showspikes=False))
        
        
        st.write("---")
        st.plotly_chart(fig)
        st.write("---")
        st.plotly_chart(fig1)
        st.write("---")
        st.plotly_chart(fig2)
        st.write("---")
        st.plotly_chart(fig3)
        st.write("---")
        st.plotly_chart(fig4)
        st.write("---")
        st.plotly_chart(fig5)
 
    def heatmap(self):
        user_input=CollectUserInput(self.df)
        time1= 0
        time2= 0
        if self.state == 0:
            user = user_input.user_input()
            data=self.df[self.df['Customer Num'] ==user['Customer'][0]]
            time1= user['Time'][0]+9
            time2= user['Time'][1]+9

        elif self.state==1:
            user = user_input.user_input_all()

            data=self.df
            time1= user['Time'][0]+9
            time2= user['Time'][1]+9
        data =  data[data['Year']==int(user['Year'][0])]
       
        ind=[]
        for i in user['Month']:
            ind.append(self.months.index(i)+1)
        fig =px.imshow(data.iloc[:,time1:time2].select_dtypes(include="number").corr(),text_auto=True,aspect="auto" )
        
        data1= data[data['Month'].isin(ind)]
        
        fig1 =px.imshow(data1.iloc[:,time1:time2].select_dtypes(include="number").corr(),text_auto=True,aspect="auto" )
        
        st.write('---')

        if self.state ==0 :
            st.markdown(f"Correlation heatmap diagram of **Annual** data for subscriber **Customer {user['Customer'][0]}  in {user['Year'][0]} from {time1-9}:00 to {time2-9}:00**")
            st.plotly_chart(fig)
            st.write('---')
            st.markdown(f"Correlation heatmap diagram of **Monthly** data for subscriber **Customer {user['Customer'][0]} in {user['Month'][0]} from {time1-9}:00 to {time2-9}:00**")
            st.plotly_chart(fig1)

        elif self.state == 1:
            st.markdown(f"Correlation heatmap diagram of **Annual** data for subscriber **in {user['Year'][0]} from {time1-9}:00 to {time2-9}:00**")
            st.plotly_chart(fig)
            st.write('---')
            st.markdown(f"Correlation heatmap diagram of **Monthly** data for subscriber **in {user['Month'][0]} from {time1-9}:00 to {time2-9}:00**")
            st.plotly_chart(fig1)



def read_data():
    df = pd.read_csv("Agricultural_Behbahan_onehours_Fa.csv")
    return df 
     
df= read_data()    
# df= df.iloc[:,:]
st.subheader('Select One 👇')
P_selectbox = st.selectbox('',['یک مشتری', 'همه مشتری ها'])

plots_selectbox = st.selectbox('',['Heatmap', 'نمودار ماهانه','نمودار سالانه'])
st.markdown("""---""")  
if P_selectbox=='همه مشتری ها':
    plot =Plot(df,1)

    if plots_selectbox == 'Heatmap':
        plot.heatmap()
        st.markdown("""---""")  
        
    elif plots_selectbox =='نمودار ماهانه':
        plot.histogram_box_month_plot()
        st.markdown("""---""")
        
    elif plots_selectbox =='نمودار سالانه':
        plot.histogram_box_plot()
        st.markdown("""---""")   

elif P_selectbox == 'یک مشتری':
    plot =Plot(df,0)
    
    if plots_selectbox == 'Heatmap':
        plot.heatmap()
        st.markdown("""---""")  
        
    elif plots_selectbox =='نمودار ماهانه':
        plot.histogram_box_month_plot()
        st.markdown("""---""")
        
    elif plots_selectbox =='نمودار سالانه':
        plot.histogram_box_plot()
        st.markdown("""---""")   


