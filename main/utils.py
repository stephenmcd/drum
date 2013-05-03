
from django.conf import settings
from django.utils.timezone import now


def order_by_score(queryset, score_fields, date_field, reverse=True):
    """
    Take some queryset (links or comments) and order them by score,
    which is basically "rating_sum / age_in_seconds ^ scale", where
    scale is a constant that can be used to control how quickly scores
    reduce over time. To perform this in the database, it needs to
    support a POW function, which Postgres and MySQL do. For databases
    that don't such as SQLite, we perform the scoring/sorting in
    memory, which will suffice for development.
    """

    scale = getattr(settings, "SCORE_SCALE_FACTOR", 2)

    # Timestamp SQL function snippets mapped to DB backends.
    # Defining these assumes the SQL functions POW() and NOW()
    # are available for the DB backend.
    timestamp_sqls = {
        "mysql": "UNIX_TIMESTAMP(%s)",
        "postgresql_psycopg2": "EXTRACT(EPOCH FROM %s)" ,
    }
    db_engine = settings.DATABASES[queryset.db]["ENGINE"].rsplit(".", 1)[1]
    timestamp_sql = timestamp_sqls.get(db_engine)

    if timestamp_sql:
        score_sql = "(%s) / POW(%s - %s, %s)" % (
            " + ".join(score_fields),
            timestamp_sql % "NOW()",
            timestamp_sql % date_field,
            scale,
        )
        order_by = "-score" if reverse else "score"
        return queryset.extra(select={"score": score_sql}).order_by(order_by)
    else:
        for obj in queryset:
            age = (now() - getattr(obj, date_field)).total_seconds()
            score_fields_sum = sum([getattr(obj, f) for f in score_fields])
            score = score_fields_sum / pow(age, scale)
            setattr(obj, "score", score)
        return sorted(queryset, key=lambda obj: obj.score, reverse=reverse)
