from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from rapidfuzz import fuzz
from llm import detect_topics



#Uses VADER to find sentiment of review (Positive, Negative, Neutral)
def sentiment(review):

    sid_object = SentimentIntensityAnalyzer()
    sentiment_dict = sid_object.polarity_scores(review)

    if sentiment_dict['compound'] >= 0.05:
        return "Positive"
    elif sentiment_dict['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    

#Use LLM to extract topics
def topic(review):

    return detect_topics(review)
    


#keyword matching with typo tolerance to determine possible risk
def risk_flag(review):

    keywords = ["sick", "hair", "raw", "undercooked", "mold", "bugs", "allergy", "racist", "hazard", "discriminate"]

    for keyword in keywords:
        score = fuzz.partial_ratio(keyword, review.lower())
        if score >= 90:
            return True
    
    return False



def analysis(review):

    sentiment_result = sentiment(review)
    topic_result = topic(review)
    risk_flag_result = risk_flag(review)

    result = {
        'review': review,
        'sentiment': sentiment_result,
        'topic': topic_result,
        'risk': risk_flag_result
    }

    return result


def extract_name(username):

    if not username:
        return "valued customer"
    
    first_name = username.split(' ')[0]

    return first_name


    





