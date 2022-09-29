CREATE DEFINER=`root`@`localhost` PROCEDURE `adding_new_person`(
	IN p_name VARCHAR(40),
    IN p_lastname VARCHAR(60),
    IN p_belt VARCHAR(40),
    IN p_stripe int
)
BEGIN
	if(select exists (select 1 from osoby_trenujace where imie = p_name AND nazwisko = p_lastname)) then
		select 'Uzytkownik jest juz w bazie';
	else
		insert into osoby_trenujace
        (
			imie,
            nazwisko,
            pas,
            belki
        )
        values
        (
			p_name,
            p_lastname,
            p_belt,
            p_stripe
        );
        end if ;
END