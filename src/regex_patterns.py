import re



#### user_id pattern ################################

user_id_pattern = re.compile(r"""
   .*?(?:user[:=]?|user\s)?(?P<user>user\d{4}) 
""", re.VERBOSE)


#### timestamp pattern ################################

time_stamp_pattern = re.compile(r"""
    (?P<timestamp>                                              # Timestamps
        \d{4}-\d{2}-\d{2} \s \d{2}:\d{2}:\d{2}(?=::)?            # e.g., 2025-07-05 19:18:10
        |
        \d{2}/\d{2}/\d{4} \s \d{2}:\d{2}:\d{2}                   # e.g., 04/07/2025 01:08:12
    )
""", re.VERBOSE)


#### action pattern ################################

action_pattern = re.compile(r"""
       (?:did|action=|\*\*\*|::)?\s*                # non-capturing: possible preamble
    (?P<action>deposit|withdrawal|cashout|top-?up|purchase|debit|refund|transfer|purchase)  # the action     # deposite, withdrawal, refund
    
""", re.VERBOSE)


#### amount pattern ################################
amount_pattern = re.compile(r"""
    (?:amt[:=]?\s*|of\s+)?                # optional prefix
    (?:[€$£])?                            # optional non-captured currency
    (?P<amount>                           # named group (amount only)
        (?:\d{1,3}(?:,\d{3})*|\d+)        # integer part
        \.\d{1,2}                           # decimal part
    )
""", re.VERBOSE)


#### currency pattern ################################

currency_pattern = re.compile(r"""
        (?:\|\s*amt[:=]?\d+)? # optional prefix
        ([$€£])                 # currency symbol
        (?:\d+\s*)?                 #optional suffix
""", re.VERBOSE)


#### location pattern ################################

location_pattern = re.compile(r"""
        (?:\:\|\s*)?           # optional prefix
        (?P<location>london|glasgow|leeds|birmingham|liverpool|manchester|cardiff)                # location
        (?:\:\s*)?                 #optional suffix
""", re.VERBOSE)


#### device pattern ################################

device_pattern = re.compile(r"""
    (?:device\s*[:=]\s*|dev\s*[:=]\s*|\s*<\s*|\s*\:\:\s*|\s*\|\s*|\s+\b)
    (?P<device>(?!None\b)(?:iPhone|Samsung|Pixel|Nokia|Xiaomi|Huawei)(?:\s+(?:\d+|[A-Z]\w*))*)\b                   
""", re.VERBOSE | re.IGNORECASE)


#### atm pattern ################################

atm_pattern = re.compile(r"""
        atm            
""", re.VERBOSE | re.IGNORECASE)
