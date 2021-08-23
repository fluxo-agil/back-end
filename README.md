# FluxoAgilBackEnd

### Para rodar a API

1. Instalar o **virtualenv**:
```
sudo apt-get remove python-virtualenv
```
2. Pegar o **path** do python3 no sistema para ser usado no próximo passo:
```
which python3
```
3. Entrar na pasta do projeto e executar o comando para criar o ambiente virtual, substituindo o **path** pelo resultado do passo anterior:
```
virtualenv -p path venv
```
4. Instalar as depedências do projeto no ambiente virtual:
```
pip install -r requirements.txt
```
5. Mudar a variável de ambiente do ambiente virtual para o arquivo app.py:
```
export FLASK_APP=app.py
```
6. Executar o projeto:
```
flask run
```