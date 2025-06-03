# AutoMLB

Automação de importação e vinculação de anúncios Mercado Livre (MLB) no Tiny ERP — **Versão de Demonstração**

---

## 📋 Descrição

O **AutoMLB** importa anúncios do Mercado Livre via códigos MLB para o Tiny ERP e, em seguida, vincula esses anúncios ao SKU correspondente. Por fim, envia o estoque atualizado para o e-commerce. Tudo de forma automática, reduzindo trabalho manual e minimizando erros.

> **Atenção:** esta implementação foi desenvolvida para o fluxo específico da empresa em que trabalho. Para uso em outros cenários, ajustes em URLs, XPaths, credenciais e lógicas de negócio serão necessários.

---

## ✨ Funcionalidades Principais

- **Importação de anúncios**  
  Recebe múltiplos códigos MLB e importa cada anúncio no Tiny ERP.

- **Vinculação de SKUs**  
  Associa cada anúncio importado ao SKU informado pelo usuário.

- **Envio de estoque**  
  Realiza o envio automático de estoque para o e-commerce após a vinculação.

- **Suporte a múltiplos marketplaces**  
  Fluxo adaptável conforme o marketplace.

- **Proteção de credenciais**  
  Usuário e senha são digitados na interface, sem exposição no código.

---

## ⚠️ Uso Específico e Adaptação

Este repositório serve como **prova de conceito / demonstração interna** para o processo de automação de anúncios no Tiny ERP, customizado para:

- URLs e endpoints do Tiny ERP da empresa NESHOP  
- XPaths e seletores específicos da versão atual do ERP  
- Perfil de usuário e fluxo de validações internos  

> **Se você pretende aproveitar este código em outra organização**, leve em conta:
> 1. **URLs e rotas**: podem mudar de ambiente para ambiente.  
> 2. **Seletores do front-end**: revise e ajuste todos os XPaths/CSS.    
> 3. **Regras de negócio**: cada empresa possui políticas próprias de importação e sincronização de estoque.

---

## 🚀 Demonstração Rápida

1. **Clone** este repositório:  
   ```bash
   git clone https://github.com/lulcas-leandro/AutoMLB.git
   cd AutoMLB

2. **Instale** num ambiente virtual:
    ```bash
    python -m venv venv
    venv\Scripts\Activate
    pip install -r requirements.txt

3. **Execute** a GUI de demonstração:
    ```bash
    python run.py

4. **Interaja**:

*Cole seus MLBs (códigos de anúncio).*

*Informe o SKU.*

*Selecione o marketplace.*

*Digite usuário e senha do Tiny.*

*Clique em Iniciar Automação.*

---

## 👤 Autor

Email: lucasleandro.cdev@gmail.com

GitHub: https://github.com/lulcas-leandro