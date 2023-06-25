SetFactory("OpenCASCADE");

// Parâmetros de controle
lambda      = DefineNumber[34.653698762, Name "Parâmetros Gerais/lambda"];
rinner      = DefineNumber[lambda,       Name "Parâmetros Gerais/rinner"];
rmiddle1    = DefineNumber[100,           Name "Parâmetros Gerais/rmiddle1"];
rmiddle2    = DefineNumber[200,          Name "Parâmetros Gerais/rmiddle2"];
rout        = DefineNumber[400,          Name "Parâmetros Gerais/rout"];
cos45       = DefineNumber[0.707106781,  Name "Parâmetros Gerais/cos"];

// Parâmetros livres
rI          = DefineNumber[rinner/lambda,   Name "Parâmetros normalizados por lambda/rinner"];
rM1         = DefineNumber[rmiddle1/lambda, Name "Parâmetros normalizados por lambda/rmiddle1"];
rM2         = DefineNumber[rmiddle2/lambda, Name "Parâmetros normalizados por lambda/rmiddle2"];
rO          = DefineNumber[rout/lambda,     Name "Parâmetros normalizados por lambda/rout"];


// Centro arco de circunferência
Point(0) = {0, 0, 0, 1.0};

// Pontos quadrado interno
Point(1) = {-rinner, rinner, 0, 1.0};
//+
Point(2) = {rinner, rinner, 0, 1.0};
//+
Point(3) = {rinner, -rinner, 0, 1.0};
//+
Point(4) = {-rinner, -rinner, 0, 1.0};

// Pontos quadrado médio 1
Point(5) = {-rmiddle1*cos45,  rmiddle1*cos45, 0, 1.0};
//+
Point(6) = {rmiddle1*cos45,   rmiddle1*cos45, 0, 1.0};
//+
Point(7) = {rmiddle1*cos45,   -rmiddle1*cos45, 0, 1.0};
//+
Point(8) = {-rmiddle1*cos45,  -rmiddle1*cos45, 0, 1.0};

// Pontos quadrado médio 2
Point(9) = {-rmiddle2*cos45,  rmiddle2*cos45, 0, 1.0};
//+
Point(10) = {rmiddle2*cos45,   rmiddle2*cos45, 0, 1.0};
//+
Point(11) = {rmiddle2*cos45,   -rmiddle2*cos45, 0, 1.0};
//+
Point(12) = {-rmiddle2*cos45,  -rmiddle2*cos45, 0, 1.0};

// Pontos quadrado externo
Point(13) = {-rout*cos45,  rout*cos45, 0, 1.0};
//+
Point(14) = {rout*cos45,   rout*cos45, 0, 1.0};
//+
Point(15) = {rout*cos45,   -rout*cos45, 0, 1.0};
//+
Point(16) = {-rout*cos45,  -rout*cos45, 0, 1.0};

//Linhas quadrado interno
Line(1) = {3, 4};
//+
Line(2) = {4, 1};
//+
Line(3) = {1, 2};
//+
Line(4) = {2, 3};

// Linhas diagonais quadrado médio 1
Line(5) = {3, 7};
//+
Line(6) = {4, 8};
//+
Line(7) = {1, 5};
//+
Line(8) = {2, 6};

// Linhas diagonais quadrado médio 2
Line(25) = {5, 9};
//+
Line(26) = {6, 10};
//+
Line(27) = {7, 11};
//+
Line(28) = {8, 12};

// Linhas diagonais quadrado externo
Line(9)  = {11, 15};
//+
Line(10) = {12, 16};
//+
Line(11) = {9, 13};
//+
Line(12) = {10, 14};


