<h1>Инструкция по запуску</h1>
<section>
<ol>
<li>Клонируйте репозиторий:<br>
<code>git clone https://github.com/CHRNVpy/web_mp3.git</code></li>

<li>Перейдите в папку с клонированным репозиторием.</li>

<li>Создайте пустую папку audio(для временных файлов):<br>
<code>mkdir audio</code></li>

<li>Создайте docker контейнер:<br>
<code>docker-compose up</code></li>

<li>Запустите docker image через Docker desktop или командой:<br>
<code>docker run &lt;название image(образа)&gt;</code></li>
</section>

<strong>Пример запросов к API сервиса c помощью Postman</strong>
<p>
<i>Добавить пользователя</i> 
<img src="add_user.png">
</p>
<p>
<i>Конвертировать файл</i> 
<img src="add_record.png">
</p>
<p>
<i>Скачать файл</i> 
<img src="get_record.png">
</p>