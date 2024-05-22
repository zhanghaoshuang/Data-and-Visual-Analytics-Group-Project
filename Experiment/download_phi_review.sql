COPY (
SELECT *
FROM phi_review
)
TO 'C:\Hal\Data Science Masters- GT\2024 Spring\CSE6242- Data and Visual Analytics\Project\Demand Score\Current Data\phi_review.csv' DELIMITER ',' CSV HEADER;