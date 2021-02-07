SELECT pkey_para,
       sentences,
       LENGTH(sentences) AS 'NumCharsWithSpaces',
       LENGTH(REPLACE(sentences, ' ', '')) AS 'NumCharsNoSpaces',
       LENGTH(sentences) - LENGTH(REPLACE(sentences, ' ', ''))+1 AS 'NumTokens',
       CASE WHEN sum_matches > 0 THEN 1 ELSE 0 END 'MatchedToken'
       
FROM mutual_fund_lab.public_health_sentence_matches
WHERE LENGTH(sentences) - LENGTH(REPLACE(sentences, ' ', ''))+1 > 20;