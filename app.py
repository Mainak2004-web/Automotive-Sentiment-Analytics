import streamlit as st
from transformers import pipeline
import re


st.set_page_config(
    page_title="Automotive Sentiment Analytics",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 50%,
            #0f172a 100%
        );
        color: white;
    }

    /* Main content width and spacing */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main application title */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    /* Subtitle below title */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 35px;
    }

    /* Text input area */
    textarea {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }

    /* Text input label */
    label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    /* Analyze button */
    .stButton > button {
        width: 100%;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-size: 17px;
        font-weight: 700;
        transition: 0.3s;
    }

    /* Analyze button hover effect */
    .stButton > button:hover {
        background: #1d4ed8;
        transform: scale(1.01);
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 28px;
        margin-bottom: 12px;
    }

    /* Small information text */
    .info-text {
        color: #cbd5e1;
        font-size: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 40px;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">'
    '🚗 AI Automotive Review Sentiment Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze automotive reviews using AI and identify aspect-level sentiment.'
    '</div>',
    unsafe_allow_html=True
)

classifier = pipeline("sentiment-analysis")

aspects = {

    "Battery": [
        "battery",
        "battery range",
        "charging",
        "charging time"
    ],

    "Engine": [
        "engine",
        "motor"
    ],

    "Mileage": [
        "mileage",
        "fuel economy",
        "fuel consumption"
    ],

    "Safety": [
        "safety",
        "brake",
        "braking",
        "airbag"
    ],

    "Comfort": [
        "comfort",
        "seat",
        "seats"
    ],

    "Service": [
        "service",
        "maintenance"
    ],

    "Infotainment": [
        "infotainment",
        "screen",
        "display",
        "audio"
    ],

    "Price": [
        "price",
        "cost",
        "expensive",
        "cheap"
    ]
}


st.markdown(
    '<div class="section-title">'
    '📝 Enter Your Automotive Review'
    '</div>',
    unsafe_allow_html=True
)

review = st.text_area(
    "Write your review below:",
    placeholder=(
        "Example: The engine is powerful and the seats are comfortable, "
        "but the price is too high."
    ),
    height=160
)
if st.button("🔍 Analyze Review"):


    if not review.strip():

        st.warning(
            "⚠️ Please enter an automotive review."
        )

    else:


        overall = classifier(review)[0]

        st.markdown(
            '<div class="section-title">'
            '📊 Overall Sentiment'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.write(
                "**Sentiment:**",
                overall["label"]
            )

            confidence = overall["score"] * 100

            st.write(
                "**Confidence:**",
                round(confidence, 2),
                "%"
            )

        st.markdown(
            '<div class="section-title">'
            '🔎 Aspect-Level Sentiment'
            '</div>',
            unsafe_allow_html=True
        )

        sentences = re.split(
            r"[,.;!?]+",
            review
        )

        found_aspects = []


        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            result = classifier(sentence)[0]

            for aspect, keywords in aspects.items():

                for keyword in keywords:

                    if keyword.lower() in sentence.lower():

                        if "battery range" in sentence.lower():

                            display_aspect = "Battery range"

                        elif "charging time" in sentence.lower():

                            display_aspect = "Charging time"

                        else:

                            display_aspect = aspect


                        found_aspects.append(
                            {
                                "Aspect": display_aspect,
                                "Sentiment": result["label"]
                            }
                        )

                        break

        unique_aspects = []

        for item in found_aspects:

            if item not in unique_aspects:

                unique_aspects.append(item)

        if unique_aspects:

            # Keep the table inside a bordered container
            with st.container(border=True):

                st.table(unique_aspects)

        else:

            st.info(
                "ℹ️ No specific automotive aspect detected."
            )

        st.markdown(
            '<div class="section-title">'
            '💬 Your Review'
            '</div>',
            unsafe_allow_html=True
        )

        # Keep review text inside the bordered container
        with st.container(border=True):

            st.write(review)


st.markdown(
    """
    <div class="footer">
        AI-Based Automotive Review & Customer Sentiment Analytics
    </div>
    """,
    unsafe_allow_html=True
)