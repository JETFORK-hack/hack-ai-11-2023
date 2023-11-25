# SpellingChecker
cp -n ./resources/bigrams.txt ./src/backend/utils/spelling_checker/mount_files/symspell/bigrams.txt

# TopModel
cp -n ./resources/features_nov.pickle          ./src/backend/utils/top_model/resources/
cp -n ./resources/query_channel_hist.parquet   ./src/backend/utils/top_model/resources/
cp -n ./resources/query_hist.parquet           ./src/backend/utils/top_model/resources/
cp -n ./resources/query_video_rel.pickle       ./src/backend/utils/top_model/resources/
cp -n ./resources/video_query_rel_2.pickle     ./src/backend/utils/top_model/resources/
cp -n ./resources/video_query_rel.pickle       ./src/backend/utils/top_model/resources/
cp -n ./resources/ranker.ckpt                  ./src/backend/utils/top_model/resources/