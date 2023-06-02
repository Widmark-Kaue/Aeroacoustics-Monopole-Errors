// Gmsh project created on Wed Nov  3 22:16:15 2021
SetFactory("OpenCASCADE");
//Parametros
d=DefineNumber[0.05715,Name "Parameters/d"];
//+
cos=DefineNumber[0.70710678,Name "Parameters/cos"];
//+
dr=DefineNumber[3.40,Name "Parameters/dr"];//diametro zona de refino - - 1 comprimento de onda
//+
d2=DefineNumber[204,Name "Parameters/d2"];//204   1
//+
db=DefineNumber[408,Name "Parameters/db"];//408   1.2

// Centro do cilindro 1
Point(1) = {0, 0, 0, 1.0};

// Pontos que definem o cilindro 1
Point(2) = {cos*d/2, cos*d/2, 0, 1.0};
Point(3) = {-cos*d/2, cos*d/2, 0, 1.0};
Point(4) = {-cos*d/2, -cos*d/2, 0, 1.0};
Point(5) = {cos*d/2, -cos*d/2, 0, 1.0};

// Pontos que definem os limites da zona util
Point(6) = {cos*d2/2, cos*d2/2, 0, 1.0};
Point(7) = {-cos*d2/2, cos*d2/2, 0, 1.0};
Point(8) = {-cos*d2/2, -cos*d2/2, 0, 1.0};
Point(9) = {cos*d2/2, -cos*d2/2, 0, 1.0};

// Pontos que definem os limites da zona buffer
Point(10) = {cos*db/2, cos*db/2, 0, 1.0};
Point(11) = {-cos*db/2, cos*db/2, 0, 1.0};
Point(12) = {-cos*db/2, -cos*db/2, 0, 1.0};
Point(13) = {cos*db/2, -cos*db/2, 0, 1.0};

// Pontos que definem os limites da zona de refino
Point(14) = {cos*dr/2, cos*dr/2, 0, 1.0};
Point(15) = {-cos*dr/2, cos*dr/2, 0, 1.0};
Point(16) = {-cos*dr/2, -cos*dr/2, 0, 1.0};
Point(17) = {cos*dr/2, -cos*dr/2, 0, 1.0};
//+
Circle(1) = {4, 1, 5};
//+
Circle(2) = {5, 1, 2};
//+
Circle(3) = {2, 1, 3};
//+
Circle(4) = {3, 1, 4};
//+
Circle(5) = {8, 1, 9};
//+
Circle(6) = {9, 1, 6};
//+
Circle(7) = {6, 1, 7};
//+
Circle(8) = {7, 1, 8};
//+
Circle(13) = {11, 1, 12};
//+
Circle(14) = {12, 1, 13};
//+
Circle(15) = {13, 1, 10};
//+
Circle(16) = {10, 1, 11};
//+
Line(17) = {6, 10};
//+
Line(18) = {9, 13};
//+
Line(19) = {8, 12};
//+
Line(20) = {7, 11};
//+
Circle(21) = {16, 1, 15};
//+
Circle(22) = {15, 1, 14};
//+
Circle(23) = {14, 1, 17};
//+
Circle(24) = {17, 1, 16};
//+
// Linhas para zona de refino
Line(25) = {3, 15};
//+
Line(26) = {2, 14};
//+
Line(27) = {5, 17};
//+
Line(28) = {4, 16};
//Linhas para zona útil

//+
Line(29) = {15, 7};
//+
Line(30) = {14, 6};
//+
Line(31) = {17, 9};
//+
Line(32) = {16, 8};
//+
Curve Loop(1) = {16, -20, -7, 17};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {17, -15, -18, 6};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {18, -14, -19, 5};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {19, -13, -20, 8};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {7, -29, 22, 30};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {30, -6, -31, -23};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {31, -5, -32, -24};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {32, -8, -29, -21};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {22, -26, 3, 25};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {26, 23, -27, 2};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {1, 27, 24, -28};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {25, -21, -28, -4};
//+
Plane Surface(12) = {12};
//+
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 12, 9, 10, 11};
//+
Transfinite Curve {16, 7, 22, 15, 6, 23, 14, 5, 24, 2, 3, 4, 1, 21, 8, 13} = 18 Using Progression 1;
//+
Transfinite Curve {29, 30, 31, 32} = 480 Using Progression 1;
//+
Transfinite Curve {20, 17, 18, 19} = 41 Using Progression 1.1;
//+
Transfinite Curve {26, 25, 28, 27} = 16 Using Progression 1.09; // zona de refino
//+
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
//+
Transfinite Surface {10};
//+
Transfinite Surface {11};
//+
Transfinite Surface {12};
//+
Extrude {0, 0, 1} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4}; Surface{8}; Surface{5}; Surface{6}; Surface{7}; Surface{12}; Surface{9}; Surface{10}; Surface{11}; Layers{1}; Recombine;
}
//+
Physical Surface("inlet") = {26};
//+
Physical Surface("outlet") = {18};
//+
Physical Surface("free") = {13, 22};
//+
Physical Surface("frontAndBack") = {17, 28, 25, 21, 40, 32, 44, 47, 50, 52, 38, 35, 2, 1, 4, 8, 12, 9, 10, 11, 3, 5, 7, 6};
//+
Physical Surface("cyl") = {46, 43, 51, 49};
//+
Physical Volume("Cylinders") = {1, 6, 10, 12, 11, 7, 2, 8, 3, 9, 5, 4};
