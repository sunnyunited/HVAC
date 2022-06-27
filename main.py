import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import conv_core
import duct_core
import rots
from math import sqrt, pi

st.set_page_config(page_title="HVAC", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

#testing comment

def unit_hl(text):

    new_text = str("["+text+"]")
    return new_text

def duct_calc():

    roughness_selection = st.select_slider('Select duct construction material', options=["GI (0.15)", "Concrete (1.0)"])
    roughness = 0.15 if roughness_selection == "GI (0.15)" else 1.0
    input_unit = st.selectbox('Select input air flowrate unit', options=['CFM', 'l/s'])
    x = st.slider(input_unit, min_value=50, max_value=20000, value=500, step=10)
    x = st.number_input('', value=x)
    if input_unit == 'CFM':
        pass
    elif input_unit == 'l/s':
        duct_core.sizing(x,roughness)
        #pass

def temperature_conv():
    st.markdown('##### Temperature Input')
    input_unit = st.selectbox('Select input temperature unit', options=['°F', '°C'])
    output_unit = '°F' if input_unit != '°F' else '°C'
    x = st.slider(input_unit, min_value=-50, max_value=250, value=68, step=1)
    x = st.number_input('', value=x)
    if input_unit == '°F':
        p1 = conv_core.Cal(F=x)
    elif input_unit == '°C':
        p1 = conv_core.Cal(C=x)
    result = p1.temperature()
    st.write("Result:",x, str(input_unit), ' is equal to', result, str(output_unit) + '.')

def airflow_conv():
    second_output = False
    st.markdown('##### Air flowrate Input')
    input_unit = st.selectbox('Select input air flowrate unit', options=['CFM', 'l/s'])
    output_unit = 'CFM' if input_unit != 'CFM' else 'l/s'
    x = st.slider(input_unit, min_value=50, max_value=20000, value=500, step=10)
    x = st.number_input('', value=x)
    if input_unit == 'CFM':
        p1 = conv_core.Cal(CFM=x)
        second_output = True
    elif input_unit == 'l/s':
        p1 = conv_core.Cal(lps=x)
    result = p1.airflow()
    if second_output == True:
        st.write("Result:", x, str(input_unit), ' is equal to', result, str(output_unit), " or",
                 round(result*3.6, 2), " m³/hr", '.')
    else:
        st.write("Result:", x, str(input_unit), ' is equal to', result, str(output_unit) + '.')

def waterflow_conv():
    st.markdown('##### Water flowrate Input')
    input_unit = st.selectbox('Select input water flowrate unit', options=['GPM', 'l/s'])
    output_unit = 'GPM' if input_unit != 'GPM' else 'l/s'
    x = st.slider(input_unit, min_value=1.0, max_value=200.0, value=23.0, step=0.1)
    x = st.number_input('', value=x)
    if input_unit == 'GPM':
        p1 = conv_core.Cal(GPM=x)
    elif input_unit == 'l/s':
        p1 = conv_core.Cal(lps=x)
    result = p1.waterflow()
    st.write("Result:", x, str(input_unit), ' is equal to', result, str(output_unit) + '.')

def velocity_conv():
    second_output = False
    st.markdown('##### Velocity Input')
    input_unit = st.selectbox('Select input velocity unit', options=['FPS', 'FPM', 'm/s'])
    output_unit = 'FPS' if input_unit != 'FPS' and input_unit != 'FPM' else 'm/s'
    x = st.slider(input_unit, min_value=0.0, max_value=15.0, value=2.0, step=0.2)

    x = st.number_input('', value=x)
    if input_unit == 'FPS':
        p1 = conv_core.Cal(FPS=x)
    elif input_unit == 'FPM':
        p1 = conv_core.Cal(FPS=(x/60))
    elif input_unit == 'm/s':
        p1 = conv_core.Cal(mps=x)
    result = p1.velocity()
    if second_output == True:
        st.write("Result:", x, str(input_unit), ' is equal to', result, str(output_unit), " or",
                 round(result*60, 2), " FPM", '.')
    else:
        st.write("Result:", x, str(input_unit), ' is equal to', result, str(output_unit) + '.')

def pressure_conv():

    input = st.selectbox('Select input pressure unit',
                              options=['in.w.g.', 'ft.w.g.',
                                       'Pa', 'kPa',
                                       'Pa/m', 'kPa/100m',
                                       'in.w.g. per 100ft', 'ft.w.g. per 100ft'])
    second_output = False

    if input == 'in.w.g.':
        slider_setting = {"input_unit": 'in.w.g.', "output_unit": 'Pa',"min": 0.01, "max": 2.0,
                          "start": 0.03, "step": 0.01, "factor": 1}

    if input == 'ft.w.g.':
        slider_setting = {"input_unit": 'in.w.g.', "output_unit": 'Pa',"min": 1, "max": 50,
                          "start": 10, "step": 1, "factor": 12}

    if input == 'Pa':
        slider_setting = {"input_unit": 'Pa', "output_unit": 'in.w.g.',"min": 15, "max": 1000,
                          "start": 50, "step": 1, "factor": 1}
        second_output = True
        second_unit = "ft.w.g."

    if input == 'kPa':
        slider_setting = {"input_unit": 'Pa', "output_unit": 'in.w.g.', "min": 1.0, "max": 10.0,
                          "start": 1.0, "step": 0.2, "factor": 1000}
        second_output = True
        second_unit = "ft.w.g."

    if input == 'Pa/m' or input == 'kPa/100m':
        slider_setting = {"input_unit": 'Pa/m', "output_unit": 'in.w.g. per 100ft', "min": 0.4, "max": 1.2,
                          "start": 0.8, "step": 0.05, "factor": 1}
        second_output = True
        second_unit = "ft.w.g. per 100ft"

    if input == 'in.w.g. per 100ft':
        slider_setting = {"input_unit": 'in.w.g. per 100ft', "output_unit": 'Pa/m', "min": 0.01, "max": 0.1,
                          "start": 0.08, "step": 0.01, "factor": 1}

    if input == 'ft.w.g. per 100ft':
        slider_setting = {"input_unit": 'in.w.g. per 100ft', "output_unit": 'Pa/m',  "min": 1.0, "max": 5.0,
                          "start": 3.0, "step": 0.1, "factor": 12}

    x = st.slider(input, min_value=slider_setting['min'],max_value=slider_setting['max'], value=slider_setting['start'],step=slider_setting['step'])

    x = st.number_input('', value=x)

    if slider_setting['input_unit'] == 'Pa':
        p1 = conv_core.Cal(pa=x * slider_setting['factor'])

    elif slider_setting['input_unit'] == 'in.w.g.':
        p1 = conv_core.Cal(inwg=x * slider_setting['factor'])

    elif slider_setting['input_unit'] == 'in.w.g. per 100ft':
        p1 = conv_core.Cal(inwg_100ft=x * slider_setting['factor'])

    elif slider_setting['input_unit'] == 'Pa/m':
        p1 = conv_core.Cal(pa_m=x * slider_setting['factor'])

    result = p1.pressure()

    if second_output == True:
        st.write("Result:",x, str(input), " is equal to", result, str(slider_setting['output_unit']), "or",
                 round(result/12,2), second_unit, ".")
    else:
        st.write("Result:",x, str(input), " is equal to", result, str(slider_setting['output_unit']), ".")

def airflow_rot():
    st.write("##### Duct Mains")
    st.write("Max PD: ", rots.ductmain_pd_i, unit_hl(rots.unitduct_pd_i), ", or ",
             rots.ductmain_pd_m, unit_hl(rots.unitduct_pd_m))
    st.write("Max Velocity: ", rots.ductmain_v_i, unit_hl(rots.unitduct_v_i), ", or ",
             rots.ductmain_v_m, unit_hl(rots.unitduct_v_m))

    st.write("##### Duct Branches")
    st.write("Max PD: ", rots.ductbranch_pd_i, unit_hl(rots.unitduct_pd_i), ", or ",
             rots.ductbranch_pd_m, unit_hl(rots.unitduct_pd_m))
    st.write("Max Velocity: ", rots.ductbranch_v_i, unit_hl(rots.unitduct_v_i), ", or ",
             rots.ductbranch_v_m, unit_hl(rots.unitduct_v_m))

def waterflow_rot():
    st.write("##### Pipe Mains")
    st.write("Max PD: ", rots.pipemain_pd_i, unit_hl(rots.unitpipe_pd_i), ", or ",
             rots.pipemain_pd_m, unit_hl(rots.unitpipe_pd_m))
    st.write("Max Velocity: ", rots.pipemain_v_i, unit_hl(rots.unitpipe_v_i), '(',
             rots.pipeheader_v_i, unit_hl(rots.unitpipe_pd_i), "in header)", ", or ",
             rots.pipemain_v_m, unit_hl(rots.unitpipe_v_m), "(",
             rots.pipeheader_v_m, unit_hl(rots.unitpipe_pd_m), "in header)")

    st.write("##### Pipe Branches")
    st.write("Max PD: ", rots.pipebranch_pd_i, unit_hl(rots.unitpipe_pd_i), ", or ",
             rots.pipebranch_pd_m, unit_hl(rots.unitpipe_pd_m))
    st.write("Max Velocity: ", rots.pipebranch_v_i, unit_hl(rots.unitpipe_v_i), ", or ",
             rots.pipebranch_v_m, unit_hl(rots.unitpipe_v_m))

    st.write("##### **CRB Pipe")
    st.write("Max PD: ", rots.pipemain_pd_CRB, "/", rots.pipebranch_pd_CRB,
             unit_hl(rots.unitduct_pd_i), "in mains/branches")

def louver_rot():
    st.write("##### Louvers")
    st.write("Max PD: ", rots.louver_pd_i, unit_hl(rots.unitlouver_pd_i), ", or ",
             rots.louver_pd_m, unit_hl(rots.unitlouver_pd_m))
    st.write("Max Velocity: ",
             rots.louverface_v_i, "/", rots.louverfree_v_i,
             unit_hl(rots.unitlouver_v_i), "(face/free area)", ", or ",
             rots.louverface_v_m, "/", rots.louverfree_v_m,
             unit_hl(rots.unitlouver_v_m), "(face/free area)")

#------------------------

st.sidebar.title('HVAC Metric / Imperial unit Calculator for HVAC Engineer')
with st.sidebar.expander("About", expanded = False):
    st.markdown('There are numerous calculation available there - but sometimes as HVAC engineers we rely on some rule of '
         'thumb numbers and the \'feel\' of the number.')
    st.markdown('Coming from a metric world, I struggled (and still'
         ' struggling). That\'s why I create this for myself.')

with st.sidebar.expander("Sizing Calculator", expanded=True):
    st.write("Upcomingggg!")
    _duct_calc = st.checkbox("Duct sizer")

with st.sidebar.expander("Converters", expanded=True):
    _temperature_conv = st.checkbox("Temperature")
    _airflow_conv = st.checkbox("Air flowrate")
    _waterflow_conv = st.checkbox("Water flowrate")
    _velocity_conv = st.checkbox("Velocity")
    _pressure_conv = st.checkbox("Pressure")

with st.sidebar.expander("Rule of thumbs", expanded=True):
    _airflow_rot = st.checkbox("Air flow", value=True)
    _waterflow_rot = st.checkbox("Water flow", value=True)
    _louver_rot = st.checkbox("Louver")

with st.sidebar.expander("WIP"):

    _energy_conv = st.checkbox("Energy")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("#### Sizing Calculator")
    if _duct_calc:
        st.write("Upcomingggg!")
        #duct_calc()

with col2:
    st.write("#### Converters")
    if _temperature_conv:
        temperature_conv()
        st.text("--------")

    if _airflow_conv:
        airflow_conv()
        st.text("--------")

    if _waterflow_conv:
        waterflow_conv()
        st.text("--------")

    if _velocity_conv:
        velocity_conv()
        st.text("--------")

    if _pressure_conv:
        pressure_conv()
        st.text("----")

with col3:
    st.write("#### Rule of thumbs")

    if _airflow_rot:
        airflow_rot()
        st.text("--------")

    if _waterflow_rot:
        waterflow_rot()
        st.text("--------")

    if _louver_rot:
        louver_rot()
        st.text("--------")

if __name__ == '__main__':
    pass