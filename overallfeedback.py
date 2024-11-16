import os
from langchain.schema import HumanMessage, ChatMessage
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_score(conversation_history):
    combined_text = ' '.join([message.content for message in conversation_history if isinstance(message, HumanMessage)])

    sid_obj = SentimentIntensityAnalyzer()

    sentiment_dict = sid_obj.polarity_scores(combined_text)
    Negative = sentiment_dict['neg']
    Positive = sentiment_dict['pos']

    if Positive >= 0.05 :
        return 1
    elif Negative <= - 0.05 :
        return 0.5
    else :
        return None



def user_word_count(conversation_history):
    total_word_count = 0
    response_count = 0
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            word_count = len(message.content.split())
            total_word_count += word_count
            response_count += 1
    if response_count > 0:
        return total_word_count / response_count
    else:
        return 0

def conversation_length(conversation_history):
    total_length = 0
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            # Adjust based on your preference: words or characters
            content_length = len(message.content.split())  # For word count
            # content_length = len(message.content)  # For character count
            total_length += content_length
    return total_length


def overall_engagement_score(conversation_history, word_count_weight=0.3, conversation_length_weight=0.7):
    user_word_count_score = normalize_score(user_word_count(conversation_history), 0, 20)
    conversation_length_score = normalize_score(conversation_length(conversation_history), 0, 200)
    overall_score = (user_word_count_score * word_count_weight) + (conversation_length_score * conversation_length_weight)
    return overall_score

def normalize_score(score, min_value, max_value):
    if max_value == min_value:
        return 0
    return (score - min_value) / (max_value - min_value)


def overall_feedback(conversation_history):
    sentiment = sentiment_score(conversation_history)
    engagement = overall_engagement_score(conversation_history, word_count_weight=0.4, conversation_length_weight=0.6)

    if engagement > 1:
        engagement =1

    sentiment = sentiment if sentiment is not None else 0
    engagement = engagement if engagement is not None else 0

    overall_feedback_percentage = round((sentiment + engagement) /2 * 100)

    if overall_feedback_percentage >=75:
        return f"You're a communication rockstar! Your engagement and insights were top-notch. Your Feedback is {overall_feedback_percentage} %"
    elif overall_feedback_percentage >= 50:
        return f"Great Job.There's space to be more proactive and dive deeper into the topics. Your Feedback is {overall_feedback_percentage} %"
    elif overall_feedback_percentage >= 25:
        return f"You could have been more engaging and insightful. Your Feedback is {overall_feedback_percentage} %"
    else:
        return f"You can do better. Your Feedback is {overall_feedback_percentage} %"