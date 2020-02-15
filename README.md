# Программа: VK_Analysis_Users'
- __I. Служит для сбора данных об интересах и деятельности пользователей сети ВК.__(bold)
- __II. Утилита может быть полезна `специалистам по машинному обучению`, блогерам, владельцем коммерческих интернет-площадок.__(bold)
--------------------------------------------------
## ИНСТРУКЦИЯ:
- Перед запуском создайте файл "text_search.txt" в котором через запятую перечислите ключевые слова.
- НАПРИМЕР: `Фотограф, фото, canon, nikon, фотография, фотографировал, фотографировала, съемка, фотопортрет, фотопортреты, фотостудия, фотостудии, модель, Photoshop, снимал, снимала, объектив`
- Сохраните и закройте файл "text_search.txt". Запустите "VK_Analysis_Users".
- Введите ваш логин в формате +79170001020.
- Введите пароль от своей страницы ВК.
- Запустите программу и введите название тематической группы.
- Программа заберет ID пользователей состоящих в группе.
- Утилита проведет анализ контента, интересов и дятельности полученных пользователей.

  - 1. Файл "text_search.txt" и "data_base_users.csv"(кодировка utf-8) должны находится в той же папке что и программа.
  - 2. При завершении в терминал будет выведен ID пользователей которых добавили в базу.
  - 3. В случае если вы ранее использовали программу есть возможность избежать записи в базу одних и тех пользователей.
  - 4. Для этого используйте базу данных пользователей которых утилита добавила ранее.
  - 5. В случае самого первого использования программа создаст пустую базу в формате с именем "data_base_users.csv".
  - 6. Программа проведет анализ записей на стене каждого найденного пользователя и выставит оценку по 10-ти бальной шкале.
  - 7. Если одно или несколько ключевых слов встретилось в одной записи на стене пользователяю добавляется 1 бал.
  - 8. Программа анализирует последние 10-ть записей на стене пользователя.
  - 9. Если произвольное из ключевых слов встретилось 8 раз в 8-ми записях оценка пользователя будет равна 8, соответственно если 5 раз то оценка равна 5 и т.д.
  - 10. Программа добавит интересы пользователя и его профессиональную деятельность.

### ПРЕДУПРЕЖДЕНИЕ:
- Существуют ограничения на использование методов API ВК.
- Программа не сохраняет ваши пароль и логин.
- Авторизацию необходимо проходить каждый раз при запуске.
- Программа не работает при двухфакторной аутентификации.
--------------------------------------------------
Разработчик: Сурнов Алексей.
e-mail: alslight@list.ru
--------------------------------------------------
