# Controle de Qualidade de Peças

Programa em Python, executado no terminal, que automatiza a inspeção de peças de uma linha de montagem:
avalia cada peça pelos critérios de qualidade, guarda as aprovadas em caixas de 10 unidades e gera um
relatório do que foi produzido.

Trabalho da disciplina **Algoritmos e Lógica de Programação** (UniFECAF).
Desafio: *Gestão de Peças, Qualidade e Armazenamento*.

---

## Como funciona

O operador informa os dados de cada peça: **ID, peso, cor e comprimento**. O programa confere três
critérios:

| Critério | Aceito |
|---|---|
| Peso | de 95 g a 105 g (os limites contam como aprovados) |
| Cor | azul ou verde |
| Comprimento | de 10 cm a 20 cm (os limites contam como aprovados) |

- Se passar nos três, a peça é **aprovada** e vai para a caixa aberta. Quando a caixa chega a 10 peças,
  ela é fechada e a próxima peça aprovada abre uma caixa nova.
- Se falhar em qualquer um, a peça é **reprovada** e o programa registra **todos** os motivos.

### Menu

```
=== CONTROLE DE QUALIDADE ===
1 - Cadastrar nova peça
2 - Listar peças aprovadas/reprovadas
3 - Remover peça cadastrada
4 - Listar caixas fechadas
5 - Gerar relatório final
6 - Importar peças de planilha CSV
7 - Salvar dados agora
0 - Salvar e sair
```

### Os dados não se perdem

As peças e as caixas ficam guardadas no arquivo `dados_pecas.json`. O programa carrega esse arquivo ao
abrir e salva ao sair (a opção 7 salva a qualquer momento). Na primeira execução, quando o arquivo
ainda não existe, o sistema avisa que está começando do zero.

### Cuidados com o que é digitado

Erro de digitação é comum em inspeção manual, então o programa confere a entrada antes de gravar:

- **Peso e comprimento** precisam ser números maiores que zero. Vírgula também é aceita (`98,5`).
- **Valor muito longe do padrão** (ex.: peso `9.8`, quando o normal é perto de 100) gera um aviso de
  possível erro de digitação e pede confirmação. O valor não é bloqueado, porque a peça pode estar
  realmente com defeito.
- **Cor** é aceita com maiúsculas ou espaços (`" AZUL "` vira `azul`), mas não pode ter números.
- **ID** não pode ficar em branco nem repetir um ID já cadastrado.
- Antes de gravar, o programa mostra o resumo da peça e pede confirmação (S/N).

### Remoção de peças

Peças reprovadas e peças que estão numa caixa **ainda aberta** podem ser removidas. Peças de uma caixa
**fechada** não podem: a caixa já foi lacrada, e o registro precisa continuar igual à caixa física.

### Importação de planilha

A opção 6 lê um arquivo CSV com as colunas `id,peso,cor,comprimento`. Cada linha passa pelas mesmas
verificações do cadastro pelo teclado. Linhas com erro são recusadas e listadas com o motivo; valores
muito fora do padrão são importados e aparecem num aviso para conferência.

### Limitações

- Não há edição de peça. Para corrigir um cadastro, remova a peça (se ainda for possível) e cadastre de
  novo.
- Se o arquivo `dados_pecas.json` estiver corrompido, o programa avisa e começa do zero. Ao salvar,
  o conteúdo antigo é substituído.
- O sistema não controla estoque nem expedição: para ele, o trabalho termina quando a caixa é fechada.

---

## Como executar

### 1. Pré-requisito

Python 3 instalado. Para conferir, no terminal:

```
python --version
```

### 2. Baixar o projeto

Na página do repositório no GitHub, clique em **Code → Download ZIP** e extraia a pasta. Ou, com Git:

```
git clone https://github.com/vinifranciscato/controle-qualidade-pecas.git
```

### 3. Abrir a pasta no VS Code

**File → Open Folder** (Arquivo → Abrir Pasta) e selecione a pasta do projeto. Assim o terminal do VS Code
já abre no lugar certo, onde também está a planilha de exemplo.

### 4. Rodar

No terminal do VS Code (**Terminal → New Terminal**):

