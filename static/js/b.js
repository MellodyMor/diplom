function sendData() {
            var inp = document.getElementsByName('nameRadio');
            var o = ''
            if (document.getElementById('btnControl5').checked){
                if (inp[0].value == n){
                    o = 'правильно';
                }
            }
            if (document.getElementById('btnControl6').checked){
                if (inp[1].value == n){
                    o = 'правильно';
                }
            }
            if (document.getElementById('btnControl3').checked){
                if (inp[2].value == n){
                    o = 'правильно';
                }
            }
            if (document.getElementById('btnControl4').checked){
                if (inp[3].value == n){
                    o = 'правильно';
                }
            }
            if (o == ''){
            document.getElementById("res").innerHTML = "не правильно";
            document.getElementById("myHeading").innerHTML = "не правильно";
            }
            else{
                document.getElementById("res").innerHTML = o;
                document.getElementById("myHeading").innerHTML = o;
            }

            // Получаем значение из тега <p>
            const value = document.getElementById('myHeading').innerText;

            // Создаем объект XMLHttpRequest
            const xhr = new XMLHttpRequest();

            // Устанавливаем метод POST и URL для отправки данных
            xhr.open('POST', '/get-text', true);

            // Устанавливаем заголовок Content-Type для отправки данных в формате JSON
            xhr.setRequestHeader('Content-Type', 'application/json');

            // Отправляем данные на сервер в формате JSON
            xhr.send(JSON.stringify({ data: value }));
            }