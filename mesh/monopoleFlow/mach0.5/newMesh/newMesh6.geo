SetFactory("OpenCASCADE");

// Parâmetros
lambda_min  = DefineNumber[17,  Name "Parameters/lambda min"];
//lambda_min  = DefineNumber[52,          Name "Parameters/lambda min"];
lambda_dp   = DefineNumber[52,          Name "Parameters/lambda doppler"];
rinner      = DefineNumber[2*lambda_dp, Name "Parameters/rinner"];
rmiddle     = DefineNumber[4.5*lambda_dp,         Name "Parameters/rmiddle"];
rout        = DefineNumber[10*lambda_dp,         Name "Parameters/rout"];
cos45       = DefineNumber[0.707106781, Name "Parameters/cos"];

// Definindo malha
ppw         = DefineNumber[8,                          Name "Mesh/ppw"];
a         	= DefineNumber[30,                          Name "Mesh/a"];
b         	= DefineNumber[(rmiddle-rinner)/lambda_min *ppw,                         Name "Mesh/b"];
c           = DefineNumber[2*rinner/lambda_min *ppw,                          Name "Mesh/c"];
d1         	= DefineNumber[c,                           Name "Mesh/d1"];
d2         	= DefineNumber[60,                          Name "Mesh/d2"];
aprog       = DefineNumber[1,                           Name "Mesh/aprog"];
bprog       = DefineNumber[1.02,                           Name "Mesh/bprog"];
cprog       = DefineNumber[1,                           Name "Mesh/cprog"];
d1prog      = DefineNumber[1,                       Name "Mesh/d1prog"];
d2prog      = DefineNumber[1.01,                       Name "Mesh/d2prog"];

// Pontos quadrado interno
Point(1) = {-rinner, rinner, 0, 1.0};
//+
Point(2) = {rinner, rinner, 0, 1.0};
//+
Point(3) = {rinner, -rinner, 0, 1.0};
//+
Point(4) = {-rinner, -rinner, 0, 1.0};

// Pontos quadrado médio
Point(5) = {-rmiddle,  rmiddle, 0, 1.0};
//+
Point(6) = {rmiddle,   rmiddle, 0, 1.0};
//+
Point(7) = {rmiddle,   -rmiddle, 0, 1.0};
//+
Point(8) = {-rmiddle,  -rmiddle, 0, 1.0};

// Pontos quadrado externo
Point(9) = {-rout,  rout, 0, 1.0};
//+
Point(10) = {rout,   rout, 0, 1.0};
//+
Point(11) = {rout,   -rout, 0, 1.0};
//+
Point(12) = {-rout,  -rout, 0, 1.0};

// Centro arco de circunferência
Point(13) = {0, 0, 0, 1.0};


//Linhas quadrado interno
Line(1) = {3, 4};
//+
Line(2) = {4, 1};
//+
Line(3) = {1, 2};
//+
Line(4) = {2, 3};

// Linhas quadrado médio
Line(5) = {3, 7};
//+
Line(6) = {4, 8};
//+
Line(7) = {1, 5};
//+
Line(8) = {2, 6};

// Linhas quadrado externo
Line(9) = {7, 11};
//+
Line(10) = {8, 12};
//+
Line(11) = {5, 9};
//+
Line(12) = {6, 10};


// Circunferência média
Circle(13) = {5, 13, 6};
//+
Circle(14) = {6, 13, 7};
//+
Circle(15) = {7, 13, 8};
//+
Circle(16) = {8, 13, 5};

// Circunferência externa
Circle(17) = {9, 13, 10};
//+
Circle(18) = {10, 13, 11};
//+
Circle(19) = {11, 13, 12};
//+
Circle(20) = {12, 13, 9};

// Definição das superfícies
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {3, 8, -13, -7};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {8, 14, -5, -4};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {5, 15, -6, -1};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {2, 7, -16, -6};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {13, 12, -17, -11};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {14, 9, -18, -12};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {9, 19, -10, -15};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {10, 20, -11, -16};
//+
Plane Surface(9) = {9};
//+

// quadrado
Transfinite Curve {1, 2, 3, 4} = a Using Progression aprog;
// 1/4's do círculo médio
Transfinite Curve {3, 7, 13, 8, 4, 14, 5, 15, 6, 1, 16, 2} = c Using Progression cprog;
// diagonais internas
Transfinite Curve {7, 8, 5, 6} = b Using Progression bprog;
// 1/4's do círculo externo
Transfinite Curve {15, 9, 19, 10, 20, 11, 16, 17, 13, 18, 12, 14} = d1 Using Progression d1prog;
// diagonais externas
Transfinite Curve {11, 12, 9, 10} = d2 Using Progression d2prog;

//+
Transfinite Surface {1};
//+
Transfinite Surface {5};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {9};
//+
Transfinite Surface {6};
//+
Transfinite Surface {7};
//+
Transfinite Surface {8};
//+
Recombine Surface {1, 5, 2, 3, 4, 9, 6, 7, 8};


// //+
// Extrude {0, 0, 1} {
//   Surface{1}; Surface{5}; Surface{2}; Surface{3}; Surface{4}; Surface{9}; Surface{6}; Surface{7}; Surface{8}; 
// }
// //+
// Physical Surface("frontAndBack", 53) = {14, 18, 5, 1, 21, 2, 24, 3, 26, 4, 30, 9, 33, 6, 36, 7, 38, 8};
// //+
// Physical Surface("outer", 54) = {28, 32, 35, 37};
// //+
// Physical Volume("internal", 55) = {1, 2, 5, 3, 4, 9, 6, 7, 8};

// Mesh 3;//+
//+
//+
//+


Extrude {0, 0, 1} {
  Surface{6}; Surface{2}; Surface{1}; Surface{4}; Surface{5}; Surface{9}; Surface{7}; Surface{3}; Surface{8}; Layers{1}; Recombine;
}
//+
Physical Surface("frontAndBack") = {22, 1, 28, 5, 18, 2, 36, 3, 26, 4, 31, 9, 38, 8, 35, 7, 14, 6};
//+
Physical Surface("outer") = {30, 37, 34, 12};
//+
Physical Volume("internal") = {3, 5, 2, 8, 4, 6, 1, 7, 9};
//+
Mesh 3;