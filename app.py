import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Combined Custom CSS
st.markdown(
    """
    <style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #78b2cc; /* Dark Ash Background */
    }

    /* Sidebar Button Styling */
    [data-testid="stSidebar"] .stButton button {
        background-color: #ffffff; /* White Background */
        color: black; /* Black text color */
        border: none;
        border-radius: 10px;
        font-size: 30px;
        font-weight: bold;
        padding: 10px;
        margin-bottom: 10px;
        width: 100%;
        cursor: pointer;
        font-family: 'Poppins', sans-serif; /* Poppins Font */
        transition: background-color 0.3s, transform 0.3s; /* Smooth transition */
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #ffffff; /* Keep white on hover */
        color: #001f3f; /* Navy Blue text on hover */
        transform: scale(1.05); /* Slightly enlarge button on hover */
    }

    [data-testid="stSidebar"] .stButton button:active {
        background-color: #001f3f; /* Navy Blue when clicked */
        color: white; /* White text when clicked */
    }
    
    /* Main Button Styling */
    .main-button {
        background-color: #ffffff; /* White Background */
        color: black; /* Black text color */
        border: none;
        border-radius: 10px;
        font-size: 30px;
        font-weight: bold;
        padding: 10px;
        cursor: pointer;
        font-family: 'Poppins', sans-serif; /* Poppins Font */
        transition: background-color 0.3s, transform 0.3s; /* Smooth transition */
        width: 100%; /* Full width */
    }

    .main-button:hover {
        background-color: #ffffff; /* Keep white on hover */
        color: #001f3f; /* Navy Blue text on hover */
        transform: scale(1.05); /* Slightly enlarge button on hover */
    }

    .main-button:active {
        background-color: #001f3f; /* Navy Blue when clicked */
        color: white; /* White text when clicked */
    }

    /* Main Content Styling */
    [data-testid="stAppViewContainer"] > .main {
        background-color: #001f3f; /* Navy Blue */
        color: white; /* Set all text color to white */
    }

    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }

    /* Home Page Styles */
    .home-title {
        text-align: center; /* Center title */
        font-size: 48px; /* Increase font size */
        margin-bottom: 20px; /* Space below the title */
        color: white; /* White text */
    }

    .welcome-text {
        font-size: 20px; 
        text-align: center; 
        margin-bottom: 40px; 
        color: white; /* Change text color to white */
    }
    
    /* Input Form Styles */
    .input-title {
        text-align: center; /* Center title */
        font-size: 32px; /* Increase font size for input form */
        margin-bottom: 20px; /* Space below the title */
        color: white; /* White text */
    }

    .input-label {
        font-size: 20px; /* Label font size */
        color: white; /* White text for labels */
    }

    /* Prediction result styles */
    .prediction {
        color: white;  /* White text for prediction title */
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }

    .p {
        color: #78b2cc;  /* Light green color for prediction result */
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        background-color: #001f3f; /* Dark background for contrast */
    }

    .success {
        color: #039905; /* Green text for success message */
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background-color: #8ef587; /* Light green background */
        margin-top: 20px;
    }

    .error {
        color: #ad0202; /* Red text for error message */
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background-color: #f07d7d; /* Light red background */
        margin-top: 20px;
    }

    /* Additional Styles */
    label {
        color: #f1f1f1 !important;  /* Light color for label text */
        font-size: 16px !important;  /* Adjust font size */
        margin-bottom: 10px !important;
    }
    input, select {
        color: #333333;  /* Darker text for input fields */
        background-color: #f9f9f9;  /* Light background for inputs */
        padding: 10px !important;  /* Add some padding to inputs */
        border-radius: 5px !important;  /* Rounded corners */
        font-size: 16px;  /* Ensure input text is legible */
    }

    /* Image Position */
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 30px; /* Add margin above the image */
    }

     div.stButton > button {
        color: black;  /* Text color */
    }


    </style>
 
    """,
    unsafe_allow_html=True
)

