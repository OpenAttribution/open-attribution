from quixstreams import Application

# Connect to your kafka client
app = Application(
    broker_address="localhost:9092", consumer_group="consumer-impressions"
)

impression_input_topic = app.topic("impressions")
click_input_topic = app.topic("clicks")
event_input_topic = app.topic("events")

impressions_df = app.dataframe(topic=impression_input_topic)
clicks_df = app.dataframe(topic=click_input_topic)
events_df = app.dataframe(topic=event_input_topic)

impressions_df = impressions_df.update(
    lambda value: print("Received impression:", value)
)

clicks_df = clicks_df.update(lambda value: print("Received click:", value))
clicks_df = clicks_df.update(
    lambda value: print("Received click:", value["ifa"] in impressions_df["ifa"])
)


events_df["campaign_name"] = events_df.update(
    lambda value: impressions_df[impressions_df["ifa"].isin(value["ifa"])]
    .sort_values("__time", descending=True)["campaign_name"]
    .values[0]
)


if __name__ == "__main__":
    app.run(events_df)
