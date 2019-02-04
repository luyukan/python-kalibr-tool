clc;
clear all;
close all;
txt_name = '/home/yukan/Documents/kalibr-cde/results-cam-homeyukanDocumentspy_kalibr_tooltest.txt';
fid = fopen(txt_name);

for i = 1:28
    tline = fgetl(fid);
end

Transform = [];

%% baseline 0-1
tline = fgetl(fid);
C_q = cell2table(strsplit(tline, ' '));
% tline = fgetl(fid);
% C_t = strsplit(tline, ' ');
Transform = [Transform;C_q.Var3(2:end), C_q.Var4, C_q.Var5, C_q.Var6(1:end-1)];
