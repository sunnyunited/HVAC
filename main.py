import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import core

#testing comment

st.sidebar.title('HVAC Metric / Imperial unit Calculator for HVAC Engineer')
st.sidebar.markdown('There are numerous calculation available there - but sometimes as HVAC engineers we rely on some rule of '
         'thumb numbers and the \'feel\' of the number.')
st.sidebar.markdown('Coming from a metric world, I struggled (and still'
         ' struggling). That\'s why I create this for myself.')

option_df = pd.DataFrame()
option_df['option']= ['Temperature','Velocity','CFM','Pressure','GPM(WIP)','Energy(WIP)']

#option = st.sidebar.selectbox('',option_df['option'])
st.markdown('# Select required section(s):')
option = st.multiselect('',option_df['option'])

if 'Velocity' in option:
    st.markdown('## Simple velocity conversation')
    st.markdown('### Input')
    input_unit = st.selectbox('Select input velocity unit', options=['FPS','FPM','m/s'])
    output_unit = 'FPS' if input_unit != 'FPS' and input_unit != 'FPM' else 'm/s'
    x = st.slider('Velocity',min_value=0.0, max_value=15.0, value=2.0, step=0.2)
    x = st.number_input('',value=x)
    if input_unit == 'FPS': p1 = core.Cal(FPS=x)
    elif input_unit == 'FPM': p1 = core.Cal(FPM=x)
    elif input_unit == 'm/s': p1 = core.Cal(mps=x)
    result=p1.velocity_conv()
    st.markdown('### Result')
    st.write(x, str(input_unit),' is equal to',result, str(output_unit)+'.',)

if 'CFM' in option:
    st.markdown('## Simple air flowrate conversation')
    st.markdown('### Input')
    input_unit = st.selectbox('Select input air flowrate unit', options=['CFM', 'l/s'])
    output_unit = 'CFM' if input_unit != 'CFM' else 'l/s'
    x = st.slider('Air flowrate', min_value=0, max_value=2000, value=500, step=10)
    x = st.number_input('', value=x)
    if input_unit == 'CFM':
        p1 = core.Cal(CFM=x)
    elif input_unit == 'l/s':
        p1 = core.Cal(lps=x)
    result = p1.airflow_conv()
    st.markdown('### Result')
    st.write(x, str(input_unit), ' is equal to', result, str(output_unit) + '.', )

if 'Temperature' in option:
    st.markdown('## Simple temperature conversation')
    st.markdown('### Input')
    input_unit = st.selectbox('Select input temperature unit', options=['°F','°C'])
    output_unit = '°F' if input_unit != '°F' else '°C'
    x = st.slider('Temperature',min_value=-50, max_value=250, value=68, step=1)
    x = st.number_input('',value=x)
    if input_unit == '°F': p1 = core.Cal(F=x)
    elif input_unit == '°C': p1 = core.Cal(C=x)
    result=p1.temp_conv()
    st.markdown('### Result')
    st.write(x,'&#176;'+str(input_unit),' is equal to',result,'&#176;'+str(output_unit)+'.',)


if 'Pressure' in option:
    st.markdown('## Simple temperature conversation')
    st.markdown('### Input')
    input_unit = st.selectbox('Select input temperature unit',
                              options=['in. w.g.','Pa','kPa','ft. w.g.',
                                       'in. w.g. per 100 ft','Pa/m'])
    if input_unit =='in. w.g.':
        cal_unit = 'inwg'
        output_unit = "Pa" #display only
        min_v = 0.5
        max_v = 1.0
        start_v = 0.6
        step_v = 0.1
        factor = 1

    if input_unit =='Pa':
        cal_unit = 'pa'
        output_unit = "in. w.g." #display only
        min_v = 0
        max_v = 1000
        start_v = 200
        step_v = 10
        factor = 1

    if input_unit == 'kPa':
        cal_unit = 'pa'
        output_unit = "in. w.g." #display only
        min_v = 0.5
        max_v = 1.0
        start_v = 0.6
        step_v = 0.1
        factor = 1000

    if input_unit == 'in. w.g. per 100 ft':
        cal_unit = 'inwg_100ft'
        output_unit = "Pa/m" #display only
        min_v = 0.5
        max_v = 1.0
        start_v = 0.6
        step_v = 0.1
        factor = 1

    if input_unit == 'Pa/m':
        cal_unit = 'pa_m'
        output_unit = "in. w.g. per 100 ft" #display only
        min_v = 0.5
        max_v = 1.0
        start_v = 0.6
        step_v = 0.1
        factor = 1

    x = st.slider(input_unit,min_value=min_v, max_value=max_v, value=start_v, step=step_v)
    x = st.number_input('',value=x)
    if cal_unit == 'pa': p1 = core.Cal(pa=x*factor)
    elif cal_unit == 'inwg': p1 = core.Cal(inwg=x*factor)
    elif cal_unit == 'inwg_100ft': p1 = core.Cal(inwg_100ft=x*factor)
    elif cal_unit == 'pa_m': p1 = core.Cal(pa_m=x*factor)

    result=p1.pressure_conv()
    st.markdown('### Result')
    st.write(x,str(input_unit),' is equal to',result,str(output_unit)+'.',)

if 'testing' in option:

    st.write('F to C \n '
             'FPS FPM m/s\n'
             ' CFM l/s \n '
             ' BTU/h MBH W Ton\n'
             'in.w.g 100ft pa/m '
             ' inch reduction ratio')

    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        st.line_chart(chart_data)

    st.write('F to C \n '
             'FPS FPM m/s\n'
             ' CFM l/s \n '
             ' BTU/h MBH W Ton\n'
             'in.w.g 100ft pa/m '
             ' inch reduction ratio')

    df = pd.DataFrame({
    'first column': [1, 2, 3, 4]
    })
    st.write(df)
