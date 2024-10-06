# https://www.imdb.com/chart/top/ as of 10/5/2024
import re
import csv

def extract_movie_data(movie_string):
    movie_title = None
    lines = movie_string.split('\n')

    # Extract movie title from the first line with number
    data = []
    for idx, line in enumerate(lines):
        match = re.search(r'^(\d+)\. (.+)', line)
        if match:
            movie_title = match.group(2).strip()
            year = lines[idx + 1]            
            data.append({
                'Movie Title': movie_title,
                'Year': year
            })

    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Movie Title', 'Year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            if entry is not None:
                writer.writerow(entry)

movie_string = """
Tim Robbins in The Shawshank Redemption (1994)
1. The Shawshank Redemption
1994
2h 22m
R
9.3
 (2.9M)

Marlon Brando in The Godfather (1972)
2. The Godfather
1972
2h 55m
R
9.2
 (2.1M)

Christian Bale in The Dark Knight (2008)
3. The Dark Knight
2008
2h 32m
PG-13
9.0
 (2.9M)

Al Pacino in The Godfather Part II (1974)
4. The Godfather Part II
1974
3h 22m
R
9.0
 (1.4M)

Henry Fonda, Martin Balsam, Jack Klugman, Lee J. Cobb, Ed Begley, Edward Binns, John Fiedler, E.G. Marshall, Joseph Sweeney, George Voskovec, Jack Warden, and Robert Webber in 12 Angry Men (1957)
5. 12 Angry Men
1957
1h 36m
Approved
9.0
 (886K)

Liv Tyler, Sean Astin, Elijah Wood, Viggo Mortensen, Ian McKellen, and Andy Serkis in The Lord of the Rings: The Return of the King (2003)
6. The Lord of the Rings: The Return of the King
2003
3h 21m
PG-13
9.0
 (2M)

Schindler's List (1993)
7. Schindler's List
1993
3h 15m
R
9.0
 (1.5M)

Uma Thurman in Pulp Fiction (1994)
8. Pulp Fiction
1994
2h 34m
R
8.9
 (2.3M)

Liv Tyler, Sean Astin, Sean Bean, Elijah Wood, Cate Blanchett, Viggo Mortensen, Ian McKellen, Orlando Bloom, Billy Boyd, Dominic Monaghan, and John Rhys-Davies in The Lord of the Rings: The Fellowship of the Ring (2001)
9. The Lord of the Rings: The Fellowship of the Ring
2001
2h 58m
PG-13
8.9
 (2M)

The Good, the Bad and the Ugly (1966)
10. The Good, the Bad and the Ugly
1966
2h 58m
R
8.8
 (826K)

Tom Hanks in Forrest Gump (1994)
11. Forrest Gump
1994
2h 22m
PG-13
8.8
 (2.3M)

Liv Tyler, Sean Astin, Christopher Lee, Elijah Wood, Viggo Mortensen, Miranda Otto, Ian McKellen, Orlando Bloom, John Rhys-Davies, and Andy Serkis in The Lord of the Rings: The Two Towers (2002)
12. The Lord of the Rings: The Two Towers
2002
2h 59m
PG-13
8.8
 (1.8M)

Brad Pitt and Edward Norton in Fight Club (1999)
13. Fight Club
1999
2h 19m
R
8.8
 (2.4M)

Leonardo DiCaprio, Tom Berenger, Michael Caine, Lukas Haas, Marion Cotillard, Joseph Gordon-Levitt, Tom Hardy, Elliot Page, Ken Watanabe, and Dileep Rao in Inception (2010)
14. Inception
2010
2h 28m
PG-13
8.8
 (2.6M)

Harrison Ford, Anthony Daniels, Carrie Fisher, Mark Hamill, James Earl Jones, David Prowse, Kenny Baker, and Peter Mayhew in Star Wars: Episode V - The Empire Strikes Back (1980)
15. Star Wars: Episode V - The Empire Strikes Back
1980
2h 4m
PG
8.7
 (1.4M)

Keanu Reeves, Laurence Fishburne, Joe Pantoliano, and Carrie-Anne Moss in The Matrix (1999)
16. The Matrix
1999
2h 16m
R
8.7
 (2.1M)

Robert De Niro, Ray Liotta, and Joe Pesci in Goodfellas (1990)
17. Goodfellas
1990
2h 25m
R
8.7
 (1.3M)

Jack Nicholson in One Flew Over the Cuckoo's Nest (1975)
18. One Flew Over the Cuckoo's Nest
1975
2h 13m
R
8.7
 (1.1M)

Matthew McConaughey in Interstellar (2014)
19. Interstellar
2014
2h 49m
PG-13
8.7
 (2.2M)

Brad Pitt and Morgan Freeman in Se7en (1995)
20. Se7en
1995
2h 7m
R
8.6
 (1.8M)

James Stewart and Donna Reed in It's a Wonderful Life (1946)
21. It's a Wonderful Life
1946
2h 10m
PG
8.6
 (506K)

Seven Samurai (1954)
22. Seven Samurai
1954
3h 27m
Not Rated
8.6
 (372K)

Jodie Foster in The Silence of the Lambs (1991)
23. The Silence of the Lambs
1991
1h 58m
R
8.6
 (1.6M)

Tom Hanks, Matt Damon, Tom Sizemore, and Edward Burns in Saving Private Ryan (1998)
24. Saving Private Ryan
1998
2h 49m
R
8.6
 (1.5M)

Inhabitants of Belo Vale Boa Morte and Cidade de Congonhas and Paige Ellens in City of God (2002)
25. City of God
2002
2h 10m
R
8.6
 (814K)

Roberto Benigni, Nicoletta Braschi, and Giorgio Cantarini in Life Is Beautiful (1997)
26. Life Is Beautiful
1997
1h 56m
PG-13
8.6
 (755K)

Movie Poster
27. The Green Mile
1999
3h 9m
R
8.6
 (1.4M)

Arnold Schwarzenegger in Terminator 2: Judgment Day (1991)
28. Terminator 2: Judgment Day
1991
2h 17m
R
8.6
 (1.2M)

Anthony Daniels, Carrie Fisher, Mark Hamill, James Earl Jones, David Prowse, and Kenny Baker in Star Wars: Episode IV - A New Hope (1977)
29. Star Wars: Episode IV - A New Hope
1977
2h 1m
PG
8.6
 (1.5M)

Michael J. Fox in Back to the Future (1985)
30. Back to the Future
1985
1h 56m
PG
8.5
 (1.3M)

Spirited Away (2001)
31. Spirited Away
2001
2h 4m
PG
8.6
 (873K)

The Pianist (2002)
32. The Pianist
2002
2h 30m
R
8.5
 (933K)

Song Kang-ho, Jung Ik-han, Jung Hyun-jun, Lee Joo-hyung, Lee Ji-hye, Lee Sun-kyun, Cho Yeo-jeong, Park Myeong-hoon, Park Keun-rok, Jang Hye-jin, Lee Jeong-eun, Choi Woo-sik, Park Seo-joon, Park So-dam, and Jung Ji-so in Parasite (2019)
33. Parasite
2019
2h 12m
R
8.5
 (997K)

Anthony Perkins, John Gavin, Janet Leigh, and Heather Dawn May in Psycho (1960)
34. Psycho
1960
1h 49m
R
8.5
 (731K)

Russell Crowe in Gladiator (2000)
35. Gladiator
2000
2h 35m
R
8.5
 (1.7M)

Matthew Broderick in The Lion King (1994)
36. The Lion King
1994
1h 28m
G
8.5
 (1.2M)

Oscar Isaac, Andy Samberg, Jake Johnson, Daniel Kaluuya, Hailee Steinfeld, Karan Soni, Shameik Moore, and Issa Rae in Spider-Man: Across the Spider-Verse (2023)
37. Spider-Man: Across the Spider-Verse
2023
2h 20m
PG
8.6
 (405K)

Leonardo DiCaprio, Jack Nicholson, and Matt Damon in The Departed (2006)
38. The Departed
2006
2h 31m
R
8.5
 (1.4M)

J.K. Simmons and Miles Teller in Whiplash (2014)
39. Whiplash
2014
1h 46m
R
8.5
 (1M)

Edward Norton in American History X (1998)
40. American History X
1998
1h 59m
R
8.5
 (1.2M)

Corinne Orr, Ayano Shiraishi, Tsutomu Tatsumi, J. Robert Spencer, Emily Neves, and Adam Gibbs in Grave of the Fireflies (1988)
41. Grave of the Fireflies
1988
1h 28m
Not Rated
8.5
 (323K)

Natalie Portman and Jean Reno in Léon: The Professional (1994)
42. Léon: The Professional
1994
1h 50m
R
8.5
 (1.3M)

Christian Bale, Hugh Jackman, and Scarlett Johansson in The Prestige (2006)
43. The Prestige
2006
2h 10m
PG-13
8.5
 (1.5M)

Harakiri (1962)
44. Harakiri
1962
2h 13m
Not Rated
8.6
 (72K)

Javier Bardem, Josh Brolin, Stellan Skarsgård, Rebecca Ferguson, Dave Bautista, Austin Butler, Timothée Chalamet, Zendaya, Florence Pugh, and Souheila Yacoub in Dune: Part Two (2024)
45. Dune: Part Two
2024
2h 46m
PG-13
8.5
 (524K)

Kevin Spacey, Stephen Baldwin, Gabriel Byrne, Benicio Del Toro, and Kevin Pollak in The Usual Suspects (1995)
46. The Usual Suspects
1995
1h 46m
R
8.5
 (1.2M)

Ingrid Bergman, Humphrey Bogart, Peter Lorre, Claude Rains, Sydney Greenstreet, Paul Henreid, and Conrad Veidt in Casablanca (1942)
47. Casablanca
1942
1h 42m
PG
8.5
 (615K)

François Cluzet and Omar Sy in The Intouchables (2011)
48. The Intouchables
2011
1h 52m
R
8.5
 (947K)

Cinema Paradiso (1988)
49. Cinema Paradiso
1988
2h 54m
PG
8.5
 (289K)

Charles Chaplin in Modern Times (1936)
50. Modern Times
1936
1h 27m
G
8.5
 (264K)

Alien (1979)
51. Alien
1979
1h 57m
R
8.5
 (983K)

Grace Kelly, James Stewart, Georgine Darcy, Judith Evelyn, and Harry Landers in Rear Window (1954)
52. Rear Window
1954
1h 52m
PG
8.5
 (531K)

Once Upon a Time in the West (1968)
53. Once Upon a Time in the West
1968
2h 46m
PG-13
8.5
 (354K)

Leonardo DiCaprio, Jamie Foxx, and Christoph Waltz in Django Unchained (2012)
54. Django Unchained
2012
2h 45m
R
8.5
 (1.7M)

Charles Chaplin in City Lights (1931)
55. City Lights
1931
1h 27m
G
8.5
 (199K)

Marlon Brando and Martin Sheen in Apocalypse Now (1979)
56. Apocalypse Now
1979
2h 27m
R
8.4
 (722K)

Guy Pearce and Carrie-Anne Moss in Memento (2000)
57. Memento
2000
1h 53m
R
8.4
 (1.3M)

WALL·E (2008)
58. WALL·E
2008
1h 38m
G
8.4
 (1.2M)

Harrison Ford, Karen Allen, Paul Freeman, Wolf Kahler, Ronald Lacey, and Terry Richards in Raiders of the Lost Ark (1981)
59. Raiders of the Lost Ark
1981
1h 55m
PG
8.4
 (1.1M)

Vikrant Massey in 12th Fail (2023)
60. 12th Fail
2023
2h 27m
8.8
 (130K)

Martina Gedeck, Sebastian Koch, and Ulrich Mühe in The Lives of Others (2006)
61. The Lives of Others
2006
2h 17m
R
8.4
 (416K)

William Holden, Nancy Olson, and Gloria Swanson in Sunset Boulevard (1950)
62. Sunset Boulevard
1950
1h 50m
Approved
8.4
 (240K)

Don Cheadle, Robert Downey Jr., Josh Brolin, Vin Diesel, Paul Bettany, Bradley Cooper, Chris Evans, Sean Gunn, Scarlett Johansson, Elizabeth Olsen, Chris Pratt, Mark Ruffalo, Zoe Saldana, Benedict Wong, Terry Notary, Anthony Mackie, Chris Hemsworth, Dave Bautista, Benedict Cumberbatch, Chadwick Boseman, Sebastian Stan, Danai Gurira, Karen Gillan, Pom Klementieff, Letitia Wright, and Tom Holland in Avengers: Infinity War (2018)
63. Avengers: Infinity War
2018
2h 29m
PG-13
8.4
 (1.2M)

Kirk Douglas in Paths of Glory (1957)
64. Paths of Glory
1957
1h 28m
Approved
8.4
 (217K)

Spider-Man: Into the Spider-Verse (2018)
65. Spider-Man: Into the Spider-Verse
2018
1h 57m
PG
8.4
 (694K)

Witness for the Prosecution (1957)
66. Witness for the Prosecution
1957
1h 56m
Approved
8.4
 (141K)

The Shining (1980)
67. The Shining
1980
2h 26m
R
8.4
 (1.1M)

Charles Chaplin and Paulette Goddard in The Great Dictator (1940)
68. The Great Dictator
1940
2h 5m
G
8.4
 (241K)

Sigourney Weaver and Carrie Henn in Aliens (1986)
69. Aliens
1986
2h 17m
R
8.4
 (786K)

Brad Pitt, Til Schweiger, Daniel Brühl, Mélanie Laurent, Eli Roth, Christoph Waltz, and Diane Kruger in Inglourious Basterds (2009)
70. Inglourious Basterds
2009
2h 33m
R
8.4
 (1.6M)

Morgan Freeman, Gary Oldman, Christian Bale, Michael Caine, Matthew Modine, Anne Hathaway, Marion Cotillard, and Joseph Gordon-Levitt in The Dark Knight Rises (2012)
71. The Dark Knight Rises
2012
2h 44m
PG-13
8.4
 (1.9M)

Alfonso Arau, Benjamin Bratt, Alanna Ubach, Gael García Bernal, Dyana Ortelli, Herbert Siguenza, and Anthony Gonzalez in Coco (2017)
72. Coco
2017
1h 45m
PG
8.4
 (614K)

Amadeus (1984)
73. Amadeus
1984
2h 40m
PG
8.4
 (435K)

Tom Hanks, R. Lee Ermey, Tim Allen, Annie Potts, John Ratzenberger, Wallace Shawn, Jim Varney, and Don Rickles in Toy Story (1995)
74. Toy Story
1995
1h 21m
G
8.3
 (1.1M)

Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1964)
75. Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb
1964
1h 35m
PG
8.3
 (526K)

Oldboy (2003)
76. Oldboy
2003
2h
R
8.3
 (652K)

Kevin Spacey, Thora Birch, Mena Suvari, and Wes Bentley in American Beauty (1999)
77. American Beauty
1999
2h 2m
R
8.3
 (1.2M)

Don Cheadle, Robert Downey Jr., Josh Brolin, Bradley Cooper, Chris Evans, Sean Gunn, Scarlett Johansson, Brie Larson, Jeremy Renner, Paul Rudd, Mark Ruffalo, Chris Hemsworth, Danai Gurira, and Karen Gillan in Avengers: Endgame (2019)
78. Avengers: Endgame
2019
3h 1m
PG-13
8.4
 (1.3M)

Das Boot (1981)
79. Das Boot
1981
2h 29m
8.4
 (268K)

Mel Gibson in Braveheart (1995)
80. Braveheart
1995
2h 58m
R
8.3
 (1.1M)

Robin Williams and Matt Damon in Good Will Hunting (1997)
81. Good Will Hunting
1997
2h 6m
R
8.3
 (1.1M)

Claire Danes and Yuriko Ishida in Princess Mononoke (1997)
82. Princess Mononoke
1997
2h 13m
PG-13
8.3
 (444K)

Joaquin Phoenix in Joker (2019)
83. Joker
2019
2h 2m
R
8.4
 (1.5M)

Your Name. (2016)
84. Your Name.
2016
1h 46m
8.4
 (335K)

Toshirô Mifune, Kenjirô Ishiyama, Kyôko Kagawa, Tatsuya Mihashi, and Tatsuya Nakadai in High and Low (1963)
85. High and Low
1963
2h 23m
Not Rated
8.4
 (55K)

Sharman Joshi, Aamir Khan, and Madhavan in 3 Idiots (2009)
86. 3 Idiots
2009
2h 50m
PG-13
8.4
 (444K)

Robert De Niro, James Woods, William Forsythe, Brian Bloom, Adrian Curran, James Hayden, Rusty Jacobs, and Scott Tiler in Once Upon a Time in America (1984)
87. Once Upon a Time in America
1984
3h 49m
R
8.3
 (384K)

Gene Kelly, Debbie Reynolds, and Donald O'Connor in Singin' in the Rain (1952)
88. Singin' in the Rain
1952
1h 43m
G
8.3
 (265K)

Capernaum (2018)
89. Capernaum
2018
2h 6m
R
8.4
 (109K)

Aleksey Kravchenko in Come and See (1985)
90. Come and See
1985
2h 22m
Not Rated
8.4
 (102K)

Jennifer Connelly in Requiem for a Dream (2000)
91. Requiem for a Dream
2000
1h 42m
NC-17
8.3
 (915K)

Tom Hanks, Joan Cusack, Tim Allen, John Ratzenberger, Wallace Shawn, Jodi Benson, Blake Clark, Estelle Harris, Jeff Pidgeon, Don Rickles, and Frank Welker in Toy Story 3 (2010)
92. Toy Story 3
2010
1h 43m
G
8.3
 (907K)

Harrison Ford, Carrie Fisher, Mark Hamill, James Earl Jones, Warwick Davis, David Prowse, Billy Dee Williams, Michael Carter, and Larry Ward in Star Wars: Episode VI - Return of the Jedi (1983)
93. Star Wars: Episode VI - Return of the Jedi
1983
2h 11m
PG
8.3
 (1.1M)

Jim Carrey and Kate Winslet in Eternal Sunshine of the Spotless Mind (2004)
94. Eternal Sunshine of the Spotless Mind
2004
1h 48m
R
8.3
 (1.1M)

Mads Mikkelsen in The Hunt (2012)
95. The Hunt
2012
1h 55m
R
8.3
 (373K)

2001: A Space Odyssey (1968)
96. 2001: A Space Odyssey
1968
2h 29m
G
8.3
 (732K)

Takashi Shimura in Ikiru (1952)
97. Ikiru
1952
2h 23m
Not Rated
8.3
 (90K)

Steve Buscemi, Harvey Keitel, Michael Madsen, Tim Roth, and Chris Penn in Reservoir Dogs (1992)
98. Reservoir Dogs
1992
1h 39m
R
8.3
 (1.1M)

Alec Guinness, Anthony Quinn, Peter O'Toole, José Ferrer, and Jack Hawkins in Lawrence of Arabia (1962)
99. Lawrence of Arabia
1962
3h 47m
PG
8.3
 (320K)

Jack Lemmon and Shirley MacLaine in The Apartment (1960)
100. The Apartment
1960
2h 5m
Approved
8.3
 (201K)

Mélissa Désormeaux-Poulin in Incendies (2010)
101. Incendies
2010
2h 11m
R
8.3
 (211K)

Al Pacino in Scarface (1983)
102. Scarface
1983
2h 50m
R
8.3
 (935K)

Cary Grant, Alfred Hitchcock, Eva Marie Saint, and Philip Ober in North by Northwest (1959)
103. North by Northwest
1959
2h 16m
Approved
8.3
 (351K)

Edward G. Robinson, Barbara Stanwyck, and Fred MacMurray in Double Indemnity (1944)
104. Double Indemnity
1944
1h 47m
Approved
8.3
 (170K)

Orson Welles, Dorothy Comingore, and Ruth Warrick in Citizen Kane (1941)
105. Citizen Kane
1941
1h 59m
PG
8.3
 (472K)

Cillian Murphy in Oppenheimer (2023)
106. Oppenheimer
2023
3h
R
8.3
 (801K)

M (1931)
107. M
1931
1h 39m
Passed
8.3
 (171K)

Vertigo (1958)
108. Vertigo
1958
2h 8m
PG
8.3
 (435K)

Full Metal Jacket (1987)
109. Full Metal Jacket
1987
1h 56m
R
8.2
 (803K)

Robert De Niro, Val Kilmer, Al Pacino, Ted Levine, Wes Studi, Jerry Trimble, and Mykelti Williamson in Heat (1995)
110. Heat
1995
2h 50m
R
8.3
 (733K)

Audrey Tautou in Amélie (2001)
111. Amélie
2001
2h 2m
R
8.3
 (804K)

Edward Asner, Bob Peterson, and Jordan Nagai in Up (2009)
112. Up
2009
1h 36m
PG
8.3
 (1.1M)

Malcolm McDowell in A Clockwork Orange (1971)
113. A Clockwork Orange
1971
2h 16m
R
8.2
 (893K)

Gregory Peck, Mary Badham, and Phillip Alford in To Kill a Mockingbird (1962)
114. To Kill a Mockingbird
1962
2h 9m
Approved
8.3
 (337K)

Leila Hatami and Payman Maadi in A Separation (2011)
115. A Separation
2011
2h 3m
PG-13
8.3
 (262K)

Paul Newman and Robert Redford in The Sting (1973)
116. The Sting
1973
2h 9m
PG
8.3
 (284K)

Bruce Willis in Die Hard (1988)
117. Die Hard
1988
2h 12m
R
8.2
 (960K)

Sean Connery, Harrison Ford, Denholm Elliott, Michael Byrne, Alison Doody, and John Rhys-Davies in Indiana Jones and the Last Crusade (1989)
118. Indiana Jones and the Last Crusade
1989
2h 7m
PG-13
8.2
 (822K)

Aamir Khan and Darsheel Safary in Like Stars on Earth (2007)
119. Like Stars on Earth
2007
2h 42m
PG
8.3
 (211K)

Brigitte Helm in Metropolis (1927)
120. Metropolis
1927
2h 33m
Not Rated
8.3
 (189K)

Brad Pitt, Benicio Del Toro, Dennis Farina, Vinnie Jones, Jason Statham, and Ade in Snatch (2000)
121. Snatch
2000
1h 42m
R
8.2
 (924K)

George MacKay and Dean-Charles Chapman in 1917 (2019)
122. 1917
2019
1h 59m
R
8.2
 (697K)

Kim Basinger, Russell Crowe, Kevin Spacey, Danny DeVito, and Guy Pearce in L.A. Confidential (1997)
123. L.A. Confidential
1997
2h 18m
R
8.2
 (626K)

Bicycle Thieves (1948)
124. Bicycle Thieves
1948
1h 29m
Not Rated
8.3
 (178K)

Lin-Manuel Miranda in Hamilton (2020)
125. Hamilton
2020
2h 40m
PG-13
8.3
 (118K)

Downfall (2004)
126. Downfall
2004
2h 36m
R
8.2
 (380K)

Robert De Niro in Taxi Driver (1976)
127. Taxi Driver
1976
1h 54m
R
8.2
 (942K)

Dangal (2016)
128. Dangal
2016
2h 41m
Not Rated
8.3
 (217K)

Christian Bale in Batman Begins (2005)
129. Batman Begins
2005
2h 20m
PG-13
8.2
 (1.6M)

Leonardo DiCaprio and Jonah Hill in The Wolf of Wall Street (2013)
130. The Wolf of Wall Street
2013
3h
R
8.2
 (1.6M)

Clint Eastwood and Lee Van Cleef in For a Few Dollars More (1965)
131. For a Few Dollars More
1965
2h 12m
R
8.2
 (280K)

Viggo Mortensen and Mahershala Ali in Green Book (2018)
132. Green Book
2018
2h 10m
PG-13
8.2
 (595K)

Marilyn Monroe, Tony Curtis, and Jack Lemmon in Some Like It Hot (1959)
133. Some Like It Hot
1959
2h 1m
Approved
8.2
 (288K)

Charles Chaplin and Jackie Coogan in The Kid (1921)
134. The Kid
1921
1h 8m
Passed
8.2
 (137K)

Jim Carrey in The Truman Show (1998)
135. The Truman Show
1998
1h 43m
PG
8.2
 (1.2M)

Marlene Dietrich, Judy Garland, Burt Lancaster, Spencer Tracy, Montgomery Clift, Maximilian Schell, and Richard Widmark in Judgment at Nuremberg (1961)
136. Judgment at Nuremberg
1961
2h 59m
Approved
8.3
 (87K)

Anthony Hopkins and Olivia Colman in The Father (2020)
137. The Father
2020
1h 37m
PG-13
8.2
 (201K)

All About Eve (1950)
138. All About Eve
1950
2h 18m
Approved
8.2
 (141K)

Leonardo DiCaprio in Shutter Island (2010)
139. Shutter Island
2010
2h 18m
R
8.2
 (1.5M)

Daniel Day-Lewis in There Will Be Blood (2007)
140. There Will Be Blood
2007
2h 38m
R
8.2
 (652K)

Jeff Goldblum, Richard Attenborough, Laura Dern, Sam Neill, Ariana Richards, BD Wong, Joseph Mazzello, Martin Ferrero, and Bob Peck in Jurassic Park (1993)
141. Jurassic Park
1993
2h 7m
PG-13
8.2
 (1.1M)

Robert De Niro, Sharon Stone, and Joe Pesci in Casino (1995)
142. Casino
1995
2h 58m
R
8.2
 (575K)

Tom Cruise in Top Gun: Maverick (2022)
143. Top Gun: Maverick
2022
2h 10m
PG-13
8.2
 (733K)

Haley Joel Osment in The Sixth Sense (1999)
144. The Sixth Sense
1999
1h 47m
PG-13
8.2
 (1.1M)

Ran (1985)
145. Ran
1985
2h 40m
R
8.2
 (139K)

Ivana Baquero in Pan's Labyrinth (2006)
146. Pan's Labyrinth
2006
1h 58m
R
8.2
 (711K)

Clint Eastwood, Morgan Freeman, Gene Hackman, and Richard Harris in Unforgiven (1992)
147. Unforgiven
1992
2h 10m
R
8.2
 (443K)

Javier Bardem and Josh Brolin in No Country for Old Men (2007)
148. No Country for Old Men
2007
2h 2m
R
8.2
 (1.1M)

The Thing (1982)
149. The Thing
1982
1h 49m
R
8.2
 (479K)

Russell Crowe in A Beautiful Mind (2001)
150. A Beautiful Mind
2001
2h 15m
PG-13
8.2
 (1M)

Uma Thurman in Kill Bill: Vol. 1 (2003)
151. Kill Bill: Vol. 1
2003
1h 51m
R
8.2
 (1.2M)

Humphrey Bogart, Tim Holt, and Walter Huston in The Treasure of the Sierra Madre (1948)
152. The Treasure of the Sierra Madre
1948
2h 6m
Approved
8.2
 (134K)

Toshirô Mifune and Tatsuya Nakadai in Yojimbo (1961)
153. Yojimbo
1961
1h 50m
Not Rated
8.2
 (134K)

Richard Attenborough, Steve McQueen, and James Garner in The Great Escape (1963)
154. The Great Escape
1963
2h 52m
Approved
8.2
 (262K)

John Cleese, Terry Gilliam, Graham Chapman, Eric Idle, Terry Jones, Michael Palin, and Monty Python in Monty Python and the Holy Grail (1975)
155. Monty Python and the Holy Grail
1975
1h 31m
PG
8.2
 (577K)

Albert Brooks, Ellen DeGeneres, and Barry Humphries in Finding Nemo (2003)
156. Finding Nemo
2003
1h 40m
G
8.2
 (1.1M)

Jake Gyllenhaal and Hugh Jackman in Prisoners (2013)
157. Prisoners
2013
2h 33m
R
8.2
 (834K)

Christian Bale, Jean Simmons, Chieko Baishô, and Takuya Kimura in Howl's Moving Castle (2004)
158. Howl's Moving Castle
2004
1h 59m
PG
8.2
 (463K)

John Hurt in The Elephant Man (1980)
159. The Elephant Man
1980
2h 4m
PG
8.2
 (263K)

Toshirô Mifune in Rashomon (1950)
160. Rashomon
1950
1h 28m
Not Rated
8.2
 (184K)

Grace Kelly and Anthony Dawson in Dial M for Murder (1954)
161. Dial M for Murder
1954
1h 45m
PG
8.2
 (192K)

Jack Nicholson and Faye Dunaway in Chinatown (1974)
162. Chinatown
1974
2h 10m
R
8.1
 (356K)

Clark Gable and Vivien Leigh in Gone with the Wind (1939)
163. Gone with the Wind
1939
3h 58m
G
8.2
 (339K)

Ricardo Darín and Soledad Villamil in The Secret in Their Eyes (2009)
164. The Secret in Their Eyes
2009
2h 9m
R
8.2
 (226K)

Jason Flemyng, Dexter Fletcher, Vinnie Jones, Jason Statham, and Nick Moran in Lock, Stock and Two Smoking Barrels (1998)
165. Lock, Stock and Two Smoking Barrels
1998
1h 47m
R
8.1
 (624K)

Lewis Black, Bill Hader, Amy Poehler, Phyllis Smith, and Mindy Kaling in Inside Out (2015)
166. Inside Out
2015
1h 35m
PG
8.1
 (832K)

Natalie Portman and Hugo Weaving in V for Vendetta (2005)
167. V for Vendetta
2005
2h 12m
R
8.1
 (1.2M)

Woody Harrelson, Frances McDormand, and Sam Rockwell in Three Billboards Outside Ebbing, Missouri (2017)
168. Three Billboards Outside Ebbing, Missouri
2017
1h 55m
R
8.1
 (565K)

Robert De Niro in Raging Bull (1980)
169. Raging Bull
1980
2h 9m
R
8.1
 (386K)

Ewan McGregor, Robert Carlyle, Jonny Lee Miller, Ewen Bremner, and Kelly Macdonald in Trainspotting (1996)
170. Trainspotting
1996
1h 33m
R
8.1
 (735K)

Alec Guinness, William Holden, Jack Hawkins, Sessue Hayakawa, Geoffrey Horne, and Ann Sears in The Bridge on the River Kwai (1957)
171. The Bridge on the River Kwai
1957
2h 41m
PG
8.1
 (237K)

Joan Cusack, Jason Schwartzman, Rashida Jones, Sergio Pablos, Will Sasso, J.K. Simmons, and Neda Margrethe Labba in Klaus (2019)
172. Klaus
2019
1h 36m
PG
8.2
 (195K)

Leonardo DiCaprio and Tom Hanks in Catch Me If You Can (2002)
173. Catch Me If You Can
2002
2h 21m
PG-13
8.1
 (1.1M)

Fargo (1996)
174. Fargo
1996
1h 38m
R
8.1
 (736K)

Joel Edgerton and Tom Hardy in Warrior (2011)
175. Warrior
2011
2h 20m
PG-13
8.1
 (504K)

Willem Dafoe, Alfred Molina, Thomas Haden Church, Jamie Foxx, Rhys Ifans, Benedict Cumberbatch, Zendaya, and Tom Holland in Spider-Man: No Way Home (2021)
176. Spider-Man: No Way Home
2021
2h 28m
PG-13
8.2
 (908K)

Clint Eastwood in Gran Torino (2008)
177. Gran Torino
2008
1h 56m
R
8.1
 (824K)

Rupert Grint, Daniel Radcliffe, and Emma Watson in Harry Potter and the Deathly Hallows: Part 2 (2011)
178. Harry Potter and the Deathly Hallows: Part 2
2011
2h 10m
PG-13
8.1
 (966K)

Clint Eastwood, Morgan Freeman, and Hilary Swank in Million Dollar Baby (2004)
179. Million Dollar Baby
2004
2h 12m
PG-13
8.1
 (731K)

My Neighbor Totoro (1988)
180. My Neighbor Totoro
1988
1h 26m
G
8.1
 (391K)

Charlize Theron and Tom Hardy in Mad Max: Fury Road (2015)
181. Mad Max: Fury Road
2015
2h
R
8.1
 (1.1M)

Children of Heaven (1997)
182. Children of Heaven
1997
1h 29m
PG
8.2
 (82K)

Ben-Hur (1959)
183. Ben-Hur
1959
3h 32m
G
8.1
 (257K)

Chiwetel Ejiofor in 12 Years a Slave (2013)
184. 12 Years a Slave
2013
2h 14m
R
8.1
 (750K)

Barry Lyndon (1975)
185. Barry Lyndon
1975
3h 5m
PG
8.1
 (187K)

Ethan Hawke and Julie Delpy in Before Sunrise (1995)
186. Before Sunrise
1995
1h 41m
R
8.1
 (347K)

Harrison Ford and Sean Young in Blade Runner (1982)
187. Blade Runner
1982
1h 57m
R
8.1
 (835K)

The Grand Budapest Hotel (2014)
188. The Grand Budapest Hotel
2014
1h 39m
R
8.1
 (902K)

Andrew Garfield in Hacksaw Ridge (2016)
189. Hacksaw Ridge
2016
2h 19m
R
8.1
 (612K)

Ben Affleck in Gone Girl (2014)
190. Gone Girl
2014
2h 29m
R
8.1
 (1.1M)

Robin Williams in Dead Poets Society (1989)
191. Dead Poets Society
1989
2h 8m
PG
8.1
 (563K)

Maharaja (2024)
192. Maharaja
2024
2h 21m
8.5
 (48K)

Memories of Murder (2003)
193. Memories of Murder
2003
2h 12m
Not Rated
8.1
 (225K)

Daniel Day-Lewis in In the Name of the Father (1993)
194. In the Name of the Father
1993
2h 13m
R
8.1
 (190K)

Charles Chaplin in The Gold Rush (1925)
195. The Gold Rush
1925
1h 35m
Approved
8.1
 (120K)

Billy Crystal and John Goodman in Monsters, Inc. (2001)
196. Monsters, Inc.
2001
1h 32m
G
8.1
 (999K)

Rita Cortese, Ricardo Darín, Diego Gentile, Darío Grandinetti, Oscar Martínez, María Marull, Erica Rivas, Leonardo Sbaraglia, Mónica Villa, María Onetto, and Julieta Zylberberg in Wild Tales (2014)
197. Wild Tales
2014
2h 2m
R
8.1
 (221K)

Robert De Niro and Christopher Walken in The Deer Hunter (1978)
198. The Deer Hunter
1978
3h 3m
R
8.1
 (367K)

Buster Keaton in The General (1926)
199. The General
1926
1h 18m
Passed
8.1
 (100K)

Buster Keaton in Sherlock Jr. (1924)
200. Sherlock Jr.
1924
45m
Passed
8.2
 (59K)

Janeane Garofalo, Ian Holm, Peter O'Toole, Brian Dennehy, John Ratzenberger, James Remar, Will Arnett, Brad Garrett, Kathy Griffin, Brad Bird, Lindsey Collins, Walt Dohrn, Tony Fucile, Michael Giacchino, Bradford Lewis, Danny Mann, Teddy Newton, Patton Oswalt, Lou Romano, Peter Sohn, Jake Steinfeld, Stéphane Roux, Lori Richardson, Thomas Keller, Julius Callahan, Marco Boerries, Andrea Boerries, and Jack Bird in Ratatouille (2007)
201. Ratatouille
2007
1h 51m
G
8.1
 (850K)

Susan Backlinie and Bruce in Jaws (1975)
202. Jaws
1975
2h 4m
PG
8.1
 (675K)

Jay Baruchel and Randy Thom in How to Train Your Dragon (2010)
203. How to Train Your Dragon
2010
1h 38m
PG
8.1
 (816K)

Marlon Brando in On the Waterfront (1954)
204. On the Waterfront
1954
1h 48m
Approved
8.1
 (168K)

Mary and Max (2009)
205. Mary and Max
2009
1h 32m
Not Rated
8.1
 (189K)

The Wages of Fear (1953)
206. The Wages of Fear
1953
2h 11m
Not Rated
8.1
 (68K)

Christian Bale and Matt Damon in Ford v Ferrari (2019)
207. Ford v Ferrari
2019
2h 32m
PG-13
8.1
 (497K)

Wild Strawberries (1957)
208. Wild Strawberries
1957
1h 32m
Not Rated
8.1
 (117K)

The Third Man (1949)
209. The Third Man
1949
1h 33m
Approved
8.1
 (185K)

James Stewart, Jean Arthur, Claude Rains, Edward Arnold, Beulah Bondi, Guy Kibbee, Thomas Mitchell, and Eugene Pallette in Mr. Smith Goes to Washington (1939)
210. Mr. Smith Goes to Washington
1939
2h 9m
Approved
8.1
 (123K)

Hugh Jackman in Logan (2017)
211. Logan
2017
2h 17m
R
8.1
 (862K)

Sylvester Stallone and Talia Shire in Rocky (1976)
212. Rocky
1976
2h
PG
8.1
 (641K)

Setsuko Hara and Chishû Ryû in Tokyo Story (1953)
213. Tokyo Story
1953
2h 16m
Not Rated
8.1
 (70K)

Julianne Moore and Jeff Bridges in The Big Lebowski (1998)
214. The Big Lebowski
1998
1h 57m
R
8.1
 (872K)

The Seventh Seal (1957)
215. The Seventh Seal
1957
1h 36m
Not Rated
8.1
 (202K)

Brie Larson and Jacob Tremblay in Room (2015)
216. Room
2015
1h 58m
R
8.1
 (458K)

Michael Keaton, Liev Schreiber, Brian d'Arcy James, Mark Ruffalo, and Rachel McAdams in Spotlight (2015)
217. Spotlight
2015
2h 9m
R
8.1
 (508K)

Arnold Schwarzenegger in The Terminator (1984)
218. The Terminator
1984
1h 47m
R
8.1
 (941K)

Don Cheadle, Nick Nolte, Joaquin Phoenix, Mosa Kaiser, Sophie Okonedo, Ofentse Modiselle, and Mathabo Pieterson in Hotel Rwanda (2004)
219. Hotel Rwanda
2004
2h 1m
PG-13
8.1
 (377K)

Charlie Sheen, Willem Dafoe, John C. McGinley, and Kevin Eshelman in Platoon (1986)
220. Platoon
1986
2h
R
8.1
 (446K)

Vincent Cassel in La haine (1995)
221. La haine
1995
1h 38m
Not Rated
8.1
 (202K)

Johnny Depp, Geoffrey Rush, Orlando Bloom, and Keira Knightley in Pirates of the Caribbean: The Curse of the Black Pearl (2003)
222. Pirates of the Caribbean: The Curse of the Black Pearl
2003
2h 23m
PG-13
8.1
 (1.2M)

Ethan Hawke and Julie Delpy in Before Sunset (2004)
223. Before Sunset
2004
1h 20m
R
8.1
 (294K)

Maria Falconetti and Eugene Silvain in The Passion of Joan of Arc (1928)
224. The Passion of Joan of Arc
1928
1h 54m
Passed
8.1
 (62K)

Suriya and Lijo Mol Jose in Jai Bhim (2021)
225. Jai Bhim
2021
2h 44m
Approved
8.7
 (221K)

Dana Andrews, Myrna Loy, Fredric March, Virginia Mayo, and Teresa Wright in The Best Years of Our Lives (1946)
226. The Best Years of Our Lives
1946
2h 50m
Approved
8.1
 (72K)

Max von Sydow in The Exorcist (1973)
227. The Exorcist
1973
2h 2m
R
8.1
 (464K)

Daniel Brühl and Chris Hemsworth in Rush (2013)
228. Rush
2013
2h 3m
R
8.1
 (522K)

Samuel L. Jackson, Holly Hunter, Jason Lee, Craig T. Nelson, Brad Bird, Sarah Vowell, and Spencer Fox in The Incredibles (2004)
229. The Incredibles
2004
1h 55m
PG
8.0
 (828K)

Judy Garland, Ray Bolger, Jack Haley, Bert Lahr, and Frank Morgan in The Wizard of Oz (1939)
230. The Wizard of Oz
1939
1h 42m
G
8.1
 (435K)

Network (1976)
231. Network
1976
2h 1m
R
8.1
 (174K)

Stand by Me (1986)
232. Stand by Me
1986
1h 29m
R
8.1
 (451K)

Richard Gere in Hachi: A Dog's Tale (2009)
233. Hachi: A Dog's Tale
2009
1h 33m
G
8.1
 (318K)

Julie Andrews, Christopher Plummer, Charmian Carr, Angela Cartwright, Duane Chase, Nicholas Hammond, Kym Karath, Heather Menzies-Urich, and Debbie Turner in The Sound of Music (1965)
234. The Sound of Music
1965
2h 52m
G
8.1
 (266K)

Hümeyra, Fikret Kuskan, Çetin Tekindor, Özge Özberk, and Ege Tanman in My Father and My Son (2005)
235. My Father and My Son
2005
1h 52m
Not Rated
8.2
 (94K)

Kim Min-hee, Ha Jung-woo, Cho Jin-woong, and Kim Tae-ri in The Handmaiden (2016)
236. The Handmaiden
2016
2h 25m
Not Rated
8.1
 (179K)

Jack Benny and Carole Lombard in To Be or Not to Be (1942)
237. To Be or Not to Be
1942
1h 39m
Approved
8.1
 (44K)

Emile Hirsch in Into the Wild (2007)
238. Into the Wild
2007
2h 28m
R
8.1
 (666K)

Fouzia El Kader, Brahim Hadjadj, and Jean Martin in The Battle of Algiers (1966)
239. The Battle of Algiers
1966
2h 1m
Not Rated
8.1
 (67K)

Henry Fonda, John Carradine, Jane Darwell, Dorris Bowdon, Frank Darien, and Russell Simpson in The Grapes of Wrath (1940)
240. The Grapes of Wrath
1940
2h 9m
Approved
8.1
 (101K)

Bill Murray and Andie MacDowell in Groundhog Day (1993)
241. Groundhog Day
1993
1h 41m
PG
8.0
 (696K)

Jennifer Aniston, Harry Connick Jr., John Mahoney, Christopher McDonald, Vin Diesel, and Bob Bergen in The Iron Giant (1999)
242. The Iron Giant
1999
1h 26m
PG
8.1
 (234K)

Emilio Echevarría, Gael García Bernal, and Goya Toledo in Amores Perros (2000)
243. Amores Perros
2000
2h 34m
R
8.0
 (256K)

Joan Fontaine and Laurence Olivier in Rebecca (1940)
244. Rebecca
1940
2h 10m
Approved
8.1
 (149K)

Viola Davis, Bryce Dallas Howard, Octavia Spencer, and Emma Stone in The Help (2011)
245. The Help
2011
2h 26m
PG-13
8.1
 (501K)

Paul Newman in Cool Hand Luke (1967)
246. Cool Hand Luke
1967
2h 7m
Approved
8.1
 (191K)

Clark Gable and Claudette Colbert in It Happened One Night (1934)
247. It Happened One Night
1934
1h 45m
Approved
8.1
 (114K)

Tabu, Ajay Devgn, Shriya Saran, Ishita Dutta, and Mrunal Jadhav in Drishyam (2015)
248. Drishyam
2015
2h 43m
Not Rated
8.2
 (98K)

Nastassja Kinski, Harry Dean Stanton, and Hunter Carson in Paris, Texas (1984)
249. Paris, Texas
1984
2h 25m
R
8.1
 (124K)

Ingrid Bergman and Liv Ullmann in Autumn Sonata (1978)
250. Autumn Sonata
1978
1h 39m
PG
8.1
 (39K)
"""
data = []
movie_data = extract_movie_data(movie_string)
print(movie_data)
write_to_csv(movie_data, './files/movies.csv')