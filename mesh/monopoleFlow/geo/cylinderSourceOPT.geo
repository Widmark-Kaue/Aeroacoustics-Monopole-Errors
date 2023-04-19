//+
SetFactory("OpenCASCADE");
//+
Geometry.OldNewReg=0;
//+
rOuter= DefineNumber[ 400.0, Name "Parameters/rOuter" ];
//+
rMiddle=DefineNumber[ 200, Name "Parameters/rMiddle" ];
//+
rInner= DefineNumber[ 100, Name "Parameters/rInner" ];
//+
rPoints= DefineNumber[ 50, Name "Parameters/rPoints" ];
//+
cPoints= DefineNumber[ 100, Name "Parameters/cPoints" ];
//+
rRatio= DefineNumber[ 1.02, Name "Parameters/rRatio" ];
//+
lc=1.0;
//+
depth=1.0;
//+
p1=newp; Point(p1) = {0, 0, 0, lc};
//+
p2=newp; Point(p2) = {-rInner, 0, 0, lc};
//+
p3=newp; Point(p3) = {rInner, 0, 0, lc};
//+
p4=newp; Point(p4) = { 0, rInner, 0, lc};
//+
p5=newp; Point(p5) = { 0, -rInner, 0, lc};
//+
c1=newc; Circle(c1) = {0, 0, 0, rOuter};
//+
c2=newc; Circle(c2) = {p2, p1, p4};
//+
c3=newc; Circle(c3) = {p4, p1, p3};
//+
c4=newc; Circle(c4) = {p3, p1, p5};
//+
c5=newc; Circle(c5) = {p5, p1, p2};
//+
p6=newp; Point(p6) = {-rMiddle, 0, 0, lc};
//+
p7=newp; Point(p7) = {rMiddle, 0, 0, lc};
//+
p8=newp; Point(p8) = { 0, rMiddle, 0, lc};
//+
p9=newp; Point(p9) = { 0, -rMiddle, 0, lc};
//+
c6=newc; Circle(c6) = {p6, p1, p8};
//+
c7=newc; Circle(c7) = {p8, p1, p7};
//+
c8=newc; Circle(c8) = {p7, p1, p9};
//+
c9=newc; Circle(c9) = {p9, p1, p6};
//+
c10=newc; Curve(c10) = {p2, p6};
//+
c11=newc; Curve(c11) = {p8, p4};
//+
c12=newc; Curve(c12) = {p7, p3};
//+
c13=newc; Curve(c13) = {p5, p9};
//+
l1=newll; Curve Loop(l1) = {c6, c11, -c2, c10};
//+
l2=newll; Curve Loop(l2) = {-c11, c7, c12, -c3};
//+
l3=newll; Curve Loop(l3) = {-c12, c8, -c13, -c4};
//+
l4=newll; Curve Loop(l4) = {c13, c9, -c10, c5};
//+
l5=newll; Curve Loop(l5) = {c6, c7, c8, c9};
//+
l6=newll; Curve Loop(l6) = {c1};
//+
l7=newll; Curve Loop(l7) = {c2, c3, c4, c5};
//+
Transfinite Curve {c2} = cPoints;
//+
Transfinite Curve {c3} = cPoints;
//+
Transfinite Curve {c4} = cPoints;
//+
Transfinite Curve {c5} = cPoints;
//+
Transfinite Curve {c6} = cPoints;
//+
Transfinite Curve {c7} = cPoints;
//+
Transfinite Curve {c8} = cPoints;
//+
Transfinite Curve {c9} = cPoints;
//+
Transfinite Curve {c10} = rPoints Using Progression rRatio;
//+
Transfinite Curve {c11} = rPoints Using Progression 1/rRatio;
//+
Transfinite Curve {c12} = rPoints Using Progression 1/rRatio;
//+
Transfinite Curve {c13} = rPoints Using Progression rRatio;
//+
s1=news; Plane Surface(s1) = {l6, l5};
//+
s2=news; Plane Surface(s2) = {l1};
//+
Transfinite Surface {s2};
//+
Recombine Surface{s2};
//+
s3=news; Plane Surface(s3) = {l2};
//+
Transfinite Surface {s3};
//+
Recombine Surface{s3};
//+
s4=news; Plane Surface(s4) = {l3};
//+
Transfinite Surface {s4};
//+
Recombine Surface{s4};
//+
s5=news; Plane Surface(s5) = {l4};
//+
Transfinite Surface {s5};
//+
Recombine Surface{s5};
//+
s6=news; Plane Surface(s6) = {l7};
//+
out[]=Extrude {0, 0, depth} {
      Surface{s1, s2, s3, s4, s5, s6}; Layers {1}; Recombine;
};
//out2[]=Extrude {0, 0, depth} {
//      Surface{s6}; Layers {1}; Recombine;
//};
//+
Physical Surface("frontAndBack", 1) = {s1, s2, s3, s4, s5, s6, 12, 16, 19, 22, 24, 25}; 
//+
Physical Surface("outer", 2) = {7};
//+
//Physical Surface("cylinder", 3) = {4};
//+
Physical Volume("internal") = {1, 2, 3, 4, 5, 6};
//+
//Physical Volume("source") = {6};
//+
Field[1] = Distance;
Field[1].SurfacesList = {8, 11, 10, 9};//{14, 17, 20, 23};
Field[1].NumPointsPerCurve = 100;
//+
Field[2] = Threshold;
Field[2].InField=1;
Field[2].SizeMin = 5*lc;
Field[2].SizeMax = 10*lc;
Field[2].DistMin = 0;
Field[2].DistMax = rOuter;
Field[2].Sigmoid = 1;
//+
Field[3] = Constant;
Field[3].VolumesList = {1};
Field[3].VIn = {lc/30};
//+
Field[4] = Min;
Field[4].FieldsList = {2, 3};
//+
Background Field = 4;
//+
Mesh.MeshSizeExtendFromBoundary = 1;
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.OptimizeThreshold=0.8;
Mesh.Smoothing=10;
