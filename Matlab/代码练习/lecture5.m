% cell(1,2)
c={'hello world',[1 5 6 2],rand(3,2)};
% c{1,1}='Hi';
%%
size(c(2))
size(c{2})
c{2}(2)
%%
s = struct;
s.name = 'Hailey';
s.year = 20;
% or struct('name',{'Hailey'},'year',20)
%%
% create a matrix y, with two rows
x = 0:0.1:1;
y = [x; exp(x)];
% open a file for writing
fid = fopen('exp.txt', 'w');
% print a title, followed by a blank line
fprintf(fid, 'Exponential Function\n\n');
% print values in column order
% two values appear on each row of the file
fprintf(fid, '%f %f\n', y);
fclose(fid);
%%
a = importdata('exp.txt',' ');
%%
values = {1, 2, 3 ; 4, 5, 'x'; 7, 8, 9};
headers = {'First','Second','Third'};
xlswrite('exp.xlsx',[headers; values]);
A = rand(5);
xlswrite('myExample.xlsx',A,'MyData');
num = xlsread('myExample.xlsx','MyData','B2');
% [num,txt,raw]=xlsread(бнбн.. )
% Reads data
% Num contains numbers,
% Txt contains strings,
% Raw is the entire cell array containing everything
%%
name = 'Zara Ali ';
position = 'Sr. Surgeon ';
worksAt = 'R N Tagore Cardiology Research Center';
profile = char(name, position, worksAt);
profile = cellstr(profile);
disp(profile)
%%
str = 'Find the starting indices of a pattern in a character vector';
strfind(str,'in')
strrep(str,'in','!')
strcmp('a','b')
%%