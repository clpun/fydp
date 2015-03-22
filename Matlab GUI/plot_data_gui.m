function varargout = plot_data_gui(varargin)
% PLOT_DATA_GUI MATLAB code for plot_data_gui.fig
%      PLOT_DATA_GUI, by itself, creates a new PLOT_DATA_GUI or raises the existing
%      singleton*.
%
%      H = PLOT_DATA_GUI returns the handle to a new PLOT_DATA_GUI or the handle to
%      the existing singleton*.
%
%      PLOT_DATA_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in PLOT_DATA_GUI.M with the given input arguments.
%
%      PLOT_DATA_GUI('Property','Value',...) creates a new PLOT_DATA_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before plot_data_gui_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to plot_data_gui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help plot_data_gui

% Last Modified by GUIDE v2.5 11-Mar-2015 22:58:27

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @plot_data_gui_OpeningFcn, ...
                   'gui_OutputFcn',  @plot_data_gui_OutputFcn, ...
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


% --- Executes just before plot_data_gui is made visible.
function plot_data_gui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to plot_data_gui (see VARARGIN)

% Choose default command line output for plot_data_gui
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes plot_data_gui wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = plot_data_gui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% ----------
%  Main GUI
% ----------

% --- Executes on mouse press over figure background.
function figure1_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% --- Executes on button press in import_data_button.
function import_data_button_Callback(hObject, eventdata, handles)
% hObject    handle to import_data_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
format long;
[FileName,PathName] = uigetfile('*.csv','Select the CSV file');
global T;
global channel_names;
T = readtable(FileName,'Delimiter',',');
channel_names = {'F3','FC5','AF3','F7','T7','P7','O1','O2',...
                 'P8','T8','F8','AF4','FC6','F4'};


% --- Executes on button press in create_mag_time_graph_button.
function create_mag_time_graph_button_Callback(hObject, eventdata, handles)
% hObject    handle to create_mag_time_graph_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global T;
global channel_names;
% Check if csv data is imported
if ~istable(T)
    h = warndlg('No data imported!');
else
    f = figure('ToolBar','figure','OuterPosition',[230 250 1000 670]);
    ah = axes('Parent',f,'Tag','axes','Position', [.15 .25 .7 .7]);
    ph = uipanel('Parent',f,'Title','Add Data','Position',[.15 .06 .7 .12]);
    pm1h = uicontrol('Parent',ph,'Style','popupmenu',...
                    'String',channel_names,...
                    'Callback',@mt_channel_popupmenu_Callback,...
                    'Tag','mt_channel_menu',...
                    'Value',1,'Position',[100 20 130 20]);
%     pm2h = uicontrol('Parent',ph,'Style','popupmenu',...
%                     'String',{'delta','theta','alpha','beta','gamma'},...
%                     'Callback',@mt_band_popupmenu_Callback,...
%                     'Tag','mt_band_menu',...
%                     'Value',1,'Position',[250 20 130 20]);
    freq_bin = {};
    for i = 1:63
       freq_bin = [freq_bin, strcat(num2str(i-1),'Hz')];
    end
    pm2h = uicontrol('Parent',ph,'Style','popupmenu',...
                    'String',freq_bin,...
                    'Callback',@mt_freq_popupmenu_Callback,...
                    'Tag','mt_freq_menu',...
                    'Value',1,'Position',[250 20 130 20]);
    pb1h = uicontrol('Parent',ph,'Style','pushbutton','String','Add',...
                    'Callback',@mt_add_button_Callback,...
                    'Position',[400 10 60 40]);
    pb2h = uicontrol('Parent',ph,'Style','pushbutton','String','Clear',...
                    'Callback',@mt_clear_button_Callback,...
                    'Position',[490 10 60 40]);
    pb3h = uicontrol('Parent',ph,'Style','pushbutton',...
                    'String','Moving Average',...
                    'Callback',@mt_ma_button_Callback,...
                    'Position',[580 10 100 40]);
    grid on;
    hold on;
    title('Magnitude-time plot');
    xlabel('time(s)');
    ylabel('magnitude');
    %axis([T.time(1), ceil(T.time(end)), 0, ceil(max(max(T{:,:})))]);
end

% --- Executes on button press in create_time_freq_graph_button.
function create_time_freq_graph_button_Callback(hObject, eventdata, handles)
% hObject    handle to create_time_freq_graph_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global T;
global channel_names;
% Check if csv data is imported
if ~istable(T)
    h = warndlg('No data imported!');
