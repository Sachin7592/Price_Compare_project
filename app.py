import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "location": "Austin, Texas, United States",
        "api_key": "e1f7b611b84a55117b47e35651491559efb230605146e5538ce10d34c8a8ff7b",
        "gl":"in"
    }
    search = serpapi.search(params)
    results = search
    shopping_results = results["shopping_results"]
    return shopping_results


C1,C2= st.columns(2)
C1.image("e_pharmacy.png",width=200)
C2.header("E-Pharmacy price comparison system")


st.sidebar.title("Enter name of Medicine:")
med_name = st.sidebar.text_input("Enter name :")
number = st.sidebar.number_input("Enter number of options here :",min_value=1)
medicine_company = []
med_price=[]

if med_name is not None:
    if st.sidebar.button("price compare"):
        shopping_results = compare(med_name)
        lowest_price = float(shopping_results[0].get("price")[1:].replace(",", ""))
        print(lowest_price)
        lowest_price_index = 0
        st.sidebar.image(shopping_results[0].get("thumbnail"))

        #........................................................
        import re

        for i in range(int(number)):
            current_price = float(shopping_results[i].get("price")[1:].replace(",", ""))
            medicine_company.append(shopping_results[i].get("source"))
            med_price.append(float((shopping_results[i].get("price"))[1:]))


            #...........................................................................
            st.title(f"Option {i+1}")

            C1,C2=st.columns(2)
            C1.write("Company:")
            C2.write(shopping_results[i].get("source"))

            C1.write("Title:")
            C2.write(shopping_results[i].get("title"))

            C1.write("Price:")
            C2.write(shopping_results[i].get("price"))

            url=shopping_results[i].get("product_link")
            C1.write("Buy Link:")
            C2.write("[Link](%s)"%url)
            """.............................................................."""
            if (current_price<lowest_price):
                lowest_price = current_price
                lowest_price_index = i

        # This is best option
        st.title("Best Option")

        C1, C2 = st.columns(2)
        C1.write("Company:")
        C2.write(shopping_results[lowest_price_index].get("source"))

        C1.write("Title:")
        C2.write(shopping_results[lowest_price_index].get("title"))

        C1.write("Price:")
        C2.write(shopping_results[lowest_price_index].get("price"))

        url = shopping_results[lowest_price_index].get("product_link")
        C1.write("Buy Link:")
        C2.write("[Link](%s)" % url)


         #.............................
        # graph comparion
        df=pd.DataFrame(med_price,medicine_company)
        st.title("Chart Comparison")
        st.bar_chart(df)


        fig,ax=plt.subplots()
        ax.pie(med_price, labels=medicine_company,shadow=True)
        ax.axis("equal")
        st.pyplot(fig)
