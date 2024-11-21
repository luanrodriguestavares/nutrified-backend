# NutriFied API
Esta API foi desenvolvida para gerenciar o registro e acompanhamento de refeições, água consumida e as necessidades de calorias dos usuários. Ela permite a criação de usuários, login, registro de alimentos, refeições e acompanhamento de consumo de água.

## Estrutura do Projeto
O projeto está organizado da seguinte forma:
-   **app/models**: Contém as definições dos modelos de dados (User, Meal, Food, Water).
-   **app/routes**: Contém as rotas para as diferentes funcionalidades (auth, user, food, meal, water).
-   **app/services**: Contém a lógica de negócios, como cálculos de calorias e água.
-   **app/database**: Configuração do banco de dados usando SQLAlchemy.

## Instalação
1.  Clone o repositório:

    `git clone https://github.com/seu-usuario/nome-do-repositorio.git` 

2.  Inicie o servidor:

    `flask run` 

A API estará disponível em `http://localhost:5000`.

## Rotas

### **Autenticação**
-   **POST /register**: Registra um novo usuário.
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "age": 30,
  "height": 175,
  "weight": 70,
  "goal": "lose weight",
  "gender": "male"
}
```

-   **POST /login**: Realiza o login de um usuário.
```json
{
    "email": "string",
	"password": "string"
}
```
-   **POST /logout**: Realiza o logout do usuário.
  
-   **GET /me**: Retorna as informações do usuário logado.

----------

### **Usuários**

-   **GET /user/int:user_id**: Retorna as informações de um usuário pelo ID.
-   **GET /user/int:user_id/needs**: Retorna as necessidades diárias de calorias e água de um usuário.
-   **POST /user/int:user_id/update_daily_calories**: Atualiza as calorias consumidas pelo usuário.

----------

### **Alimentos**

-   **POST /food**: Registra um novo alimento.
```json
{
      "name": "string",
      "calories_per_portion": 200,
      "portion_weight": 100,
      "category": "fruta"
}
```
-   **GET /food**: Retorna todos os alimentos registrados.
----------

### **Refeições**

-   **POST /meal**: Registra uma nova refeição.
 ```json
{
    "user_id": 1,
    "foods": [
        {
            "food_id": 1,
            "quantity": 2,
            "calories": 400
        }
    ],
    "total_calories": 400,
    "date": "2024-11-21T10:00:00"
}
```
-   **GET /meals**: Retorna todas as refeições de um usuário pelo ID.
    
----------

### **Água**

-   **POST /water/record**: Registra a quantidade de água consumida por um usuário.
```json
{
	"user_id": 1,
	"quantity": 500
}
```
-   **GET /water/logs**: Retorna os registros de consumo de água de um usuário.
    

## Tecnologias Usadas

-   **Flask**: Framework para a construção da API.
-   **SQLAlchemy**: ORM para interagir com o banco de dados.
-   **Werkzeug**: Para gerenciamento de segurança (hash de senhas).
-   **PostgreSQL ou SQLite**: Banco de dados relacional para persistência.