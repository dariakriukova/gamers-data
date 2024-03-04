# Answers

# Gender ratio in each game

## Short Answer

**For WWC:**

- Women: Approximately 53.16%
- Men: Approximately 46.84%

**For HB:**

- Women: 50.7%
- Men: 49.3%

## Long Answer

To calculate the gender ratio in each game directly through SQL, I used the following queries:

**For Wild Wild Chords (WWC):**

```sql
SELECT 
    gender, 
    COUNT(*) as count,
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users WHERE wwc = true)) as percentage
FROM users
WHERE wwc = true
GROUP BY gender;
```

**For HarmonicaBots (HB):**

```sql
SELECT 
    gender, 
    COUNT(*) as count,
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users WHERE hb = true)) as percentage
FROM users
WHERE hb = true
GROUP BY gender;
```

These queries count the number of users by gender for each game and also calculate the percentage of each gender within the game directly. This approach minimizes the need for external calculations.

# The youngest and the oldest players per country

## Short Answer

| nationality | youngest_first_name | youngest_second_name | youngest_age | oldest_first_name | oldest_first_name | oldest_age |
| --- | --- | --- | --- | --- | --- | --- |
| au | dwayne | andrews | 28 | roberto | myers | 79 |
| br | alcina | almeida | 28 | helga | nogueira | 79 |
| ca | blake | grewal | 29 | marilou | margaret | 79 |
| ch | sophia | hubert | 29 | alexis | brun | 78 |
| de | thea | reimann | 28 | luka | kirsch | 79 |
| dk | NULL | petersen | 29 | thea | olsen | 79 |
| es | fernando | diaz | 28 | marc | saez | 77 |
| fi | mikael | lakso | 29 | luukas | nikula | 76 |
| fr | elea | garnier | 28 | ambre | pierre | 79 |
| gb | rachel | barnes | 30 | holly | white | 78 |
| ie | jeremy | caldwell | 29 | julie | matthews | 79 |
| ir | hly | ysmy | 28 | bhrh | kmyrn | 76 |
| nl | joy | vermeeren | 29 | melda | bekkema | 79 |
| nz | luke | hall | 29 | madeleine | brown | 77 |
| tr | deniz | asikoglu | 28 | deniz | abaci | 77 |
| us | colleen | morrison | 30 | katherine | evans | 78 |

## Long Answer

Users’s nationalities were used as proxies for country identification. The dataset lacks explicit country information for users. The easiest way would be to use their nationalities for this analysis. Also direct age information is not available, so it’s calculated  from the age based on the date of birth (dob).

```sql
WITH age_calculation AS (
    SELECT 
        id,
        first_name,
        last_name,
        nationality,
        dob,
        (strftime('%Y', 'now') - strftime('%Y', dob)) - (strftime('%m-%d', 'now') < strftime('%m-%d', dob)) AS age
    FROM 
        users
)
SELECT 
    youngest.nationality,
    youngest.first_name AS youngest_first_name,
    youngest.last_name AS youngest_last_name,
    youngest.age AS youngest_age,
    oldest.first_name AS oldest_first_name,
    oldest.last_name AS oldest_last_name,
    oldest.age AS oldest_age
FROM 
    (SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY nationality ORDER BY age) AS rank_youngest
     FROM 
        age_calculation) AS youngest
JOIN 
    (SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY nationality ORDER BY age DESC) AS rank_oldest
     FROM 
        age_calculation) AS oldest
ON 
    youngest.nationality = oldest.nationality
    AND youngest.rank_youngest = 1
    AND oldest.rank_oldest = 1;
```

1. 

# How to make the data pipeline faster, more scalable and more reliable?

## Optimize Database Design

Instead of using boolean columns to track game participation, the separate Games table can be created and have many-to-many relationship with Users table. This approach allows for more flexible querying, and accommodates future scalability where users can participate in multiple games.

## Improve Normalization

The "state" field's free-form nature has led to inconsistencies, such as multiple entries for the same geographical location due to variety of namings. For example, there are 2 records with city=“Helsinki”, however one of them has state=”Uuusimaa” and the other “Proper Finland”. There are several approaches can be used to address it:

- Python library**`pgeocode`** can translate postal codes into geographical data, so that states and countries can be identified.
- More complex solution would be to implement natural language processing techniques to normalize and standardize location names.
- Let users to select within provided options their region based on the other information, like Street address, country, postal code. This is not solving a problem with existing data sources, but improves the future experience.
- A curated dictionary of known aliases and corrections for commonly misreported locations can be used as well, however it’s not the most scalable approach.

## Use Generator

Python's generators can be used to improve the memory usage. Generator will iterate over the input file without loading the entire dataset into memory at once and save then into a warehouse in small batches. For the sample data sources I’ve got it’s not an issue, but with bigger volumes the system may run out of memory.

## Concurrency control

In case there are several the data pipeline across multiple Docker containers are being deployed, concurrency control has to be done to prevent data corruption and ensure data integrity. 

# A list of principles to follow when developing an event pipeline

1. Start with the simplest solution that works and easily maintainable. Then add up more if there is a need.
2. Handle errors properly and implement possibility to recover data in case of failure.
3. Use technologies that can scaled for the future development.
4. Use real time event processing to have **a r**esponsive and up-to-date system.
5. Properly validate the data quality.
6. Setup monitoring and alert for the pipeline.
7. Make proper tests under various conditions.