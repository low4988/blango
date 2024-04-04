from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# We’ll set up sustained and burst limits for 
# both authorized and anonymous users
# in settings.py REST_FRAMEWORK{} import these as  
# DEFAULT_THROTTLE_CLASSES: [
# "blog.api.throttling.AnonSustainedThrottle",]
# and define rates
#"DEFAULT_THROTTLE_RATES": 
# {"anon_sustained": "500/day",}
class AnonSustainedThrottle(AnonRateThrottle):
    scope = "anon_sustained"


class AnonBurstThrottle(AnonRateThrottle):
    scope = "anon_burst"


class UserSustainedThrottle(UserRateThrottle):
    scope = "user_sustained"


class UserBurstThrottle(UserRateThrottle):
    scope = "user_burst"