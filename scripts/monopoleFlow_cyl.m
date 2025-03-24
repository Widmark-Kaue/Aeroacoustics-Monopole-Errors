%clear all
close all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% TCC - SOLU��O ANAL�TICA PARA MONOPOLO ESTACION�RIO:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% DADOS UTILIZADOS NA SIMULA��O

%c_0=1;           % velocidade do som para fechar lambda=30
freq=100;         % frequ�ncia da onda 
P_sim=10;         % amplitude da press�o definida na simula��o
t = 0.17;         % instante de tempo dos resultados

% C�LCULO DA TEMPERATURA DA SIMULA��O
c_0=340.29;       % velocidade do som utilizada no c�lculo do comprimento de onda
c = 331.45;       % velocidade do som a 0 �C
T0 = 273.15;      % 0 �C em Kelvin
T = (c_0/c)^2*T0; % temperatura da simula��o 
%omega=pi()/15;   % Disserta��o
%A=23.206;        % Constante para fonte pontual - definir a partir da aplica��o de condi��o de contorno
%A=1;

% C�LCULO DA DENSIDADE
rho0 = 101325/(287.058*T); % equa��o dos gases ideais

% C�LCULO DO TEMPO DE SIMULA��O 
r_buffer = 204;                 % raio externo da zona de buffer
t_simulacao = (r_buffer+6)/c_0; % +6 para passar o primeiro pulso e fechar 210

%% SOLU��O ANAL�TICA
%freq=omega/(2*pi());
omega=freq*2*pi;
lambda=c_0/freq;
r=.0001:0.1:100;

%solu��o analitica da disserta��o
epsilon=1;
alpha=log(2)/(9);
f=epsilon*exp(-alpha*r.^2);


H_0=besselh(0, (omega*r/c_0));      %Fun��o de Hankel
G_t=(-1i*omega)*(1i/(4*c_0^2))*H_0; %transformada de fourier da derivada dG/dt

%convolu��o via FFT espacial
%f_k=fft(f);
%G_k=fft(G_t);
%P=ifft(f_k.*G_k);

P=conv(f,G_t); %convolu��o

%% C�LCULO DA CONSTANTE "A" PELA CONDI��O DE CONTORNO

r_fonte = 0.05715/2;
H_0_fonte=besselh(0, (omega*r_fonte/c_0));      %Fun��o de Hankel
G_t_fonte=(-1i*omega)*(1i/(4*c_0^2))*H_0_fonte; %transformada de fourier da derivada dG/dt

A = abs(P_sim/G_t_fonte);
P_2=A*G_t;                                     %Amplitude considerando fonte pontual

p_2=-1*imag(P_2*exp(-1i*omega*t));              %calculado com fonte pontual

%% SOLU��O ANAL�TICA - BUCKINGHAM

H_0_B=besselh(0, 2, (omega*r/c_0));                  %Fun��o de Hankel
% UTILIZANDO PAR�METRO DE PRESS�O (COMENTAR A SOLU��O DA VELOCIDADE PARA
% CALCULAR)

H_0_fonte_B=besselh(0, 2, (omega*r_fonte/c_0));      %Fun��o de Hankel
A_B = abs(P_sim/H_0_fonte_B);
P_2_B=A_B*H_0_B;
p_2_B = imag(P_2_B*exp(1i*omega*t)); %calculado com fonte pontual

% UTILIZANDO PAR�METRO DE VELOCIDADE
S = 0.1;                              % Vaz�o volum�trica definida na simula��o por unidade de espessura do dom�nio
P_2_B = -rho0*omega*S*H_0_B/4;
p_2_B = imag(P_2_B*exp(1i*omega*t)); %calculado com fonte pontual / solu��o invertida

%% SOLU��O ANAL�TICA - JACOBSEN

Area = 2*pi*r_fonte;
Velocity = S/Area;
H_1_fonte_J=besselh(1, 2, (omega*r_fonte/c_0));

A0 = Velocity*1i*rho0*c_0/H_1_fonte_J;

H_0_J=besselh(0, 2, (omega*r/c_0));                  %Fun��o de Hankel
P_2_J = A0*H_0_J;
p_2_J = imag(P_2_J*exp(1i*omega*t)); %calculado com fonte pontual

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% MONOPOLO COM ESCOAMENTO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% SOLU��O ANAL�TICA
M = 0.3;
y = 0;
x = -100:0.13:100;
k = omega/c_0; % n�mero de onda
Gx = zeros(1,length(x)); 
Gt_escoamento = zeros(1,length(x));

ksi = omega*sqrt(x.^2+(1-M^2)*y^2)/((1-M^2)*c_0);
eta = -1i*M/(1-M^2)*k*x-1i*omega*t;
H_0_escoamento = besselh(0, ksi);
H_1_escoamento = besselh(1, ksi);

% DERIVADA DA FUN��O GREEN EM X
for i=1:length(x)
Gx(i) = omega/(4*c_0^3*(1-M^2)^(3/2))*(M*H_0_escoamento(i)-1i*x(i)*H_1_escoamento(i)/sqrt(x(i)^2+(1-M^2)*y^2))*exp(eta(i));
end

% DERIVADA DA FUN��O GREEN EM t
for i=1:length(x)
Gt_escoamento(i) = eta(i)*1i/(4*c_0^2*sqrt(1-M^2))*H_0_escoamento(i)*exp(eta(i))*(-1i*omega);
end

p_flow=-imag(rho0*(c_0^2)*S*(Gt_escoamento+M*Gx));

%% RESULTADOS - MONOPOLO COM ESCOAMENTO

figure(2)
hold on
%plot(r,p_2(1:length(r)), 'r-')                          % Anal�tico Akhnoukh com fonte pontual
plot(r,p_2_J(1:length(r)), 'k-')                        % Anal�tico Jacobsen com fonte pontual
plot(x,p_flow, 'g-')                                  % Anal�tico Akhnoukh com escoamento
% plot(Simulation(:,8), (Simulation(:,5))-101325, 'r-')   % Simula��o
hold off
 xlabel('x (m)')
ylabel('p (Pa)')
legend('Jacobsen', 'Aknoukh')