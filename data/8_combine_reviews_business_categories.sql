WITH category_main AS ( 
	SELECT b.id as b_id, c.id, c.name 
	FROM phi_bi2cat b 
	INNER JOIN phi_category_v1 c
	ON b.catv1_id = c.id
), phi_bizcat AS (
	SELECT b.*, c.id, c.name FROM phi_business b
	INNER JOIN category_main c 
	ON b.id = c.b_id
), phi_data_all AS (
	SELECT 
		b.*, r.id as r_id, 
		r.review_id, r.user_id, r.date as r_date, r.text,
		r.stars, r.useful, r.funny, r.cool,
		ROW_NUMBER() OVER() as rn FROM phi_bizcat b 
	RIGHT JOIN phi_review r 
	ON b.business_id = r.business_id
	ORDER BY b.business_id
)

SELECT * FROM phi_data_all;

------ SELECT data in 4 chunks, this allows for piece wise download ------
---- File would be too big otherwise for csv format due to the large amount of data ----

-- SELECT * FROM phi_data_all
-- WHERE rn BETWEEN 1 and 242585

-- SELECT * FROM phi_data_all
-- WHERE rn BETWEEN 242586 and 485171

-- SELECT * FROM phi_data_all
-- WHERE rn BETWEEN 485172 and 727756

-- SELECT * FROM phi_data_all
-- WHERE rn > 727756