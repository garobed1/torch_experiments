close all
clear all

db = [0 0.0 0.75];
dg = [0 0.5 0];
dr = [0.75 0.0 0];

% bad piv range (based on old figures from TO)
iToss = 30;

% shift based on where the take "zero" in the experiment
yShift = 0.138201*1000;

% set line of data to pull from piv, not all will work as some are in the neck-region with no data
yLine = 32.1;

% PIV data
dataBS = load('fullFlowfield/BelowStep.mat');
dataBN = load('fullFlowfield/BelowNozzle.mat');
dataAS = load('fullFlowfield/AboveStep.mat');
dataAI = load('fullFlowfield/AboveInlet.mat');

% goes from -111.1765 to ~140 
unc = load('Uncertainty/Uncertainty.mat');

yAI = dataAI.AboveInlet.y;
yAS = dataAS.AboveStep.y;
yBN = dataBN.BelowNozzle.y;
yBS = dataBS.BelowStep.y;

xAI = dataAI.AboveInlet.x;
xAS = dataAS.AboveStep.x;
xBN = dataBN.BelowNozzle.x;
xBS = dataBS.BelowStep.x;

uUnc = (unc.U.zero.vx + unc.U.p60.vx + unc.U.m60.vx)/3.0;
vUnc = (unc.U.zero.vy + unc.U.p60.vy + unc.U.m60.vy)/3.0;
wUnc = (unc.U.zero.vz + unc.U.p60.vz + unc.U.m60.vz)/3.0;
xUnc = unc.U.x;
yUnc = unc.U.y + yShift;

uAI = (dataAI.AboveInlet.zerodeg.vx + dataAI.AboveInlet.p60deg.vx + dataAI.AboveInlet.m60deg.vx)/3.0;
uAS = (dataAS.AboveStep.zerodeg.vx + dataAS.AboveStep.p60deg.vx + dataAS.AboveStep.m60deg.vx)/3.0;
uBN = (dataBN.BelowNozzle.zerodeg.vx + dataBN.BelowNozzle.p60deg.vx + dataBN.BelowNozzle.m60deg.vx)/3.0;
uBS = (dataBS.BelowStep.zerodeg.vx + dataBS.BelowStep.p60deg.vx + dataBS.BelowStep.m60deg.vx)/3.0;

vAI = (dataAI.AboveInlet.zerodeg.vy + dataAI.AboveInlet.p60deg.vy + dataAI.AboveInlet.m60deg.vy)/3.0;
vAS = (dataAS.AboveStep.zerodeg.vy + dataAS.AboveStep.p60deg.vy + dataAS.AboveStep.m60deg.vy)/3.0;
vBN = (dataBN.BelowNozzle.zerodeg.vy + dataBN.BelowNozzle.p60deg.vy + dataBN.BelowNozzle.m60deg.vy)/3.0;
vBS = (dataBS.BelowStep.zerodeg.vy + dataBS.BelowStep.p60deg.vy + dataBS.BelowStep.m60deg.vy)/3.0;

wAI = (dataAI.AboveInlet.zerodeg.vz + dataAI.AboveInlet.p60deg.vz + dataAI.AboveInlet.m60deg.vz)/3.0;
wAS = (dataAS.AboveStep.zerodeg.vz + dataAS.AboveStep.p60deg.vz + dataAS.AboveStep.m60deg.vz)/3.0;
wBN = (dataBN.BelowNozzle.zerodeg.vz + dataBN.BelowNozzle.p60deg.vz + dataBN.BelowNozzle.m60deg.vz)/3.0;
wBS = (dataBS.BelowStep.zerodeg.vz + dataBS.BelowStep.p60deg.vz + dataBS.BelowStep.m60deg.vz)/3.0;

yAI = yAI + yShift;
yAS = yAS + yShift;
yBN = yBN + yShift;
yBS = yBS + yShift;

if yLine >= min(yBN)
    data = dataBN;
    u = uAI;
    v = vAI;
    w = wAI;
    y = yBN;
    x = xBN;
elseif yLine >= min(yAS)
    data = dataAS;
    u = uAS;
    v = vAS;
    w = wAS;
    y = yAS;
    x = xAS;
elseif yLine >= min(yBS)
    data = dataBS;
    u = uBS;
    v = vBS;
    w = wBS;
    y = yBS;
    x = xBS;
else
    data = dataAI;
    u = uAI;
    v = vAI;
    w = wAI;
    y = yAI;
    x = xAI;
end

