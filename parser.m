%-------------------------------------------------------------------------%
% EULER MATRIX TESTING ---------------------------------------------------%
%--- Variable definition%
pos = [31 0 0];
% eul = [heading pitch roll]; % Euler angles vector. Z->Y->X


while 1
mssg = judp('receive',5005,120,10000); char(mssg');
array = strsplit(char(mssg')); 
heading = str2double(array(2));
roll = str2double(array(3));
pitch = str2double(array(4));

%Euler -> Rotation Matrix, using Z->Y->X rotation.
%===============================================================
p = degtorad(pitch);
r = degtorad(roll);
h = -degtorad(heading);
cp = cos(p);
cr = cos(r);
ch = cos(h);
sp = sin(p);
sr = sin(r);
sh = sin(h);


EulRot = [ cp*ch sr*sp*ch+cr*sh -cr*sp*ch+sr*sh
           -cp*sh -sr*sp*sh+cr*ch cr*sp*sh+sr*ch
           sp -sr*cp cr*cp ];
       
% Alternative Definition %
ZROT = [ch sh 0
        -sh ch 0
        0 0 1];
    
YROT = [cp 0 -sp
        0 1 0
        sp 0 cp];
    
XROT = [1 0 0
        0 cr sr
        0 -sr cr];
    
EURLROT = ZROT*YROT*XROT;
%==============================================================

          
answer = pos * EulRot;
answer2 = pos*ZROT*YROT*XROT;
%==============================================================

% eul = [Heading Roll Pitch];
% rotmZYX = (eul2rotm(eul));
% 
% data=[heading,roll,pitch];
% scatter3(heading,roll,pitch);
% grid on
% drawnow
% disp(data)

%---Plotting---%
z = answer;
% line([0,0,0],[z(1),z(2),z(3)]);
plot3([0,z(1)],[0,z(2)],[0,z(3)]);
% plot([0,0,0],[z(1),z(2),z(3)]);
axis([-50 50 -50 50 -50 50]);

xlabel('X');
ylabel('Y');
zlabel('Z','rotation' ,-90);
grid on
drawnow
display (answer)
display (answer2)

end


