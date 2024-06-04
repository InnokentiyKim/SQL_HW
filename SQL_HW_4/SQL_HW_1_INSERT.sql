INSERT INTO artist
VALUES  (1, 'Metallica'),
		(2, 'Red Hot Chili Peppers'),
		(3, 'Taylor Swift'),
		(4, 'Elvis Presley'),
		(5, 'Bob Marley'),
		(6, 'The Wailers'),
		(7, 'Ed Sheeran');

INSERT INTO genre
VALUES  (1, 'хэви-метал'),
		(2, 'рок'),
		(3, 'поп'),
		(4, 'рок-н-ролл'),
		(5, 'регги');
	
INSERT INTO artist_genre 
VALUES	(1, 1),
		(1, 2),
		(2, 2),
		(2, 3),
		(3, 3),
		(4, 4),
		(5, 5),
		(6, 5),
		(7, 3);

INSERT INTO album
VALUES  (1, 'Reload', 1997),
		(2, 'Greatest Hits', 2003),
		(3, 'Reputation', 2017),
		(4, 'Rock''n''Roll Legends', 1999),
		(5, 'Riding High', 2019);
	
INSERT INTO artist_album 
VALUES  (1, 1),
		(2, 2),
		(3, 3),
		(4, 4),
		(5, 5),
		(6, 5),
		(7, 3);

INSERT INTO tracks 
VALUES  (1, 1, 'Fuel', 269),
		(2, 1, 'The Memory Remains', 279),
		(3, 1, 'Devil''s Dance', 318),
		(4, 1, 'The Unforgiven II', 396),
		(5, 1, 'Better Than You', 321),
		(6, 2, 'Under the Bridge', 265),
		(7, 2, 'Give It Away', 284),
		(8, 2, 'Californication', 374),
		(9, 2, 'Scar Tissue', 296),
		(10, 3, 'Ready For It?', 322),
		(11, 3, 'End Game', 288),
		(12, 3, 'I Did Something Bad', 347),
		(13, 3, 'Don''t Blame Me', 330),
		(14, 4, 'Don''t Be Cruel', 176),
		(15, 4, 'I Don''t Care If the Sun Don''t Shine', 292),
		(16, 4, 'All Shook Up', 190),
		(17, 5, 'Corner Stone', 321),
		(18, 5, 'Riding High', 188),
		(19, 5, '400 Years', 280);
		
INSERT INTO collection 
VALUES  (1, 'The Very Best of 2000', 2000),
		(2, 'Partyhits: Best of Rock ''n'' Roll Music', 1998),
		(3, 'Various artists', 2020),
		(4, 'The Best collection', 2022);
		
INSERT INTO collection_track 
VALUES  (1, 1),
		(1, 4),
		(1, 6),
		(1, 8),
		(2, 14),
		(2, 15),
		(2, 16),
		(3, 2),
		(3, 5),
		(3, 10),
		(3, 15),
		(3, 18),
		(4, 2),
		(4, 7),
		(4, 9),
		(4, 11),
		(4, 12),
		(4, 17);
		



	
		





