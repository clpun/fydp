function varargout = stats_gui(varargin)
% STATS_GUI MATLAB code for stats_gui.fig
%      STATS_GUI, by itself, creates a new STATS_GUI or raises the existing
%      singleton*.
%
%      H = STATS_GUI returns the handle to a new STATS_GUI or the handle to
%      the existing singleton*.
%
%      STATS_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in STATS_GUI.M with the given input arguments.
%
%      STATS_GUI('Property','Value',...) creates a new STATS_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before stats_gui_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to stats_gui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help stats_gui

% Last Modified by GUIDE v2.5 15-Mar-2015 19:43:04

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @stats_gui_OpeningFcn, ...
                   'gui_OutputFcn',  @stats_gui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before stats_gui is made visible.
function stats_gui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to stats_gui (see VARARGIN)

% Choose default command line output for stats_gui
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);


% UIWAIT makes stats_gui wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = stats_gui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in import_data_pushbutton.
function import_data_pushbutton_Callback(hObject, eventdata, handles)
% hObject    handle to import_data_pushbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global channel;
    channel = {'F3','FC5','AF3','F7','T7','P7','O1','O2',...
                 'P8','T8','F8','AF4','FC6','F4'};
    [header filename data_3D] = import_multiple_csv_files();
    [m,n,p] = size(data_3D);
    [a_mean b_mean c_mean] = Process3Darray(data_3D);
    [anova tukey] = anova_tukey(a_mean, b_mean, c_mean, p);
    %t_value_2D = Process3Darray(data_3D);
    %t_value_2D = [t_value_2D;1./var(t_value_2D)];
    %t_value_2D = [header(2:end);num2cell(t_value_2D)];
    %write_to_csv('t_values.csv',t_value_2D.');
    write_to_csv('p_values_tukey.csv',tukey);
    msgbox('Results written to p_values_tukey.csv');

function [header, FileName, array3D] = import_multiple_csv_files()
    [FileName, PathName] = uigetfile('*.csv','Select csv files','MultiSelect', 'on');
    filename_strings = char(FileName);
    
%     filename = strtrim(filename_strings(1,:));
%     T = readtable(filename,'Delimiter',',');
%     tmpArray = [T.Properties.VariableNames;table2cell(T)];
%     array3D = tmpArray;
    
    for x = 1:length(FileName)
        filename = strtrim(filename_strings(x,:));
        T = readtable(filename,'Delimiter',',');
        %tmpArray = [T.Properties.VariableNames;table2cell(T)];
        header_tmp = strrep(T.Properties.VariableNames,'z_','z)');
        header = strrep(header_tmp,'_','(');
        tmpArray = T{:,:};
        array3D(:,:,x) = tmpArray;
    end

% parameters a and b are matrices
function t_values = Calc_t_values (a, b)
    size_a = size(a);
	size_b = size(b);
    t_values = zeros(1,size_a(2));
	expectation_a = mean(a);
	expectation_b = mean(b);
	variance_a = var(a);
	variance_b = var(b);
	t_values = (expectation_a - expectation_b)./(((variance_a./size_a(1))+(variance_b./size_b(1))).^(0.5));

function [pass_anova, pass_tukey] = anova_tukey(a_mean, b_mean, c_mean, num_test)
    global channel;
    pass_anova = [];
    pass_tukey = [];
    for ch=0:13
        for freq=1:64
            for test=1:num_test
                c(test) = a_mean(test,ch*64+freq);
                f(test) = b_mean(test,ch*64+freq);
                m(test) = c_mean(test,ch*64+freq);
            end
            table = [c;f;m]';
            [p tbl stats] = anova1(table,[],'off');
            if p <= 0.05
                pass_anova = [pass_anova;[channel(ch+1) freq]];
                C = multcompare(stats,'Display','off');
                for x=1:3
                    if C(x,6) <= 0.05
                       pass_tukey = [pass_tukey; [channel(ch+1) freq C(x,1:2)]];
                    end
                end
            end
        end
    end
        
function [a_mean, b_mean, c_mean] = Process3Darray(data_3D)
    % data from import_data
    % t_value returned from Calc_t_value(a,b) is an array
    % return 2D array of t_values from diff test cases
    [m,n,p] = size(data_3D);
    %t_value_2D = [];
    %for z=1:p %each testcase
        for row=2:m
            if data_3D(row,1,1) >= 5.0
                row_exp = row;
                break;
            end
        end
        for row=row_exp:m
            if data_3D(row,1,1) >= 7.8
                row_maintainance = row;
                break;
            end
        end
        a = data_3D(1:row_exp-1,2:end,:);
        b = data_3D(row_exp:row_maintainance-1,2:end,:);
        c = data_3D(row_maintainance:end,2:end,:);
        for x=1:p % each test case
            a_mean(x,:) = mean(a(:,:,x));
            b_mean(x,:) = mean(b(:,:,x));
            c_mean(x,:) = mean(c(:,:,x));
        end
        %t_value = Calc_t_values(a,b);
        %t_value_2D = [t_value_2D;t_value];
    %end

function write_to_csv(filename,array)
    %csvwrite('p_values_tukey.csv',array);
    %xlswrite('t_values.csv',array);
    %write line by line
    filehandle = fopen(filename,'wt');
    fprintf(filehandle, 'channel,freq,C1,C2\n');
    for x=1:size(array,1)
        fprintf(filehandle, '%s,%d,%d,%d\n', array{x,:});
    end
    fclose(filehandle);

function test_func(data_3D)
    [m,n,p] = size(data_3D);
    mat = zeros(m,n);
    for row=2:m
        for col=2:n
            mat(row,col) = data_3D(row,col,:);
        end
    end
