from facebook_business import FacebookSession
from facebook_business import FacebookAdsApi
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business.adobjects.adaccount import AdAccount
import datetime

# Facebook App Data
access_token = 'your_token'
app_secret = 'your_app_scret'
app_id = 'your_app_id'
ad_account_id = 'your_account'

# Setup session and api objects
session = FacebookSession(
    app_id,
    app_secret,
    access_token
)
api = FacebookAdsApi(session)
FacebookAdsApi.set_default_api(api)
me = AdUser(fbid='me')
# File to save output to
f = open('output.txt', 'a')

# Get the first account connected to the user
# my_account = me.get_ad_account()

# or get the account using the acc id
my_account = AdAccount(ad_account_id)


def print_and_output(string):
    print(string)
    f.write(string + '\n')


# Get user input for the time frame

possible_time_frames = ['today', 'yesterday', 'last_3d', 'last_7d', 'last_14d', 'last_28d', 'last_30d', 'last_90d',
                        'this_month', 'last_month', 'this_quarter', 'lifetime', 'last_week_mon_sun',
                        'last_week_sun_sat', 'last_quarter', 'last_year', 'this_week_mon_today', 'this_week_sun_today',
                        'this_year']
print('Possible time frames: ')
print(possible_time_frames)
time_frame = input('Enter desired time frame: ').strip()

if not any(i == time_frame for i in possible_time_frames):
    print('Input not found, defaulting to \'yesterday\'')
    time_frame = 'yesterday'

current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

print_and_output('\nDate and time: ' + current_time)

print_and_output('Time frame: ' + time_frame)

print_and_output('\nAccount stats: ')

account_spent = "None"
# Account Insights
account_fields = [
    AdsInsights.Field.account_currency,
    AdsInsights.Field.spend,
]
for stat in my_account.get_insights(params={
    'date_preset': time_frame
}, fields=account_fields):
    print_and_output('\t%s:\t%s' % ('Account currency', stat[AdsInsights.Field.account_currency]))
    try:
        account_spent = stat[AdsInsights.Field.spend]
        print_and_output('\t%s:\t%s' % ('Spent', stat[AdsInsights.Field.spend]))
    except:
        pass

final_data = {
    'account': {
        'account_id': ad_account_id,
        'account_spent': account_spent
    },
    'campaigns': [],
}
# Campaign Insights
campaign_fields = [
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.account_currency,
    AdsInsights.Field.spend,
    AdsInsights.Field.action_values,
]
print_and_output('\nCampaign stats: ')

# Get all campaigns
campaigns = my_account.get_insights(params={
    'level': 'campaign',
    'date_preset': time_frame,
    'fields': campaign_fields

})
# Extract values from received data
for idx, campaign in enumerate(campaigns):
    campaign_name = campaign[AdsInsights.Field.campaign_name]
    campaign_account_currency = campaign[AdsInsights.Field.account_currency]
    campaign_spent = "None"
    try:
        campaign_spent = campaign[AdsInsights.Field.spend]
    except:
        pass
    print_and_output('\t%s:\t%s' % ('Campaign name', campaign_name))
    print_and_output('\t%s:\t%s' % ('Account currency', campaign_account_currency))
    print_and_output('\t%s:\t%s' % ('Spent', campaign_spent))

    print_and_output('\tProduct conversion data: ')
    try:
        action_values = campaign[AdsInsights.Field.action_values]
    except:
        print_and_output('\t\tNo data\n')
        continue

    total = 0

    final_data['campaigns'].append({
        'campaign_name': campaign_name,
        'campaign_spent': campaign_spent,
        'campaign_action_values': []
    })

    for action in campaign[AdsInsights.Field.action_values]:
        action_type = 'None'
        action_value = 'None'
        try:
            action_type = action['action_type']
        except:
            pass

        try:
            action_value = action['value']
        except:
            pass
        print_and_output('\t\t%s:\t%s' % ('Action type', action_type))
        print_and_output('\t\t%s:\t%s' % ('Action value', action_value) + '\n')
        total += float(action_value)
        final_data['campaigns'][-1]['campaign_action_values'].append({
            'action_type': action_type,
            'action_value': action_value
        })

        print_and_output('\t\t%s:\t%s' % ('Conversion total', '{0:.2f}'.format(total)) + '\n')

print_and_output('____________________________________________')

###
# Close the output stream
f.close()