iLineTemp = find (y>=yLine);
iLine = iLineTemp(1);
wt =  (yLine - y(iLine-1)) / (y(iLine) - y(iLine-1));
Udat = wt*u(:,iLine-1) + (1-wt)*u(:,iLine);
Vdat = wt*v(:,iLine-1) + (1-wt)*v(:,iLine);
Wdat = wt*w(:,iLine-1) + (1-wt)*w(:,iLine);

iLineTemp2 = find (yUnc>=yLine);
iLine2 = iLineTemp2(1);
wt =  (yLine - yUnc(iLine2-1)) / (yUnc(iLine2) - yUnc(iLine2-1));
Uerr = wt*uUnc(:,iLine2-1) + (1-wt)*uUnc(:,iLine2);
Verr = wt*vUnc(:,iLine2-1) + (1-wt)*vUnc(:,iLine2);
Werr = wt*wUnc(:,iLine2-1) + (1-wt)*wUnc(:,iLine2);

UerrDat = Udat;
VerrDat = Vdat;
WerrDat = Wdat;
for i = 2:length(x)-1
    xx = x(i);
    jjTemp = find(xUnc>=xx);
    jj = 0;
    if length(jjTemp) > 0
        jj = jjTemp(1);
    end
    if jj >= 2 
       wt =  (xx - xUnc(jj-1)) / (xUnc(jj) - xUnc(jj-1));
       UerrDat(i) = wt*Uerr(jj-1) + (1-wt)*Uerr(jj);
       VerrDat(i) = wt*Verr(jj-1) + (1-wt)*Verr(jj);
       WerrDat(i) = wt*Werr(jj-1) + (1-wt)*Werr(jj);
    end
end

rad = 28.062;
for i = 1:length(x)
  if x(i) < -rad || x(i) > rad
      Udat(i) = 0;
      Vdat(i) = 0;
      Wdat(i) = 0;
  end
end

rad = 27.5;
for i = 1:length(x)
  if x(i) < -rad || x(i) > rad
      UerrDat(i) = 0;
      VerrDat(i) = 0;
      WerrDat(i) = 0;
  end
  if UerrDat(i) ~= UerrDat(i)
    UerrDat(i) = 0.0;
  end
  if VerrDat(i) ~= VerrDat(i)
    VerrDat(i) = 0.0;
  end
  if WerrDat(i) ~= WerrDat(i)
    WerrDat(i) = 0.0;
  end
end

vLo = Vdat - VerrDat;
vHi = Vdat + VerrDat;
wLo = Wdat - WerrDat;
wHi = Wdat + WerrDat;
xT = transpose(x);


% plots....................
% f1: axial vel
% f2: swirl vel

figure(1)
plot(x(1+iToss:end-iToss),Vdat(1+iToss:end-iToss),'-','LineWidth',2);
ep = patch([xT(1+iToss:end-iToss); xT(end-iToss:-1:1+iToss); xT(1+iToss)], [vLo(1+iToss:end-iToss); vHi(end-iToss:-1:1+iToss); vLo(1+iToss)], 'b');
set(ep, 'facecolor', [0.6 0.8 1.0], 'edgecolor', 'none','FaceAlpha',0.5);
gcl=legend('PIV');
legend boxoff;
fontsize(16,"points")
ylim([-4 6]);
xlabel('$r(mm)$','fontsize',14,'interpreter','latex');
ylabel('$U_{axial}(m/s)$','fontsize',14,'interpreter','latex');
set(gcl,'Interpreter','latex','Location','northeast')
set(gca,'TickLabelInterpreter','latex')
set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,'PaperPosition',[0 0 screenposition(3:4)],'PaperSize',[screenposition(3:4)]);
print -dpdf -vector uAxial_piv.pdf

figure(2)
plot(x(1+iToss:end-iToss),Wdat(1+iToss:end-iToss),'LineWidth',2);
ep = patch([xT(1+iToss:end-iToss); xT(end-iToss:-1:1+iToss); xT(1+iToss)], [wLo(1+iToss:end-iToss); wHi(end-iToss:-1:1+iToss); wLo(1+iToss)], 'b');
set(ep, 'facecolor', [0.6 0.8 1.0], 'edgecolor', 'none','FaceAlpha',0.5);
gcl=legend('PIV');
legend boxoff;
fontsize(16,"points")
ylim([-25 25]);
xlabel('$r(mm)$','fontsize',14,'interpreter','latex');
ylabel('$U_{swirl}(m/s)$','fontsize',14,'interpreter','latex');
set(gcl,'Interpreter','latex','Location','southwest')
set(gca,'TickLabelInterpreter','latex')
set(gcf,'Units','inches');
screenposition = get(gcf,'Position');
set(gcf,'PaperPosition',[0 0 screenposition(3:4)],'PaperSize',[screenposition(3:4)]);
print -dpdf -vector uAzimuthal_piv.pdf



