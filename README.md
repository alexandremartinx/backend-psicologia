## Setup

### Supabase (database)

Para rodar localmente é necessário ter instalado o supabase

- https://supabase.com/docs/guides/cli/getting-started?queryGroups=platform&platform=linux

Este processo pode demorar, irá baixar o docker do Supabase para rodar local:

```sh
supabase start
```

A UI pode ser acessada através da URL: `http://localhost:54323/project/default`

### API (backend)

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

O projeto possui um `launch.json` assim pode ser executada diretamente pelo VScode como debug (recomendado)

#### Alternativamente pode ser executada pelo terminal

```sh
python app/app.py
```

## Docs

```sh
http://localhost:5000/apidocs
```

## Arquitetura

O repositório é estruturado com as seguintes ideias:

- https://medium.com/geekculture/how-to-architect-your-flask-rest-api-abf95637d9f5
- https://medium.com/@DanKaranja/building-api-documentation-in-flask-with-swagger-a-step-by-step-guide-59a453509e2f
- https://brunotatsuya.dev/blog/jwt-authentication-and-authorization-for-python-flask-rest-apis
