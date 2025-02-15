from enum import Enum

__all__ = (
    "ContentType",
    "Visibility",
    "RankingMode",
    "SearchTarget",
    "Sort",
    "Duration",
)


class ContentType(str, Enum):
    ILLUSTRATION = "illust"
    MANGA = "manga"


class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class RankingMode(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    DAY_MALE = "day_male"
    DAY_FEMALE = "day_female"
    WEEK_ORIGINAL = "week_original"
    WEEK_ROOKIE = "week_rookie"
    DAY_MANGA = "day_manga"
    DAY_R18 = "day_r18"
    DAY_MALE_R18 = "day_male_r18"
    DAY_FEMALE_R18 = "day_female_r18"
    WEEK_R18 = "week_r18"
    WEEK_R18G = "week_r18g"


class SearchTarget(str, Enum):
    PARTIAL_MATCH_FOR_TAGS = "partial_match_for_tags"
    EXACT_MATCH_FOR_TAGS = "exact_match_for_tags"
    TITLE_AND_CAPTION = "title_and_caption"
    KEYWORD = "keyword"


class Sort(str, Enum):
    DATE_DESC = "date_desc"
    DATE_ASC = "date_asc"
    POPULAR_DESC = "popular_desc"


class Duration(str, Enum):
    WITHIN_LAST_DAY = "within_last_day"
    WITHIN_LAST_WEEK = "within_last_week"
    WITHIN_LAST_MONTH = "within_last_month"
