import streamlit as st
import json
import re
@st.cache_data
def load_reviews():
    with open("reviews.json","r",encoding="utf-8") as file:
        return json.load(file)
@st.cache_data
def load_extracted_reviews():
    with open("extracted_reviews.json","r",encoding="utf-8") as file:
        return json.load(file)
def highlight_food_service(review_text,food_comments,service_comments):
    for food in food_comments:
        review_text=re.sub(rf"({re.escape(food)})",r'<span style="color: green; font-weight: bold;">\1</span>',review_text,flags=re.IGNORECASE)
    for service in service_comments:
        review_text=re.sub(
            rf"({re.escape(service)})",r'<span style="color: blue; font-weight: bold;">\1</span>',review_text,flags=re.IGNORECASE)
    return review_text
st.title("🍽️ Restaurant Review Dashboard")
st.markdown(
    """
    Welcome to the Restaurant Review Dashboard! 
    You can search for reviews of your favorite restaurant and get detailed feedback.
    Enter the name of a restaurant below to view the reviews.
"""
)
search_query=st.text_input("Search for a restaurant:")
restaurant_name="Kitchen + Kocktails by Kevin Kelley - DC"
reviews_data=load_reviews()
extracted_reviews_data=load_extracted_reviews()
st.write(f"Data loaded: {len(extracted_reviews_data)} reviews")
if search_query:
    if search_query==restaurant_name:
        st.write(f"Filtered reviews: {len(extracted_reviews_data)} reviews")
        st.subheader(f'Reviews for "{restaurant_name}"')
        reviews_per_page=10
        total_pages=(len(extracted_reviews_data)//reviews_per_page)
        page=st.number_input("page:",min_value=1,max_value=total_pages,value=1,step=1)
        start_idx=(page-1)*reviews_per_page
        end_idx=start_idx+reviews_per_page
        reviews_to_display=reviews_data[start_idx:end_idx]
        extracted_reviews_to_display=extracted_reviews_data[start_idx:end_idx]
        for review,extracted_review in zip(reviews_to_display,extracted_reviews_to_display):
            review_text=extracted_review.get("review_text",review.get("review_text"))
            food_comments=extracted_review.get("food_quality",[])
            service_comments=extracted_review.get("staff_service",[])
            highlighted_review=highlight_food_service(review_text,food_comments,service_comments)
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff; padding: 15px; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: #4285F4; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px; font-weight: bold;">
                            {review['name'][0].upper()}
                        </div>
                        <div style="margin-left: 10px;">
                            <strong style="color:black;">{review['name']}</strong>
                            <div style="color: #5f6368; font-size: 14px;">{review['location']}</div>
                        </div>
                    </div>
                    <div style="color: #ff4d4f; font-size: 16px; margin-bottom: 5px;">
                        {'⭐' * int(review['overall'])}
                    </div>
                    <div style="color: #5f6368; font-size: 14px; margin-bottom: 10px;">
                        Overall {review['overall']} • Food {review['food']} • Service {review['Service']} • Ambience {review['Ambience']}
                    </div>
                    <div style="color: #5f6368; font-size: 14px; margin-bottom: 15px;">
                        {review['date']}
                    </div>
                    <div style="font-size: 16px; line-height: 1.6; color: #333;">
                        {highlighted_review}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown(f"**Page {page} of {total_pages}**")
    else:
        st.warning("No reviews found for the given restaurant. Please try searching for 'Kitchen + Kocktails by Kevin Kelley - DC'.")
else:
    st.warning("Please enter a restaurant name to search.")