# Load the saved model
with open('saved_rf_model.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

# Extract the model from the loaded dictionary
rf_model_loaded = loaded_data["model"]

# Load the datasets
original_data = pd.read_csv('C:\\Users\\Lihini Akarsha\\Desktop\\FDM\\FDM\\d.csv')  # Dataset with categorical values
numerical_data = pd.read_csv('C:\\Users\\Lihini Akarsha\\Desktop\\FDM\\FDM\\cleaned_drug_sensitivity.csv')  # Dataset with corresponding numerical values

# Remove any extra spaces in column names
original_data.columns = original_data.columns.str.strip()
numerical_data.columns = numerical_data.columns.str.strip()

# Create separate mappings for each categorical column
cell_line_name_mapping = pd.Series(numerical_data['CELL_LINE_NAME'].values, 
                                   index=original_data['CELL_LINE_NAME']).to_dict()

drug_name_mapping = pd.Series(numerical_data['DRUG_NAME'].values, 
                              index=original_data['DRUG_NAME']).to_dict()

target_pathway_mapping = pd.Series(numerical_data['TARGET_PATHWAY'].values, 
                                   index=original_data['TARGET_PATHWAY']).to_dict()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Input Form"):
    st.session_state.page = "Input Form"

# Home Page
if st.session_state.page == "Home":
    st.markdown("<h1 class='home-title'>Med-React</h1>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-text'>Welcome to the Med-React Prediction App!</p>", unsafe_allow_html=True)
    st.markdown(
    """<div style="text-align: justify; margin: 0 auto; max-width: 800px;">
        This app predicts the target variable (IC50 values) based on user input of 
        cell line names and drug names. It utilizes a trained machine learning model to 
        provide accurate predictions for drug sensitivity in various cancer cell lines. 
        This application can be a valuable tool for doctors and medical researchers, 
        assisting them in making informed decisions regarding treatment options and 
        enhancing the understanding of drug efficacy in specific cancer types.
    </div>""",
        unsafe_allow_html=True
    )
    
    st.image("C:\\Users\\Lihini Akarsha\\Desktop\\FDM\\FDM\\image.jpeg", use_column_width=True)

    if st.button("Get Started"):
        st.session_state.page = "Input Form"

# Input Form Page
if st.session_state.page == "Input Form":
    st.markdown("<h2 style='color: white;'>Input Features for Prediction</h2>", unsafe_allow_html=True)
    
    # Define input fields
    st.markdown("<p>Fill the fields below:</p>", unsafe_allow_html=True)
    
    # Selectboxes for categorical features
    cell_line_name = st.selectbox("Cell Line Name", original_data['CELL_LINE_NAME'].unique())
    drug_name = st.selectbox("Drug Name", original_data['DRUG_NAME'].unique())
    
    # Text inputs for numerical features with no restrictions on decimal points
    auc = st.number_input("AUC", format="%.10f")
    z_score = st.number_input("Z-Score", format="%.10f")
    
    # Target pathway as a number (assumed as numeric)
    target_pathway = st.selectbox("Target Pathway", original_data['TARGET_PATHWAY'].unique())

    # Predict button
    if st.button("Predict"):
        # Convert categorical inputs to their corresponding numeric values using the mappings
        cell_line_numeric = cell_line_name_mapping[cell_line_name]
        drug_numeric = drug_name_mapping[drug_name]
        target_pathway_numeric = target_pathway_mapping[target_pathway]
        
        # Create user input array with numerical representations
        user_input = np.array([[cell_line_numeric, drug_numeric, float(auc), float(z_score), target_pathway_numeric]])
        
        # Make prediction using the model
        prediction = rf_model_loaded.predict(user_input)[0]  # Get the first prediction value
        
        # Display the prediction result
        st.markdown("<div class='prediction' style='color: white;'>Prediction</div>", unsafe_allow_html=True)
        # Display the predicted value in one line
        st.markdown(f"""
            <div class='prediction'>
                <span style='color: #78b2cc; font-size: 28px; font-weight: bold;'>Predicted LN_IC50 value:</span> 
                <span style='border: 2px solid #78b2cc; padding: 5px 10px; border-radius: 8px; background-color: #001f3f; color: #78b2cc; font-size: 28px; font-weight: bold;'>{prediction:.4f}</span>
            </div>
        """, unsafe_allow_html=True)


        # Provide interpretation of prediction
        if prediction < 0:
            st.markdown(f"<div class='success'>The drug <strong>{drug_name}</strong> will be effective for the cell line <strong>{cell_line_name}</strong>.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='error'>The drug <strong>{drug_name}</strong> will not be effective for the cell line <strong>{cell_line_name}</strong>.</div>", unsafe_allow_html=True)
