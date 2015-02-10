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

% Last Modified by GUIDE v2.5 08-Feb-2015 23:15:23

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


% --- Executes on button press in import_data_button.
function import_data_button_Callback(hObject, eventdata, handles)
% hObject    handle to import_data_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[FileName,PathName] = uigetfile('*.csv','Select the CSV file');
%M = csvread(FileName)
global T;
T = readtable(FileName,'Delimiter',',');


% --- Executes on button press in create_graph_button.
function create_graph_button_Callback(hObject, eventdata, handles)
% hObject    handle to create_graph_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global T;
% Check if csv data is imported
if ~istable(T)
    h = warndlg('No data imported!');
else
    f = figure('ToolBar','figure','OuterPosition',[230 250 1000 670]);
    ah = axes('Parent',f,'Tag','axes','Position', [.15 .25 .7 .7]);
    ph = uipanel('Parent',f,'Title','Add Data','Position',[.15 .06 .7 .12]);
    pm1h = uicontrol('Parent',ph,'Style','popupmenu',...
                    'String',{'AF3','F7','F3','FC5','T7','P7','O1','O2',...
                    'P8','T8','FC6','F4','F8','AF4'},...
                    'Callback',@channel_popupmenu_Callback,...
                    'Tag','channel_menu',...
                    'Value',1,'Position',[130 20 130 20]);
    pm2h = uicontrol('Parent',ph,'Style','popupmenu',...
                    'String',{'delta','theta','alpha','beta','gamma'},...
                    'Callback',@band_popupmenu_Callback,...
                    'Tag','band_menu',...
                    'Value',1,'Position',[300 20 130 20]);
    pb1h = uicontrol('Parent',ph,'Style','pushbutton','String','Add',...
                    'Callback',@add_button_Callback,...
                    'Position',[500 10 60 40]);
    pb2h = uicontrol('Parent',ph,'Style','pushbutton','String','Clear',...
                    'Callback',@clear_button_Callback,...
                    'Position',[590 10 60 40]);
end
            
% --- Executes on button press in add_button.
function add_button_Callback(hObject, eventdata, handles)
global T;
myhandles = guihandles(hObject);
mydata = guidata(hObject);
channel_array = get(myhandles.channel_menu, 'String');
channel_index = get(myhandles.channel_menu, 'Value');
channel = channel_array{channel_index};
band_array = get(myhandles.band_menu, 'String');
band_index = get(myhandles.band_menu, 'Value');
band = band_array{band_index};
variable = strcat(channel,'_',band,'_');
grid on;
hold on;
if isfield(mydata,'legend')
    if isempty(strfind(mydata.legend,strcat(channel,'(',band,')')))
        plot(T.time, T{:, {variable}}, 'Color', rand([1,3]))
        mydata.legend = strcat(mydata.legend,',',channel,'(',band,')');
        legend(strsplit(mydata.legend,','));
    end
else
    plot(T.time, T{:, {variable}}, 'Color', rand([1,3]))
    mydata.legend = strcat(channel,'(',band,')');
    legend(strsplit(mydata.legend,','));
end

% if isfield(mydata,'legend')
%     tmp = mydata.legend;
%     mydata.legend = strcat(tmp,',',channel,'(',band,')');
% else
%     mydata.legend = strcat(channel,'(',band,')');
% end
guidata(hObject, mydata);


function clear_button_Callback(hObject, eventdata, handles)
myhandles = guihandles(hObject);
cla(myhandles.axes);
legend('off');
mydata = guidata(hObject);
mydata = rmfield(mydata,'legend');
%mydata.legend = '';
guidata(hObject, mydata);


function channel_popupmenu_Callback(hObject, eventdata, handles)
% myhandles = guidata(hObject);
% items = get(hObject,'String');
% index_selected = get(hObject,'Value');
% item_selected = items{index_selected};
% myhandles.channel = item_selected;
% guidata(hObject, myhandles);

function band_popupmenu_Callback(hObject, eventdata, handles)
% myhandles = guidata(hObject);
% items = get(hObject,'String');
% index_selected = get(hObject,'Value');
% item_selected = items{index_selected};
% myhandles.band = item_selected;
% guidata(hObject, myhandles);
