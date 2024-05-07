import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(category, cutoff):
    category_map = {}
    for i in range(len(category)):
        if category.values[i] >= cutoff:
            category_map[category.index[i]] = category.index[i]
        else:
            category_map[category.index[i]] = "Other"
    return category_map


def clean_experience(year):
    if year == "More than 50 years":
        return 50
    if year == "Less than 1 year":
        return 0.5
    return int(year)


def clean_education(level):
    if "Bachelor" in level:
        return "Bachelor's degree"
    if "Master" in level:
        return "Master's degree"
    if "Professional degree" in level:
        return "Post grad"
    return "Less than a bachelors"


@st.cache
def load_data():
    df = pd.read_csv("data/survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro",
             "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "AnnualSalary"}, axis=1)
    df = df[df["AnnualSalary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df["Country"].value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["AnnualSalary"] <= 350000]
    df = df[df["AnnualSalary"] >= 10000]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    return df


df = load_data()


def show_explore_page():
    st.title("Explore SWE Salaries")

    st.write(
        """
    ### Stack Overflow SWE Salary 2023 
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%",
            shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)

    st.write("""#### Mean Salary Based on Country """)

    data = df.groupby(["Country"])[
        "AnnualSalary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary Based on Experience """)
    data = df.groupby(["YearsCodePro"])[
        "AnnualSalary"].mean().sort_values(ascending=True)
    st.line_chart(data)
