# Resumo dos Testes

## Três malhas
- NewMesh0 : malha feita por Widmark 50 ppw
- quadMesh : malha totalmente quadrada
- circMesh : malha circular com elementos triangulares

## Testes - Esquemas temporais
| Schemes    |   Teste 1    |   Teste 2     | Teste 3           |
|------------|--------------|-------------- |-------------------|
| ddtSchemes |Euler         |backward       | cranckNicolson 0.9|
| gradSchmes |Gauss linear  |Gauss linear   | Gauss Linear      |
| divSchmes  |VanLeer       |VanLeer        | VanLeer           |

## Testes - Esquemas espaciais

| Schemes    |   Teste 4    |   Teste 5     | Teste 6           |
|------------|--------------|-------------- |-------------------|
| ddtSchemes |bakward       |backward       | backward          |
| gradSchmes |Gauss linear  |Gauss linear   | Gauss Linear      |
| divSchmes  |upwind        |limitedLinear 1| linearUpwind      |



