
from django.conf import settings
from django.utils.timezone import now


def with_users(queryset):
    """
    Wraps the queryset with select_related args for loading users
    and their profiles when querying links and comments.
    """
    return queryset.select_related("user", "user__profile")


def order_by_score(queryset, date_field, reverse=True, db_scoring=True):
    """
    Take some queryset (links or comments) and orders them by score,
    which is basically "rating_sum / age_in_seconds ^ scale", where
    scale is a constant that can be used to control how quickly scores
    reduce over time. To perform this in the database, it needs to
    support a POW function, which Postgres and MySQL do. For databases
    that don't such as SQLite, we perform the scoring/sorting in
    memory, which will suffice for development.
    """

    scale = getattr(settings, "SCORE_SCALE_FACTOR", 2)

    # Timestamp SQL function snippets mapped to DB backends.
    # Defining these assumes the SQL fucntions POW() and NOW()
    # are available for the db backend.
    db_engine = settings.DATABASES[queryset.db]["ENGINE"].rsplit(".", 1)[1]
    timestamp_sql = {
        "mysql": "UNIX_TIMESTAMP(%s)",
        "postgresql_psycopg2": "EXTRACT(EPOCH FROM %s)" ,
    }.get(db_engine)

    # db_scoring arg allows us to explicitly skip db sorting
    # if desired, eg for testing.
    if timestamp_sql and db_scoring:
        now_sql = timestamp_sql % "NOW()"
        age_sql = timestamp_sql % date_field
        score_sql = "rating_sum / POW(%s - %s, %s)" % (now_sql, age_sql, scale)
        order_by = "-score" if reverse else "score"
        return queryset.extra(select={"score": score_sql}).order_by(order_by)
    else:
        for obj in queryset:
            age = (now() - getattr(obj, date_field)).total_seconds()
            score = obj.rating_sum / pow(age, scale)
            setattr(obj, "score", score)
        return sorted(queryset, key=lambda obj: obj.score, reverse=reverse)
