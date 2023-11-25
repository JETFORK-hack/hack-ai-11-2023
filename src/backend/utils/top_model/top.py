import pickle
from pathlib import Path
import re
import rapidfuzz
from yargy import Parser, rule, or_, and_
from yargy.predicates import (
    eq,
    type,
    normalized,
    gte,
    lte,
    dictionary,
)
from yargy.interpretation import fact
import pandas as pd
from catboost import CatBoostRanker
from yargy.interpretation import fact
import pandas as pd
import numpy as np

# from app.lifespan import global_objs


path = Path(__file__).parent.absolute()


DOT = eq(".")
INT = type("INT")
SPACE = eq(" ")


Date = fact("Date", ["year", "month", "day"])


MONTHS = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12,
}

MONTH_NAME = dictionary(MONTHS).interpretation(
    Date.month.normalized().custom(MONTHS.get)
)

MONTH = and_(INT, gte(1), lte(12)).interpretation(Date.month.custom(int))

YEAR = and_(INT, gte(1000), lte(3000)).interpretation(Date.year.custom(int))

YEAR_SUFFIX = rule(or_(eq("г"), normalized("год")), DOT.optional())

DAY = and_(INT, gte(1), lte(31)).interpretation(Date.day.custom(int))

DATE = or_(
    rule(YEAR, YEAR_SUFFIX),
    rule(MONTH_NAME, YEAR),
    rule(DAY, DOT.optional(), MONTH, DOT.optional(), YEAR),
    rule(YEAR, DOT.optional(), MONTH, DOT.optional(), DAY),
    rule(DAY, MONTH_NAME, YEAR),
)

DATE = rule(
    DATE,
).interpretation(Date)

nan_replacements = {
    "v_year_views": 0,
    "v_month_views": 0,
    "v_week_views": 0,
    "v_day_views": 0,
    "v_likes": 0,
    "v_dislikes": 0,
    "v_cr_click_like_7_days": 0,
    "v_cr_click_vtop_7_days": 0,
    "v_cr_click_long_view_7_days": 0,
    "v_cr_click_comment_7_days": 0,
    "v_cr_click_like_30_days": 0,
    "v_cr_click_vtop_30_days": 0,
    "v_cr_click_long_view_30_days": 0,
    "v_cr_click_comment_30_days": 0,
    "v_cr_click_like_1_days": 0,
    "v_cr_click_vtop_1_days": 0,
    "v_cr_click_long_view_1_days": 0,
    "v_cr_click_comment_1_days": 0,
    "query_video_avg_watchtime": 0,
    "query_video_avg_comment": 0,
    "query_video_num_clicks": 0,
    "query_channel_avg_watchtime": 0,
    "query_channel_num_clicks": 0,
    "mean_rel_video_per_query": 0,
    "mean_rel_query_per_video": 0,
    "mean_rel_tokens_per_video": 0,
}


