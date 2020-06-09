FROM koursaros/nboost:latest-pt

RUN nboost                                  \
    --uhost es                   \
    --uport 9200                        \
    --search_route "/wikipedia/search"   \
    --query_path url.query.q            \
    --topk_path url.query.size          \
    --default_topk 10                   \
    --choices_path body.hits.hits       \
    --cvalues_path _source.text