else
    f = figure('ToolBar','figure','OuterPosition',[230 250 1000 670]);
    ah = axes('Parent',f,'Tag','axes','Position', [.15 .25 .7 .7]);
    ph = uipanel('Parent',f,'Title','Plot Data','Position',[.15 .06 .7 .12]);
    pm1h = uicontrol('Parent',ph,'Style','popupmenu',...
                    'String',channel_names,...
                    'Tag','tf_channel_menu',...
                    'Callback',@tf_channel_menu_Callback,...
                    'Value',1,'Position',[100 20 130 20]);
    c1h = uicontrol('Parent',ph,'Style','checkbox',...
                'String','2D','Tag','tf_2d_cbox',...
                'Callback',@tf_2d_cbox_Callback,...
                'Value',0,'Position',[300 20 130 20]);
    c2h = uicontrol('Parent',ph,'Style','checkbox',...
                'String','Grayscale','Tag','tf_gray_cbox',...
                'Callback',@tf_gray_cbox_Callback,...
                'Value',0,'Position',[400 20 130 20]);
end

% --- Executes on button press in view_fft_button.
function view_fft_button_Callback(hObject, eventdata, handles)
% hObject    handle to view_fft_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global T;
global channel_names;
% Check if csv data is imported
if ~istable(T)
    h = warndlg('No data imported!');
else
    f = figure('ToolBar','figure','OuterPosition',[230 250 1000 670]);
    ah = axes('Parent',f,'Tag','axes','Position', [.15 .25 .7 .7]);
    ph = uipanel('Parent',f,'Title','Menu','Position',[.15 .06 .7 .12]);
    pm1h = uicontrol('Parent',ph,'Style','popupmenu',...
                    'String',channel_names,...
                    'Callback',@fft_channel_menu_Callback,...
                    'Tag','fft_channel_menu',...
                    'Value',1,'Position',[150 10 130 20]);
    num_row = length(T.time);
    step = 1/(num_row-1);
    sh = uicontrol('Parent',ph,'Style','slider',...
                    'Min',T.time(1),'Max',T.time(end),'Value',T.time(1),...
                    'SliderStep',[step step*5],...
                    'Callback',@fft_slider_Callback,...
                    'Tag','fft_slider',...
                    'Position',[350 10 150 20]);
    t1h = uicontrol('Parent',ph,'Style','text',...
                    'String','Current channel: F3',...
                    'Tag','fft_channel_text',...
                    'Position',[150 36 130 17]);
    t2h = uicontrol('Parent',ph,'Style','text',...
                    'String',['Current time: ',num2str(T.time(1)),'s'],...
                    'Tag','fft_time_text',...
                    'Position',[350 36 150 17]);
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
    title('Fast Fourier Transform');
end

% ----------------------
%  Magnitude-time graph
% ----------------------
% --- Executes on button press in add_button.
function mt_add_button_Callback(hObject, eventdata, handles)
global T;
global channel_names;
myhandles = guihandles(hObject);
mydata = guidata(hObject);
%channel_array = get(myhandles.mt_channel_menu, 'String');
channel_index = get(myhandles.mt_channel_menu, 'Value');
%channel = channel_array{channel_index};
channel = channel_names{channel_index};
%band_array = get(myhandles.mt_band_menu, 'String');
%band_index = get(myhandles.mt_band_menu, 'Value');
freq_array = get(myhandles.mt_freq_menu, 'String');
freq_index = get(myhandles.mt_freq_menu, 'Value');
%band = band_array{band_index};
freq = freq_array{freq_index};
%variable = strcat(channel,'_',band,'_');
variable = strcat(channel,'_',freq,'_');
if isfield(mydata,'legend')
    %if isempty(strfind(mydata.legend,strcat(channel,'(',band,')')))
    if isempty(strfind(mydata.legend,strcat(channel,'(',freq,')')))
        plot(T.time, T{:, {variable}}, 'Color', rand([1,3]));
        %mydata.legend = strcat(mydata.legend,',',channel,'(',band,')');
        mydata.legend = strcat(mydata.legend,',',channel,'(',freq,')');
        legend(strsplit(mydata.legend,','));
    end
else
    plot(T.time, T{:, {variable}}, 'Color', rand([1,3]));
    %mydata.legend = strcat(channel,'(',band,')');
    mydata.legend = strcat(channel,'(',freq,')');
    legend(strsplit(mydata.legend,','));
end
guidata(hObject, mydata);


function mt_clear_button_Callback(hObject, eventdata, handles)
myhandles = guihandles(hObject);
cla(myhandles.axes);
legend('off');
mydata = guidata(hObject);
mydata = rmfield(mydata,'legend');
guidata(hObject, mydata);

