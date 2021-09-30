# FluxoAgilBackEnd

## Para rodar a API

1. Instalar o **virtualenv**:
```
$ sudo apt install virtualenv
```
2. Pegar o **path** do python3 no sistema para ser usado no próximo passo:
```
$ which python3
```
3. Entrar na pasta do projeto e executar o comando para criar o ambiente virtual, substituindo o **path** pelo resultado do passo anterior:
```
$ virtualenv -p <path> venv
```
4. Ativar o venv para uso:
```
$ source venv/bin/activate
```
5. Instalar as depedências do projeto no ambiente virtual:
```
$ pip install -r requirements.txt
```
6. Mudar a variável de ambiente do ambiente virtual para o arquivo app.py:
```
$ export FLASK_APP=app
```
7. Executar o projeto:
```
$ flask run
```
**Obs:** Não é preciso instalar nada alem do virutalenv e o python para rodar o projeto.
## Antes de commitar
 * Caso tenha adicionado alguma biblioteca execute o comando **antes de commitar:**
 
 ``` 
$ pip freeze > requirements.txt
```