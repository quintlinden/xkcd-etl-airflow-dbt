{{ config(materialized='view') }} -- change to table, based on needs

WITH source AS (
  SELECT
    num,
    title,
    safe_title,
    printf('%04d-%02d-%02d', year, month, day) AS date, -- print in format to be recognized as date 
    img AS img_url,
    alt AS alt_text,
    transcript,
    LENGTH(title) * 5.0 AS cost,
    ABS(RANDOM() % 10000) AS views, -- recalculates them from scratch
    MIN(10.0, ROUND(1 + (ABS(RANDOM()) % 9) + (ABS(RANDOM()) % 10)/10.0, 1)) AS review_score
  FROM comics
)

SELECT * FROM source
