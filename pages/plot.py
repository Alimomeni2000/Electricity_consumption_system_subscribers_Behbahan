import streamlit as st 
import pandas as pd    
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re


class CollectUserInput():
    def __init__(self,df):
        self.df= df
#         self.months= months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        self.seasons= ['بهار','تابستان','پاییز','زمستان']
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
        self.months = ['None','فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        # self.seasons= ['بهار','تابستان','پاییز','زمستان']
        
        self.seasons = {1: 'بهار', 2: 'بهار', 3: 'بهار', 4: 'تابستان', 5: 'تابستان', 6: 'تابستان',
           7: 'پاییز', 8: 'پاییز', 9: 'پاییز', 10: 'زمستان', 11: 'زمستان', 12: 'زمستان'}
        self.yearseasons= ['1399 تابستان','1399 زمستان','1399 پاییز','1400 بهار','1400 تابستان','1400 پاییز']

        self.yearmonths =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399', 'دی 1399','بهمن 1399',
                      'اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400', 'تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400',
                       'آبان 1400','آذر 1400', 'دی 1400']
        
        self.customer2 =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
        
        self.customer44 =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399','بهمن 1399','اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400','تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
        
        self.customer33 =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399','اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400','تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
        
        self.customer16 =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399','دی 1399','بهمن 1399','اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400', 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
        
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
        # st.write(data)
        month_data= data.iloc[:,10:36].groupby(['Year','Month']).sum().sum(axis=1).reset_index()
        
        # st.write(month_data)
        
        month_data['Sum (KW)'] = pd.DataFrame(month_data.iloc[:,2])
        month_data= month_data.drop(month_data.columns[2],axis=1)
        month_data['Avg (KW)']= month_data['Sum (KW)']/25
        month_data = month_data.round(3)
        month_data[['Month']] = month_data[['Month']].astype(int)
        # st.write(month_data)
        if self.state == 0:
            if user['Customer'][0]==2:
                month_data['Months'] =self.customer2 
            elif user['Customer'][0]==44:
                datmonth_dataa1['Months'] =self.customer44 
            elif user['Customer'][0]==33:
                month_data['Months'] =self.customer33
            elif user['Customer'][0]==16:
                month_data['Months'] =self.customer16
            else:
                month_data['Months'] =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399','دی 1399','بهمن 1399','اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400','تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
        else: 
            month_data['Months'] =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399','دی 1399','بهمن 1399','اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400','تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
  
        fig6 = px.histogram(month_data, x='Months',y='Sum (KW)',color='Sum (KW)')
        fig7= px.histogram(month_data, x='Months',y='Avg (KW)',color='Avg (KW)')
        
        st.write("---")
        st.write('مجموع مصرف  در ماه های مختلف')
        st.plotly_chart(fig6)
        st.write("---")
        st.write('میانگین مصرف در ماه های مختلف')
        st.plotly_chart(fig7)
        Month=data.iloc[:,2:]

        
        df = data[data['Month']==self.months.index(user['Month'][0])]
        df = df[df['Year']==int(user['Year'][0])]
        data= data.iloc[:,7:]
        time1= user['Time'][0]+2
        time2= user['Time'][1]+2
        newdata= data[['Date','Month','Day','Total Avg. (KW)']]
        
        data= data.iloc[:,time1:time2]
        nbins = self.nbins[user['Month'][0]]

        sumdata = []
        for i in range(time1+7,time2):
            sumdata.append(df.iloc[:,i])
            
        
        df["Total selcted Time"]=pd.DataFrame(df.iloc[:,time1+7:time2+7].sum(axis=1))
        df= df.round(3)
        
        fig5 = px.histogram(df, x='Day',y='Total selcted Time',color='Day', nbins=nbins)
        st.write(f"مجموع مصرف **{user['Month'][0]} {user['Year'][0]}  از ساعت {time1-2}:00 تا {time2-2}:00**")
        st.plotly_chart(fig5)
        
        df["Sum (KW)"]= df.iloc[:,9:25+7].sum(axis=1)
        df["Avg (KW)"]= df['Sum (KW)']/23
        df= df.round(3)

        st.write('---')
    
        st.write(f"مجموع مصرف روزانه ماه  {user['Month'][0]}  سال {user['Year'][0]} ")
        fig5 = px.histogram(df, x='Day',y='Sum (KW)',color='Day',nbins=nbins)
        st.plotly_chart(fig5)
        
        st.write(f"میانگین مصرف روزانه ماه  {user['Month'][0]}  سال {user['Year'][0]} ")
        fig5 = px.histogram(df, x='Day',y='Avg (KW)',color='Day',nbins=nbins)
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
        time=re.findall(r'\d+', y_axis_val)
        # st.write(a[0])
        st.markdown(f"مصرف روزانه **{user['Year'][0]} {user['Month'][0]}  از ساعت {time[0]} تا {time[1]}**")

        st.plotly_chart(fig1)
        st.plotly_chart(fig3)
        
        st.write('---')
        st.markdown(f"نمودار باکس روزانه **{user['Year'][0]} {user['Month'][0]}  از ساعت {time[0]} تا {time[1]}**")

        st.plotly_chart(fig2)
        st.write('---')
        st.markdown(f"نمودار ماه های مختلف در  **{user['Year'][0]} {user['Month'][0]} از ساعت {time[0]} تا {time[1]}**")

        st.plotly_chart(fig4)
      
    def histogram_box_plot(self):
        user_input=CollectUserInput(self.df)
        user=0
        if self.state == 0:
            user = user_input.histoplot_input()
            data=self.df[self.df['Customer Num'] ==user]
        elif self.state==1:
            data=self.df
        data= data.iloc[:,7:]
        
        Season=data.iloc[:,2:]
        Season['Season'] = Season['Month'].map(self.seasons)
        Season_data = Season.groupby(['Season','Year']).sum().sum(axis=1).reset_index()

        year_data= data.iloc[:,3:26].groupby(['Year']).sum().sum(axis=1).reset_index()
        year_data['Sum (KW)'] = pd.DataFrame(year_data.iloc[:,1])
        year_data= year_data.drop(year_data.columns[1],axis=1)
        year_data['Avg (KW)']= year_data['Sum (KW)']/25
        year_data = year_data.round(3)
        year_data[['Year']] = year_data[['Year']].astype(int)
        
        fig = px.histogram(year_data, x='Year',y='Sum (KW)',color='Sum (KW)',nbins=2)
        fig1= px.histogram(year_data, x='Year',y='Avg (KW)',color='Avg (KW)',nbins=2)
        st.write("---")
        st.write('مجموع مصرف  در یک سال')
        st.plotly_chart(fig)
        st.write("---")
        st.write('میانگین در یک سال ')
        st.plotly_chart(fig1)   
        
        
        Season_data['Sum (KW)'] = pd.DataFrame(Season_data.iloc[:,2])
        Season_data= Season_data.drop(Season_data.columns[2],axis=1)
        Season_data['Avg (KW)']= Season_data['Sum (KW)']/25
        Season_data = Season_data.round(3)
        Season_data.sort_values(by=['Year'],inplace=True)
        Season_data[['Year']] = Season_data[['Year']].astype(str)
        Season_data['YearSeason']=Season_data['Year'] + ' ' + Season_data['Season']
        
        fig = px.histogram(Season_data, x='YearSeason',y='Sum (KW)',color='Sum (KW)',nbins=2)
        fig1= px.histogram(Season_data, x='YearSeason',y='Avg (KW)',color='Avg (KW)',nbins=2)
        st.write("---")
        st.write('مجموع مصرف  در یک فصل خاص')
        st.plotly_chart(fig)
        st.write("---")
        st.write('میانگین در یک فصل خاص')
        st.plotly_chart(fig1)
        

        
        
        
        Season[['Year']] = Season[['Year']].astype(str)
        Season['Year_Season'] = Season['Year'] + ' ' + Season['Season']
        
        y_axis_val1 = st.selectbox('Select Y_Axis Vlaue for Season', options= Season.columns)
        
        fig8 = px.histogram(Season, x='Year_Season', y= y_axis_val1,color='Year_Season')
        st.write("---")
        st.write('میانگین ساعتی در یک فصل خاصی')
        st.plotly_chart(fig8)
        y_axis_val = st.selectbox('Select Y_Axis Vlaue', options= data.iloc[:,1:].columns)

        data1 = pd.DataFrame(data.groupby(['Year','Month'])[y_axis_val].mean())
        
        if user==2:
            data1['Months'] = self.customer2 
        elif user==44:
            data1['Months'] = self.customer44 
        elif user==33:
            data1['Months'] = self.customer33
        elif user==16:
            data1['Months'] = self.customer16
        else:
            data1['Months'] =['تیر 1399', 'مرداد 1399', 'شهریور 1399', 'مهر 1399', 'آبان 1399', 'آذر 1399','دی 1399','بهمن 1399','اسفند 1399', 'فروردین 1400', 'اردیبهشت 1400', 'خرداد 1400','تیر 1400' , 'مرداد 1400', 'شهریور 1400', 'مهر 1400','آبان 1400','آذر 1400']
        
        

        
        fig = px.histogram(data, x='Date', y= y_axis_val)
        st.write("---")
        st.plotly_chart(fig)

        fig = px.line(data, x="Date", y=y_axis_val)

        st.write("---")
        st.plotly_chart(fig)
        
        # the histogram and line plot for Months
        fig = px.histogram(data1, x='Months',color=y_axis_val,y=y_axis_val)#['darkred'])
        st.write("---")
        st.plotly_chart(fig)
        
        fig = px.line(data1, x="Months", y=y_axis_val)

        st.write("---")
        st.plotly_chart(fig)
        # the box plot for y_axis_val
        fig = px.box(data,x=y_axis_val) 

        st.write("---")
        st.plotly_chart(fig)
        
        # the 3d plot for model
        # fig = go.Figure(data=[go.Mesh3d(z=data[y_axis_val],
        #                 y=data['Total Avg. (KW)'],
        #                 x=data['Date'],
        #                 opacity=0.5,color='rgba(244,23,100,0.6)')])
        # fig.update_layout(scene=dict(xaxis_showspikes=False,
        #                             yaxis_showspikes=False))
        # st.write("---")
        # st.plotly_chart(fig)
 
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