/*

// Circunferência middle 
Circle(13) = {8, 13, 5};
//+
Circle(14) = {5, 13, 6};
//+
Circle(15) = {6, 13, 7};
//+
Circle(16) = {7, 13, 8};

// Circunferência out
Circle(17) = {12, 13, 9};
//+
Circle(18) = {9, 13, 10};
//+
Circle(19) = {10, 13, 11};
//+
Circle(20) = {11, 13, 12};

// Definindo superfícies
//+
Curve Loop(1) = {2, 3, 4, 1};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {6, 13, -7, -2};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {7, 14, -8, -3};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {8, 15, -5, -4};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {5, 16, -6, -1};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {10, 17, -11, -13};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {11, 18, -12, -14};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {12, 19, -9, -15};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {9, 20, -10, -16};
//+
Plane Surface(9) = {9};
//+
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9};

// Definindo malha
a = 60;
c1 = 60;
c2 = a;
b1 = 1.5*a;50
b2 = 1.5*a;

    // quadrado
Transfinite Curve {2, 3, 4, 1}      = a Using Progression   1;
    // 1º quarto de círculo (middle)
Transfinite Curve {6, 13, 7, 2}     = c1 Using Progression  1;

    // 2º quarto de círculo (middle)
Transfinite Curve {7, 14, 8, 3}     = c1 Using Progression  1;

    // 3º quarto de círculo (middle)
Transfinite Curve {8, 15, 5, 4}     = c1 Using Progression  1;

    // 4º quarto de círculo (middle)
Transfinite Curve {5, 16, 6, 1}     = c1 Using Progression  1;



    // 1º quarto de cículo (out)
Transfinite Curve {10, 17, 11, 13}  = c2 Using Progression  1;

    // 2º quarto de cículo (out)
Transfinite Curve {11, 18, 12, 14}  = c2 Using Progression  1;

    // 3º quarto de cículo (out)
Transfinite Curve {12, 19, 9, 15}   = c2 Using Progression  1;

    // 4º quarto de cículo (out)
Transfinite Curve {9, 20, 10, 16}   = c2 Using Progression  1;


    // diagonais internas
Transfinite Curve {7, 8, 5, 6}      = b1 Using Progression  1;
    // diagonais externas
Transfinite Curve {11, 12, 9, 10} = b2 Using Progression 1;
    // diagonais externas
Transfinite Curve {11, 12, 9, 10}   = b2 Using Progression  1;

Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {6};
//+
Transfinite Surface {7};
//+
Transfinite Surface {8};
//+
Transfinite Surface {9};

Mesh 2;

/*
Circle(9) = {5, 9, 6};
//+
Circle(10) = {6, 9, 7};
//+
Circle(11) = {7, 9, 8};
//+
Circle(12) = {8, 9, 5};


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

Mesh 3;*///+

//+

//+

// Círculo médio 1
Circle(13) = {8, 0, 5};
//+
Circle(14) = {5, 0, 6};
//+
Circle(15) = {6, 0, 7};
//+
Circle(16) = {7, 0, 8};


// Círculo médio 2
Circle(17) = {12, 0, 9};
//+
Circle(18) = {9, 0, 10};
//+
Circle(19) = {10, 0, 11};
//+
Circle(20) = {11, 0, 12};

// Círculo externo
Circle(21) = {16, 0, 13};
//+
Circle(22) = {13, 0, 14};
//+
Circle(23) = {14, 0, 15};
//+
Circle(24) = {15, 0, 16};


// Definindo superfícies
Curve Loop(1) = {2, 3, 4, 1};
// +
Plane Surface(1) = {1};
//+
Curve Loop(2) = {14, -8, -3, 7};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {8, 15, -5, -4};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {5, 16, -6, -1};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {6, 13, -7, -2};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {18, 19, 20, 17};
//+
Curve Loop(7) = {13, 14, 15, 16};
//+
Plane Surface(6) = {6, 7};
//+
Curve Loop(8) = {10, 21, -11, -17};
//+
Plane Surface(7) = {8};
//+
Curve Loop(9) = {11, 22, -12, -18};
//+
Plane Surface(8) = {9};
//+
Curve Loop(10) = {12, 23, -9, -19};
//+
Plane Surface(9) = {10};
//+
Curve Loop(11) = {9, 24, -10, -20};
//+
Plane Surface(10) = {11};
//+
Recombine Surface {1, 5, 2, 3, 4, 6, 8, 9, 10, 7};

// Definindo malha
a = 10;
c2 = a;
b1 = 1.8*a;
b2 = a;

    // quadrado


