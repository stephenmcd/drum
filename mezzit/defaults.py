
from mezzanine.conf import register_setting


register_setting(
    name="RATINGS_RANGE",
    default=(-1, 1),
)

register_setting(
    name="RATINGS_ACCOUNT_REQUIRED",
    default=True,
)

register_setting(
    name="COMMENTS_ACCOUNT_REQUIRED",
    default=True,
)
