function sendData() {
                document.getElementById("r").innerHTML = '';
                var o = ''
                if (document.getElementById('check').checked){
                    if (0  == '{{ n }}'){
                        o = 'правильно';
                    }
                }
                if (document.getElementById('check2').checked){
                    if (1  == '{{ n }}'){
                        o = 'правильно';
                    }
                }
                if (document.getElementById('check3').checked){
                    if (2 == '{{ n }}'){
                        o = 'правильно';
                    }
                }
                 if (document.getElementById('check4').checked){
                    if (3  == '{{ n }}'){
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