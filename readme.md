# API - Consulta de Endereço por CEP

Este endpoint permite consultar informações de endereço a partir de um CEP (Código de Endereçamento Postal).

## 📍 Endpoint GET /v1/zipcode/{zipcode}
### 🔸 Parâmetros

| Parâmetro | Tipo   | Obrigatório | Descrição                     |
|-----------|--------|-------------|-------------------------------|
| zipcode   | string | Sim         | CEP no formato somente números (ex: `01001000`) |

### ✅ Exemplo de Requisição GET /v1/zipcode/01001000
### ✅ Exemplo de Resposta (200 OK)

```json
{
  "zipcode": "01001000",
  "street": "Praça da Sé",
  "complement": "lado ímpar",
  "unit": null,
  "neighborhood": "Sé",
  "city": "São Paulo",
  "state_code": "SP",
  "state": "São Paulo",
  "region": "Sudeste"
}
```
📦 Códigos de Resposta
Código HTTP	Descrição
200	Endereço encontrado com sucesso
400	CEP inválido ou mal formatado
404	Endereço não encontrado
500	Erro interno do servidor


## Usage installers
# Base installation for only SANDBOX
```bash
make install
```

# Installation for lint and tests
```bash
make install-local
```

# Lint
```bash
make lint
```

# Reports
```bash
make coverage
```
