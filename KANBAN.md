# 🥬 GreenEats - Documentação Técnica e Gestão

## 📌 Parte 1: Gestão Ágil (User Stories & Kanban)

### 1. Histórias de Usuário (User Stories) - MVP
*Focadas no cadastro e controle de qualidade.*

1.  **Cadastro de Produtos:**
    * "Como **Agricultor Parceiro**, quero **cadastrar meus produtos com título, preço e categoria**, para que **eles fiquem disponíveis imediatamente no marketplace.**"
2.  **Validação Automática:**
    * "Como **Administrador do Sistema**, quero **que o sistema rejeite automaticamente cadastros com dados inválidos (preço negativo ou nome curto)**, para que **a integridade da contabilidade seja mantida.**"
3.  **Gestão de Estoque:**
    * "Como **Administrador**, quero **visualizar uma lista atualizada de todos os produtos**, para que **eu possa conferir o que está sendo ofertado.**"

### 2. Quadro Kanban (Fluxo de Trabalho)

| Backlog / To Do (Futuro) | Doing (Em Progresso) | Done (Concluído) ✅ |
| :--- | :--- | :--- |
| Implementar Edição (PUT) | Gravação do Vídeo Demo | **Definição de User Stories** |
| Implementar Exclusão (DELETE) | | **Setup Backend (Flask + Airtable)** |
| Upload de Imagens | | **Rota POST /validar-produto** |
| Login de Usuários | | **Rota POST e GET /produtos** |
| | | **Frontend Vue.js Integrado** |
| | | **Deploy no Render** |

---

## 📌 Parte 2 e 3: Arquitetura da API (Backend)

### Modelo de Dados (Entidade Produto)
A tabela `Produtos` no Airtable possui a seguinte estrutura:
* `id`: String (Gerado automaticamente pelo Airtable)
* `titulo`: String (Min. 5 caracteres)
* `preco`: Number (Float, deve ser > 0)
* `categoria`: String (Enum: 'Fruta', 'Legume', 'Verdura')

### Definição das Rotas (CRUD Completo)
*Conforme solicitado na avaliação, aqui está a definição da estrutura RESTful:*

| Ação | Método HTTP | Rota (Endpoint) | Status (Projeto) |
| :--- | :--- | :--- | :--- |
| **Criar** | `POST` | `/produtos` | ✅ **Implementado** |
| **Ler (Listar)** | `GET` | `/produtos` | ✅ **Implementado** |
| **Validar** | `POST` | `/validar-produto` | ✅ **Implementado** (Regra de Negócio) |
| **Atualizar** | `PUT` | `/produtos/<id>` | 📝 *Planejado (Backlog)* |
| **Apagar** | `DELETE` | `/produtos/<id>` | 📝 *Planejado (Backlog)* |

---

## 📌 Parte 4: Integração Frontend (Conceito)

**Ciclo de Vida do Componente:**
A requisição para buscar os produtos é feita no momento de **montagem** do componente.
* No **Vue.js**, utilizamos o hook `mounted()`.
* *(Se fosse React, usaríamos `useEffect` com array vazio).*

**Trecho de Código Utilizado (Consumo da API):**
```javascript
// Método chamado automaticamente no mounted()
async listarProdutos() {
    try {
        // Consome a rota GET definida no Backend
        const response = await fetch('[https://greeneats-backend.onrender.com/produtos](https://greeneats-backend.onrender.com/produtos)');
        // Armazena o resultado no estado da aplicação (data)
        this.produtos = await response.json();
    } catch (error) {
        console.error("Erro na integração", error);
    }
}