class RankHunter:
    def __init__(self) -> None:
        self.date_parser = Parser(DATE)

        self.query_hist = pd.read_parquet(
            path / "resources/query_hist.parquet"
        ).rename(columns={"video_id": "id"})
        self.query_channel_hist = pd.read_parquet(
            path / "resources/query_channel_hist.parquet"
        ).rename(columns={"channel_title": "source_channel_title"})
        with open(path / "resources/query_video_rel.pickle", "rb") as handle:
            self.query_video_rel = pickle.load(handle)
        with open(path / "resources/video_query_rel.pickle", "rb") as handle:
            self.video_query_rel = pickle.load(handle)
        with open(path / "resources/video_query_rel_2.pickle", "rb") as handle:
            self.video_query_rel_2 = pickle.load(handle)
        with open(path / "resources/features_nov.pickle", "rb") as handle:
            self.video_features = pickle.load(handle)

        self.ranker = CatBoostRanker()
        self.ranker.load_model(path / "resources/ranker.ckpt")

        self.episode_re = re.compile(
            r"\d+ *(?:выпуск|серия|эпизод)|(?:выпуск|серия|эпизод) *\d+"
        )
        self.season_re = re.compile(r"\d+ *сезон|сезон *\d+")
        self.number_re = re.compile(r"\d+")

    def rerank(
        self, query: str, candidates: list[dict[str, str]], k: int = 5
    ) -> list[str]:
        df = pd.concat(
            [
                pd.DataFrame({"query": [query] * len(candidates)}),
                pd.DataFrame.from_records(candidates),
            ],
            axis=1,
        )
        df['clean_video_text'] = df['processed_video_title'].fillna('') + ' ' + df['processed_channel_title'].fillna('')
        df.drop(
            ["processed_video_title", "processed_channel_title"], axis=1, inplace=True
        )

        df["v_year_views"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_year_views", 0)
        )
        df["v_month_views"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_month_views", 0)
        )
        df["v_week_views"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_week_views", 0)
        )
        df["v_day_views"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_day_views", 0)
        )
        df["v_likes"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_likes", 0)
        )
        df["v_dislikes"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_dislikes", 0)
        )
        df["v_duration"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_duration", 0)
        )
        df["v_cr_click_like_7_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_like_7_days", 0)
        )
        df["v_cr_click_vtop_7_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_vtop_7_days", 0)
        )
        df["v_cr_click_long_view_7_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get(
                "v_cr_click_long_view_7_days", 0
            )
        )
        df["v_cr_click_comment_7_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_comment_7_days", 0)
        )
        df["v_cr_click_like_30_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_like_30_days", 0)
        )
        df["v_cr_click_vtop_30_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_vtop_30_days", 0)
        )
        df["v_cr_click_long_view_30_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get(
                "v_cr_click_long_view_30_days", 0
            )
        )
        df["v_cr_click_comment_30_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get(
                "v_cr_click_comment_30_days", 0
            )
        )
        df["v_cr_click_like_1_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_like_1_days", 0)
        )
        df["v_cr_click_vtop_1_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get("v_cr_click_vtop_1_days", 0)
        )
        df["v_cr_click_long_view_1_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get(
                "v_cr_click_long_view_1_days", 0
            )
        )
        df["v_cr_click_long_view_1_days"] = df["id"].apply(
            lambda x: self.video_features.get(x, {}).get(
                "v_cr_click_long_view_1_days", 0
            )
        )

        df["mean_rel_video_per_query"] = df["query"].apply(
            lambda x: self.query_video_rel.get(x, 0)
        )
        df["mean_rel_query_per_video"] = df["id"].apply(
            lambda x: self.video_query_rel.get(x, 0)
        )
        df["mean_rel_tokens_per_video"] = df["id"].apply(
            lambda x: self.video_query_rel_2.get(x, 0)
        )

        df = df.merge(self.query_hist, on=["id", "query"], how="left").merge(
            self.query_channel_hist, on=["source_channel_title", "query"], how="left"
        )
        df = df.fillna(nan_replacements)
        df["query_video/channel_avg_watchtime"] = (
            df["query_video_avg_watchtime"] / df["query_channel_avg_watchtime"]
        ).fillna(0)
        df["dosmostr"] = (df["query_video_avg_watchtime"] / df["v_duration"]).fillna(0)
        df["query_num_tokens"] = df["query"].str.split().apply(len)
        df.drop(
            ["query_video_avg_watchtime", "v_duration", "query_channel_avg_watchtime"],
            axis=1,
            inplace=True,
        )

        df["jaro_winkler"] = df.apply(
            lambda x: rapidfuzz.distance.JaroWinkler.normalized_similarity(
                x["query"], x["clean_video_text"]
            ),
            axis=1,
        )
        df["damerau_levenshtein"] = df.apply(
            lambda x: rapidfuzz.distance.DamerauLevenshtein.normalized_similarity(
                x["query"], x["clean_video_text"]
            ),
            axis=1,
        )
        df["date_similarity"] = df.apply(
            lambda x: self.match_dates(x["query"], x["clean_video_text"]), axis=1
        )
        df["same_episode"] = df.apply(
            lambda x: self.match_episodes(x["query"], x["clean_video_text"]), axis=1
        )
        df["same_season"] = df.apply(
            lambda x: self.match_season(x["query"], x["clean_video_text"]), axis=1
        )

        lookup = df["id"].values
        df.drop(
            ["clean_video_text", "source_channel_title", "query", "id"],
            axis=1,
            inplace=True,
        )

        df["group_id"] = [11991199] * df.shape[0]
        pred_scores = self.ranker.predict(df)

        return lookup[np.argsort(pred_scores)[::-1][:k]].tolist()


    def match_dates(self, query: str, video: str) -> float:
        res_query = self.date_parser.findall(query)
        spans_query = [_.span for _ in res_query]

        res_video = self.date_parser.findall(video)
        spans_video = [_.span for _ in res_video]

        if (not spans_query and spans_video) or (spans_query and not spans_video):
            return 0.0

        if not spans_query and not spans_video:
            return -1.0

        spans_query = query[spans_query[0].start : spans_query[0].stop]
        spans_video = video[spans_video[0].start : spans_video[0].stop]

        if spans_query == spans_video:
            return 1.0

        return len(set(spans_query) & set(spans_video)) / max(
            len(set(spans_query)), len(set(spans_query))
        )


    def match_episodes(self, query: str, video: str) -> float:
        res_query = self.episode_re.search(query)
        res_video = self.episode_re.search(query)

        if (not res_query and res_video) or (res_query and not res_video):
            return 0.0

        if not res_query and not res_video:
            return -1.0

        res_query = self.number_re.findall(res_query.group(0))[0]
        res_video = self.number_re.findall(res_video.group(0))[0]

        if res_query == res_video:
            return 1.0

        return 0.0


    def match_season(self, query: str, video: str) -> float:
        res_query = self.season_re.search(query)
        res_video = self.season_re.search(query)

        if (not res_query and res_video) or (res_query and not res_video):
            return 0.0

        if not res_query and not res_video:
            return -1.0

        res_query = self.number_re.findall(res_query.group(0))[0]
        res_video = self.number_re.findall(res_video.group(0))[0]

        if res_query == res_video:
            return 1.0

        return 0.0


