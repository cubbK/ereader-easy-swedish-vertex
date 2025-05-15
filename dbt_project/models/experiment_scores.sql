{{ config(materialized='table') }}

SELECT
  CAST(NULL AS FLOAT64) AS score,
  CAST(NULL AS STRING) AS experiment_id,
  CURRENT_TIMESTAMP() AS inserted_at
FROM UNNEST([1]) AS dummy
WHERE FALSE