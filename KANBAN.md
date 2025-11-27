# 🥬 GreenEats - Documentação do Projeto

## 📌 Parte 1: Gestão Ágil e Conceção

### 1. Histórias de Usuário (User Stories) - MVP
*Focadas no cadastro e listagem de produtos.*

1.  **Cadastro de Produtos:**
    * "Como **Agricultor Parceiro**, quero **cadastrar meus produtos com nome, preço e categoria**, para que **eles fiquem disponíveis para venda no marketplace.**"
2.  **Validação de Dados:**
    * "Como **Sistema**, quero **impedir cadastros com preços negativos ou nomes muito curtos**, para que **a contabilidade e a apresentação da loja não sejam prejudicadas.**"
3.  **Visualização de Estoque:**
    * "Como **Administrador/Agricultor**, quero **ver uma lista atualizada de todos os produtos cadastrados**, para que **eu possa conferir o que está à venda.**"

---

### 2. Product Backlog (Visão Geral)
*Lista de desejos para o produto completo.*

* [MVP] Módulo de Cadastro de Produtos (Backend API)
* [MVP] Validação de Regras de Negócio (Preço > 0, Categorias)
* [MVP] Interface de Listagem e Cadastro (Frontend)
* [Futuro] Edição de Produtos (PUT)
* [Futuro] Remoção de Produtos (DELETE)
* [Futuro] Login e Autenticação de Agricultores
* [Futuro] Carrinho de Compras para o Consumidor

---

### 3. Sprint Backlog (O que foi feito nesta entrega)
*Foco: Validação e CRUD Básico (Create/Read).*

* **Backend (Python/Flask):**
    * Configuração do Ambiente e Airtable.
    * Implementação da Rota `POST /validar-produto` (Regras de Negócio).
    * Implementação da Rota `POST /produtos` (Salvar no banco).
    * Implementação da Rota `GET /produtos` (Listar do banco).
* **Frontend (Vue.js + Tailwind):**
    * Criação do Formulário de Cadastro.
    * Integração com API (Fetch/Axios).
    * Design Responsivo e Feedback visual de erros.

---

### 4. Quadro Kanban (Status Final)

| To Do (Futuro) | Doing (Em Progresso) | Done (Concluído) ✅ |
| :--- | :--- | :--- |
| Rota de Edição (PUT) | Gravação do Vídeo Demo | **Definição de User Stories** |
| Rota de Exclusão (DELETE) | | **Setup do Backend (Flask)** |
| Upload de Imagens Reais | | **Conexão com Airtable** |
| Tela de Login | | **Endpoint de Validação** |
| | | **Integração Frontend (Vue.js)** |
| | | **Deploy no Render (Web Service)** |
| | | **Deploy no Render (Static Site)** |
