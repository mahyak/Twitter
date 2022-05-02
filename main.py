import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from helpers.stop_words import Stop_words as  sw
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

from modules.twitter_client import TwitterClient
from modules.twitter_analyzer import TweetAnalyzer
from modules.user_interactions import UserInteraction

if __name__ == '__main__':

    print("Please inser the username: ")
    user_name = input("@username")

    # Text data analysis
    twitter_client= TwitterClient()
    api = twitter_client.get_twitter_client_api()

    tweet_analyzer = TweetAnalyzer()

    tweets = api.user_timeline(screen_name=user_name)

    df = tweet_analyzer.tweets_to_data_frame(tweets)

    df['date'].min()

     # join tweets to a single string
    words = ' '.join(df['tweets'])

    # remove URLs, RTs, and twitter handles
    no_urls_no_tags = " ".join([word for word in words.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'
                                ])
    # create a twitter-style mask for the wordcloud
    twitter_mask = custom_mask = np.array(Image.open('src/twitter_mask.jpeg'))

    # add some Croatian stopwords manually
    cro_stopwords = sw.english
                    
    STOPWORDS = STOPWORDS.union(cro_stopwords)

    # generate the wordcloud
    wordcloud = WordCloud(
                        stopwords = STOPWORDS,
                        background_color='white',
                        width=2000, 
                        height=2000, 
                        colormap='rainbow',
                        mask=twitter_mask,
                        contour_width = 3,
                        contour_color='blue'
                        ).generate(no_urls_no_tags)

    # set the figure size
    plt.figure(figsize=(15,15))

    # show the wordcloud
    #Plotting
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.show()


    # Likes Counts
    time_likes = pd.Series(data=df['likes'].values, index = df['date'])
    time_likes.plot(figsize=(16, 4), color='r')
    plt.show()


    # Retweets Count
    time_retweets = pd.Series(data=df['retweets'].values, index = df['date'])
    time_retweets.plot(figsize=(16, 4), color='r')
    plt.show()

    # Likes VS Retweets
    time_likes = pd.Series(data=df['likes'].values, index = df['date'])
    time_likes.plot(figsize=(16, 4), label='Likes', legend=True)

    time_retweets = pd.Series(data=df['retweets'].values, index = df['date'])
    time_retweets.plot(figsize=(16, 4), label='Retweets', legend=True)

    plt.show()


    # Visulize Network
    df = UserInteraction().get_most_interactives(user_name, 'main_user')
    user_df = df
    # Create graph
    graph = nx.DiGraph()
    # print "Adding followers relationships..."

    nodes = []
    nodes.append(user_name)

    for index, user_row in user_df.iterrows(): 
        graph.add_node(user_row["author"], size=100*100)
        value = int(user_row['mention_count'])
        graph.add_node(user_row["in_reply_to_screen_name"], size = value*value )

        graph.add_edge(user_row["author"], user_row["in_reply_to_screen_name"], weight = (user_row['mention_count']/10))

    for edge in nx.edge_betweenness(graph):
        friends_df = UserInteraction().get_most_interactives(edge[1], 'friend')

        for index, friend_row in friends_df.iterrows():
            if friend_row["in_reply_to_screen_name"] not in nx.nodes(graph):
                value = int(friend_row['mention_count'])
                graph.add_node(friend_row["in_reply_to_screen_name"], size = value*value )

            graph.add_edge(friend_row["author"], friend_row["in_reply_to_screen_name"], weight = (friend_row['mention_count']/10))

    # print "Saving the file as "+username+"-personal-network.gexf..."
    nx.write_gexf(graph, user_name+"-personal-network.gexf")
    sizes = list(nx.get_node_attributes(graph,'size').values())
    weights = list(nx.get_edge_attributes(graph,'weight').values())

    plt.figure(figsize=(30, 30))

    nx.draw_random(graph,
    arrows = False,
    arrowstyle = "fancy",
    with_labels=True,
    node_color="skyblue",
    edge_color = "blue", 
    font_size=25, 
    font_weight="bold",
    width = weights,
    node_size=sizes)

    plt.show()
   