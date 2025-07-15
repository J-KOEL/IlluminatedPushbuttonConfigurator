import streamlit as st
import pandas as pd
from itertools import product

# Load CSVs based on illumination type
@st.cache_data
def load_data():
    led_light_unit = pd.read_csv("IlluminatedPushbuttonLEDLightUnit 4.csv")
    led_lens_color = pd.read_csv("IlluminatedPushbuttonLEDLensColor 4.csv")
    led_voltage = pd.read_csv("IlluminatedPushbuttonLEDVoltage 5.csv")

    inc_light_unit = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit 2.csv", skiprows=1, usecols=[0, 1], names=["Label", "Code"])
    inc_lens_color = pd.read_csv("illuminatedPushbuttonIncandescentLensColor 2.csv", skiprows=1, usecols=[0, 1], names=["Label", "Code"])

    circuit = pd.read_csv("NonIlluminatedPushbuttonCircuit 4.csv", skiprows=1, usecols=[0, 1], names=["Label", "Code"])

    return led_light_unit, led_lens_color, led_voltage, inc_light_unit, inc_lens_color, circuit

led_light_unit, led_lens_color, led_voltage, inc_light_unit, inc_lens_color, circuit_df = load_data()

# UI
st.title("10250T Illuminated Pushbutton Configurator")

illumination_type = st.radio("Select Illumination Type", ["LED", "Incandescent"])

if illumination_type == "LED":
    st.subheader("LED Configuration")
    light_unit_choice = st.selectbox("LED Light Unit", led_light_unit["Label"].tolist())
    lens_color_choice = st.selectbox("LED Lens Color", led_lens_color["Label"].tolist())
    voltage_choice = st.selectbox("LED Voltage", led_voltage["Label"].tolist())
    circuit_choice = st.selectbox("Circuit Type", circuit_df["Label"].tolist())

    light_unit_code = led_light_unit[led_light_unit["Label"] == light_unit_choice]["Code"].values[0]
    lens_color_code = led_lens_color[led_lens_color["Label"] == lens_color_choice]["Code"].values[0]
    voltage_code = led_voltage[led_voltage["Label"] == voltage_choice]["Code"].values[0]
    circuit_code = circuit_df[circuit_df["Label"] == circuit_choice]["Code"].values[0]

    catalog_number = f"10250T{light_unit_code}{lens_color_code}{voltage_code}-{circuit_code}"

else:
    st.subheader("Incandescent Configuration")
    light_unit_choice = st.selectbox("Incandescent Light Unit", inc_light_unit["Label"].tolist())
    lens_color_choice = st.selectbox("Incandescent Lens Color", inc_lens_color["Label"].tolist())
    circuit_choice = st.selectbox("Circuit Type", circuit_df["Label"].tolist())

    light_unit_code = inc_light_unit[inc_light_unit["Label"] == light_unit_choice]["Code"].values[0]
    lens_color_code = inc_lens_color[inc_lens_color["Label"] == lens_color_choice]["Code"].values[0]
    circuit_code = circuit_df[circuit_df["Label"] == circuit_choice]["Code"].values[0]

    catalog_number = f"10250T{light_unit_code}{lens_color_code}-{circuit_code}"

st.markdown("### Generated Catalog Number")
st.code(catalog_number)

# Show all combinations
if st.checkbox("Show all possible combinations"):
    if illumination_type == "LED":
        combinations = list(product(
            led_light_unit["Code"],
            led_lens_color["Code"],
            led_voltage["Code"],
            circuit_df["Code"]
        ))
        all_catalogs = [f"10250T{lu}{lc}{v}-{c}" for lu, lc, v, c in combinations]
    else:
        combinations = list(product(
            inc_light_unit["Code"],
            inc_lens_color["Code"],
            circuit_df["Code"]
        ))
        all_catalogs = [f"10250T{lu}{lc}-{c}" for lu, lc, c in combinations]

    st.write(f"Total combinations: {len(all_catalogs)}")
    st.dataframe(pd.DataFrame(all_catalogs, columns=["Catalog Number"]))
