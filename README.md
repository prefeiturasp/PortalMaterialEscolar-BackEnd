[![Build Status](http://jenkins.sme.prefeitura.sp.gov.br/buildStatus/icon?job=PortalMaterialEscolar-BackEnd%2Fmaster)](http://jenkins.sme.prefeitura.sp.gov.br/view/Portal_Material_Escolar/job/PortalMaterialEscolar-BackEnd/job/master/)
# SME-PortalMaterialEscolar-BackEnd-BackEnd
========

Portal do programa de captação de fornecedores de material escolar da Secretaria de Educação da cidade de São Paulo.

License: MIT

Versão: 0.1.0


## Release Notes


### Para desenvolver

1.  Clone o repositório.
2.  Crie um Virtualenv com Python 3.6
3.  Ative o Virtualenv.
4.  Instale as dependências.
5.  Configure a instância com o .env
6.  Execute os testes.
7.  Faça um Pull Request com o seu desenvolvimento

```console
git clone https://github.com/prefeiturasp/PortalMaterialEscolar-BackEnd.git back
cd back
python -m venv .venv
source .venv/bin/activate
pip install -r requirements\local.txt
cp env_sample .env
pytest
```

### Tema do Admin
Para instalar o tema do Admin

```console
python manage.py loaddata admin_interface_theme_uswds.json
```

### Filas Celery
**Subir o Celery Worker**
```console
celery  -A config worker --loglevel=info
```

**Subir o Celery Beat**
```console
celery  -A config beat --loglevel=info
```

**Monitorar os processos no celery**
```console
flower -A config --port=5555
```

**Limpar os processos no celery**
```console
celery  -A config purge
```
