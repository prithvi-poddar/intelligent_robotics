[x,y] = meshgrid(1:1:51,1:1:51);
so = 10;
ro = 10;
sg = 10;
rg = 1;
uo=x;
vo=y;
ug = x;
vg = y;
xg = 47;
yg = 47;
xo = 26;
yo = 26;


for i=1:length(x)
    for j=1:length(y)
        theta = atan2(y(i,j)-yo,x(i,j)-xo);
        distance = sqrt(((x(i,j)-xo)*(x(i,j)-xo))+((y(i,j)-yo)*(y(i,j)-yo)));
        if (distance<so+ro && distance>ro)
            uo(i,j)=7*(so+ro-distance)*cos(theta);
            vo(i,j)=7*(so+ro-distance)*sin(theta);
        elseif(distance<ro)
            uo(i,j)=sign(cos(theta))*100;
            vo(i,j)=sign(sin(theta))*100;
        else
            uo(i,j)=0;
            vo(i,j)=0;
        end
        theta = atan2(y(i,j)-yg,x(i,j)-xg);
        distance = sqrt(((x(i,j)-xg)*(x(i,j)-xg))+((y(i,j)-yg)*(y(i,j)-yg)));
        if (distance<rg)
            ug(i,j)=0;
            vg(i,j)=0;
        elseif(distance>=rg && distance<=sg+rg)
            ug(i,j) = (-2)*(distance-rg)*cos(theta);
            vg(i,j) = (-2)*(distance-rg)*sin(theta);
        elseif(sqrt(((x(i,j)-xo)*(x(i,j)-xo))+((y(i,j)-yo)*(y(i,j)-yo)))<ro)
            ug(i,j)=0;
            vg(i,j)=0;
        else
            ug(i,j) = (-2)*sg*cos(theta);
            vg(i,j) = (-2)*sg*sin(theta);
        end
    end
end

quiver(x,y,uo+ug,vo+vg);


