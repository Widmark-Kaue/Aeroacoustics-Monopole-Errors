SetFactory("OpenCASCADE");

// Parâmetros
lambda  = DefineNumber[34.653698762,Name "Parameter/lambda"];
dinner  = DefineNumber[lambda,Name "Parameters/dinner"];
dout    = DefineNumber[11.542779394*lambda,Name "Parameters/dout"];
cos45   = DefineNumber[0.707106781, Name "Parameters/cos"];

// Pontos quadrado interno
Point(1) = {-dinner, dinner, 0, 1.0};
//+
Point(2) = {dinner, dinner, 0, 1.0};
//+
Point(3) = {dinner, -dinner, 0, 1.0};
//+
Point(4) = {-dinner, -dinner, 0, 1.0};

// Pontos quadrado externo
Point(5) = {-dout*cos45,  dout*cos45, 0, 1.0};
//+
Point(6) = {dout*cos45,   dout*cos45, 0, 1.0};
//+
Point(7) = {dout*cos45,   -dout*cos45, 0, 1.0};
//+
Point(8) = {-dout*cos45,  -dout*cos45, 0, 1.0};

// Centro arco de circunferência
Point(9) = {0, 0, 0, 1.0};


//Linhas quadrado interno
Line(1) = {3, 4};
//+
Line(2) = {4, 1};
//+
Line(3) = {1, 2};
//+
Line(4) = {2, 3};

// Linhas quadrado externo
Line(5) = {3, 7};
//+
Line(6) = {4, 8};
//+
Line(7) = {1, 5};
//+
Line(8) = {2, 6};


// Circunferência
Circle(9) = {5, 9, 6};
//+
Circle(10) = {6, 9, 7};
//+
Circle(11) = {7, 9, 8};
//+
Circle(12) = {8, 9, 5};


// Definição das superfícies
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {3, 8, -9, -7};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {4, 5, -10, -8};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {11, -6, -1, 5};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {12, -7, -2, 6};
//+
Plane Surface(5) = {5};
//+
Recombine Surface {2, 3, 4, 5, 1};

// Definindo malha
a = 100;
c = a;
b = 1.05*a;

    // quadrado
Transfinite Curve {1, 2, 3, 4}  = a Using Progression 1;
    
    //1º quarto de círculo
Transfinite Curve {9, 8, 3, 7}  = c Using Progression 1;
    
    //2º quarto de círculo
Transfinite Curve {10, 5, 4, 8} = c Using Progression 1;

    //3º quarto de círculo
Transfinite Curve {1, 5, 11, 6} = c Using Progression 1;

    //4º quarto de círculo
Transfinite Curve {2, 6, 12, 7} = c Using Progression 1;

    //diagonais
Transfinite Curve {7, 8, 5, 6}  = b Using Progression 1.03;
//+

//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {1};


// Extrusão da malha no eixo Z
Extrude {0, 0, 1} {
  Surface{4}; Surface{3}; Surface{1}; Surface{5}; Surface{2}; Layers {1}; Recombine;
}
// Definindo superfícies de contorno
Physical Surface("outer", 33) = {18, 21, 6, 12};
//+
//+
Physical Surface("frontAndBack", 34) = {17, 1, 5, 20, 2, 22, 3, 14, 4, 10};
//+
Physical Volume("internal", 35) = {5, 2, 3, 1, 4};

Mesh 3;