function mt_ma_button_Callback(hObject, eventdata, handles)
global T;
myhandles = guihandles(hObject);
mydata = guidata(hObject);
%cla(myhandles.axes);
strlegend = ''
for entry = strsplit(mydata.legend,',')
    data = strsplit(strjoin(entry),'(');
    channel = strjoin(data(1));
    band = strjoin(data(2));
    variable = strcat(channel,'_',band(1:end-1),'_');
    if isempty(strlegend)
        strlegend = strcat(channel,'(',band(1:end-1),')',' MA window=20');
    else
        strlegend = strcat(strlegend,',',channel,'(',band(1:end-1),')',' MA window=20');
    end
    ma = moving_average(T{:, {variable}},20);
	plot(T.time, ma, 'Color', rand([1,3]));
end
orig_legend = strsplit(mydata.legend,',')
strlegend = strsplit(strlegend,',')
new_legend = [orig_legend,strlegend];
legend([orig_legend,strlegend]);


function ma = moving_average(y,window)
%window = 5;
mask = ones(1,window)/window;
ma = conv(y,mask,'same');

function mt_channel_popupmenu_Callback(hObject, eventdata, handles)

function mt_freq_popupmenu_Callback(hObject, eventdata, handles)

% ----------------------
%  Time-frequency graph
% ----------------------

function tf_channel_menu_Callback(hObject, eventdata, handles)
global T;
global channel_names;
myhandles = guihandles(hObject);
channel_index = get(myhandles.tf_channel_menu, 'Value');
channel = channel_names{channel_index};
dim_2 = get(myhandles.tf_2d_cbox, 'Value');
grayscale = get(myhandles.tf_gray_cbox, 'Value');
%create cell array of channel
column = {};
for i = 1:63
    column = [column, strcat(channel,'_',num2str(i-1),'Hz_')];
end
X = T.time;
Y = zeros(1,63);
for i = 1:63
    Y(1,i) = i-1;
end
Z = zeros(length(Y),length(X));
for i = 1:63
    Z(i,:) = T{:,column(i)}.';
end
surf(X,Y,Z,'EdgeColor','None','facecolor','interp');
title(strcat('Time-frequency plot of ',channel));
xlabel('time(s)');
ylabel('freq(Hz)');
zlabel('mag');

if dim_2 == 1
	view(2);
end
if grayscale == 1
	colormap(gray); 
end

function tf_2d_cbox_Callback(hObject, eventdata, handles)
myhandles = guihandles(hObject);
dim_2 = get(myhandles.tf_2d_cbox, 'Value');
if dim_2 == 1
    view(2);
else
    view(3);
end

function tf_gray_cbox_Callback(hObject, eventdata, handles)
myhandles = guihandles(hObject);
grayscale = get(myhandles.tf_gray_cbox, 'Value');
if grayscale == 1
    colormap(gray);
else
    colormap(jet);
end

% ---------------------------
%  FFT graph
% ---------------------------

function fft_channel_menu_Callback(hObject, eventdata, handles)
global T;
global channel_names;
myhandles = guihandles(hObject);
channel_index = get(myhandles.fft_channel_menu, 'Value');
channel = channel_names{channel_index};
cur_time = get(myhandles.fft_slider, 'Value');
set(myhandles.fft_channel_text,'String',['Current channel: ',channel]);
ch_offset = (channel_index-1)*64;
%step = (T.time(end)-T.time(1))/(length(T.time)-1);
step = 0.203125;
if T.time(1) == 0
    row_index = cur_time/step + 1;
else
    row_index = cur_time/step;
end
x = 0:1:63;
y = T{round(row_index),ch_offset+2:ch_offset+65};
plot(x,y);
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Fast Fourier Transform');
legend([channel,' at t=',num2str(cur_time),'s']);

function fft_slider_Callback(hObject, eventdata, handles)
global T;
global channel_names;
myhandles = guihandles(hObject);
channel_index = get(myhandles.fft_channel_menu, 'Value');
channel = channel_names{channel_index};
cur_time = get(myhandles.fft_slider, 'Value');
set(myhandles.fft_time_text,'String',['Current time: ',num2str(cur_time)]);
ch_offset = (channel_index-1)*64;
%step = (T.time(end)-T.time(1))/(length(T.time)-1);
step = 0.203125;
if T.time(1) == 0
    row_index = cur_time/step + 1;
else
    row_index = cur_time/step;
end
x = 0:1:63;
y = T{round(row_index),ch_offset+2:ch_offset+65};
plot(x,y);
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Fast Fourier Transform');
legend([channel,' at t=',num2str(cur_time),'s']);
%axis([0, 70, 0, ceil(max(max(T{:,:})))]);

