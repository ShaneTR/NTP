clear
clc

% file = fopen('C:\Users\10815945\Downloads\ntpq-cleaned.csv');
file = fopen('C:\Users\Brian\Documents\MATLAB\ntpq-cleaned.csv');

data = textscan(file, '%s%s%d%s%s%d%d%f%f%f','delimiter',',');

colors={'r' 'm' 'c' 'b' 'g' 'k' 'r'};

[rows dummy] = size(data{1});

% There are 7 servers so we divide the number of rows in the sample to
% obtain the number of half hour steps.
steps = rows/7;

x = linspace(0,steps/2,steps);

grid on
hold on

% Iterate over the servers
for i=1:7
% For displaying individual servers
%     if i ~= 2
%         continue;
%     end
    servers(i).name = data{1}(i);
    
    legendInfo(i) = servers(i).name; 
    
    servers(i).offsets = zeros(1,24);
    
    % Iterate over the half hour intervals
    for j=1:steps
        row = i + ((j-1)*7);
        
        % Offset information is in the data array in 'column' 9
        servers(i).offsets(j) = data{9}(row);
    end
    
    plot(x, servers(i).offsets, colors{i});
end

title('NTP Analysis (Server Offset)','FontWeight','bold');
xlabel('Time (Hours)');
ylabel('Offset (Seconds)');
legend(legendInfo);
hold off