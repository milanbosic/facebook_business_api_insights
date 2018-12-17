# Facebook Business API Account and Campaign Insights
Python script that utilizes the Facebook Business API to get stats for the relevant Facebook Ad account and its campaigns, and output and save to a file. Ability to enter desired time frame via console.

## Facebook Session
Change the starting parameters (access token, app secret, app id, and account id) to your values.

Only the first three parameters are necessary to start the session, since you can call me.get_ad_accounts() and choose the account you want.

## Query fields
Choose which account fields you want to retrieve with the request:

```python
# Account Insights example
account_fields = [
    AdsInsights.Field.account_currency,
    AdsInsights.Field.spend,
]
```

and similar for Campaigns:

```python
# Campaign Insights example
campaign_fields = [
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.account_currency,
    AdsInsights.Field.spend,
    AdsInsights.Field.action_values,
]
```
Available fields:

[Account](https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/)

[Campaign](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group/insights/)

## Retrieved data
Data is stored in a dictionary called final_data. If you've changed the field arguments, you need to add it to the dictionary.

