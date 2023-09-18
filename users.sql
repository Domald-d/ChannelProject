Create Database Runners;
use Runners;

CREATE TABLE USERS(
Username varchar(75) primary key,
Nickname varchar(15),
Nametitle varchar(75),
Lvl int,
Runs int,
RunsToday int,
Timer float,
constraint userName_PK primary key(Username)
);


delimiter $$
drop procedure if exists BuatilNotanda $$
create procedure BuaTilNotanda(Nafn varchar(75),Nick varchar(15), Title varchar(75), lvl int, runs int, runsToday int, timer float)
begin
	insert into USERS(Username,Nickname,Nametitle,Lvl,Runs,RunsToday,Timer)values(Nafn,Nick,Title,lvl,runs,runsToday,timer);
end $$
delimiter ;

delimiter $$
drop procedure if exists uppfaeraNotanda $$
create procedure uppfaeraNotanda(Nafn varchar(75),Nick varchar(15),Title varchar(75),lvl int,runs int,runsToday int,timer float)
begin
	if exists(select Nafn from users where Nafn = Username)
		then update USERS set Nickname = Nick, Nametitle = Title, Lvl = lvl, Runs = runs, RunsToday = runsToday, Timer = timer
        where Username = Nafn;
	end if;
end $$
delimiter ;

delimiter $$
drop procedure if exists UserExists $$
create procedure UserExists(IN pUsername varchar(75), out pUserExists int)
begin
	declare userCount int;
    SELECT COUNT(*) INTO userCount FROM USERS WHERE Username = pUsername;
    SET pUserExists = IF(userCount > 0, 1, 0);
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS GetUserByUsername $$
CREATE PROCEDURE GetUserByUsername(IN pUsername VARCHAR(75))
BEGIN
    SELECT * FROM USERS WHERE Username = pUsername;
END $$
DELIMITER ;