```
python controle_qualidade.py
```

No Windows, se `python` não for reconhecido, use `py controle_qualidade.py`.

### 5. Somente para a opção 6 (importação de planilha)

A importação usa a biblioteca **pandas**. Instale uma vez:

```
pip install -r requirements.txt
```

Sem o pandas, as opções de 1 a 5 funcionam normalmente; só a opção 6 avisa que falta a biblioteca.

---

## Exemplos de entrada e saída

### Primeira execução e cadastro de peça aprovada (valor com vírgula e cor em maiúsculo)

```
=== SISTEMA DE CONTROLE DE QUALIDADE DE PEÇAS ===
Nenhum dado salvo encontrado - começando do zero.

--- CADASTRO DE PEÇA ---
ID da peça: v-01
Peso (g): 98,5
Cor:  AZUL
Comprimento (cm): 15

Peça V-01 | Peso: 98.5 g | Cor: azul | Comprimento: 15.0 cm
Confirmar cadastro? (S/N): S
Peça APROVADA. Guardada na caixa 1 (1 de 10).
```

### Peça reprovada em mais de um critério

```
ID da peça: R-1
Peso (g): 120
Cor: preta
Comprimento (cm): 15

Peça R-1 | Peso: 120.0 g | Cor: preta | Comprimento: 15.0 cm
Confirmar cadastro? (S/N): S
Peça REPROVADA. Motivos:
    - peso fora do padrão
    - cor não aceita
```

### Valor suspeito de erro de digitação

```
Peso (g): 9.8
  Atenção: 9.8 g está muito fora do padrão (95 a 105 g).
  Pode ser erro de digitação.
  Confirma esse valor? (S/N): N
Peso (g): 98
```

### Caixa completa

```
Confirmar cadastro? (S/N): S
Peça APROVADA. Guardada na caixa 1 (10 de 10).
Caixa 1 completa e FECHADA. A próxima peça aprovada abre uma nova caixa.
```

### Tentativa de remover peça de caixa fechada

```
ID da peça a remover: F-05
A peça F-05 está na caixa 1, que já está fechada.
Peças de caixas fechadas não podem ser removidas pelo sistema.
```

### Importação da planilha de exemplo e relatório final

```
Nome do arquivo CSV (ex.: pecas_exemplo.csv): pecas_exemplo.csv

Linhas lidas: 14
Peças importadas: 14 (aprovadas: 11 - reprovadas: 3)
Linhas recusadas: 0
```

```
=== RELATÓRIO FINAL ===
Peças cadastradas: 14
Peças aprovadas: 11
Peças reprovadas: 3

Reprovações por motivo:
  - peso fora do padrão: 2
  - cor não aceita: 2
  - comprimento fora do padrão: 2
  (uma peça pode ter mais de um motivo)

Peças reprovadas:
  P-104
    - peso fora do padrão
  P-105
    - cor não aceita
    - comprimento fora do padrão
  P-112
    - peso fora do padrão
    - cor não aceita
    - comprimento fora do padrão

Caixas utilizadas: 2 - Caixas Fechadas: 1 - Caixas em aberto: 1
```

### Segunda execução: os dados voltam

```
=== SISTEMA DE CONTROLE DE QUALIDADE DE PEÇAS ===
Dados carregados de dados_pecas.json: 2 peça(s) e 1 caixa(s).
```

---

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `controle_qualidade.py` | o programa |
| `pecas_exemplo.csv` | planilha com 14 peças para testar a opção 6 |
| `requirements.txt` | biblioteca necessária para a opção 6 |
| `dados_pecas.json` | criado pelo programa ao salvar; guarda as peças e as caixas |
| `Trabalho-Controle-Qualidade-Vinicius-Franciscato.pdf` | parte teórica do trabalho, com os prints da execução |

## Tecnologias

- Python 3
- `json` (biblioteca padrão) para salvar e carregar os dados
- pandas (somente para a importação de planilha)

---

**Vinícius Franciscato** - RA 254086
Algoritmos e Lógica de Programação - UniFECAF
Vídeo de apresentação: https://youtu.be/lqdcI4ug2rE
