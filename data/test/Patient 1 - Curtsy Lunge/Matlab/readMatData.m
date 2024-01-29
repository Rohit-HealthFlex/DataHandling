% Column 1 (Equipment):1 is WT901BLE68(d7:f5:e1:06:da:71)(d7:f5:e1:06:da:71)   2 is WT901BLE68(fc:66:87:ee:fb:8c)(fc:66:87:ee:fb:8c)   
% Column 2:Chip Time   The interval (in seconds) between each piece of data and the start time, with the start time as the starting point
% Column 3:Acceleration X(g)
% Column 4:Acceleration Y(g)
% Column 5:Acceleration Z(g)
% Column 6:Angular velocity X(°/s)
% Column 7:Angular velocity Y(°/s)
% Column 8:Angular velocity Z(°/s)
% Column 9:Angle X(°)
% Column 10:Angle Y(°)
% Column 11:Angle Z(°)
% Column 12:Magnetic field X(ʯt)
% Column 13:Magnetic field Y(ʯt)
% Column 14:Magnetic field Z(ʯt)
% Column 15:Temperature(℃)
% Column 16:Quaternions 0
% Column 17:Quaternions 1
% Column 18:Quaternions 2
% Column 19:Quaternions 3
% 函数调用：a=readMatData;
function d = readMatData(file)

    if nargin<1
        disp('默认数据')
        file='data.mat';
    else
        disp(file);
    end

    disp('加载mat文件')
    data = matfile(file);
    varlist = who(data);
    len = size(varlist,1);
    
    if len > 0
        disp('开始合并矩阵')
        mcol = size(data.(varlist{1}),2);
        mrow = size(data.(varlist{1}),1);
        fprintf('行数%d 列数%d\r\n',len,mcol);
        d=zeros((len-1)*mrow,mcol);
        %h=waitbar(0,'数据合并中……');
        for i = 1: len-1
            d(mrow*(i-1)+1:mrow*(i-1)+mrow,:) = [data.(varlist{i})];   
            m=len-1;
%             p=fix(i/(m)*10000)/100; %这样做是可以让进度条的%位数为2位
%             str=['正在合并，目前进度为 ',num2str(p),' %，完成 ',num2str(i),'/',num2str(m)];%进度条上显示的内容
%             waitbar(i/m,h,str);
            %pause(1)
        end
        d = [d;data.(varlist{len})];
        disp('加载矩阵完成')
    else
        disp('mat文件为空')
        d = [];
    end
end