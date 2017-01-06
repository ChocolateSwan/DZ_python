/**
 * Created by olyasur on 28.12.16.
 */

function validate_form ( )
{
    var valid;
	valid = true;
        if ( document.ante_form.sum_of_ante.value == "" )
        {
                alert ( "Пожалуйста заполните поле 'Сумма ставки'!" );
                valid = false;
        }
         if (!isFinite(document.ante_form.sum_of_ante.value))
        {
                alert ( "Поле 'Сумма ставки' должно быть числовым!" );
                valid = false;
        }
        if ( document.ante_form.participant.selectedIndex == 0 )
        {
                alert ( "Пожалуйста, выберите участника!" );
                valid = false;
        }
        return valid;
}