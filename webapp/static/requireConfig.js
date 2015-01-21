requirejs.config({
    baseUrl : 'static',
    paths : {
        jquery : 'lib/jquery-2.1.1',
        lodash : 'lib/lodash-2.4.1',
        bootstrap : 'lib/bootstrap',
        Chart : 'lib/Chart',
        webSocket : 'src/webSocket'
    }
});

var pathname = window.location.pathname;
if (pathname.indexOf('/webSoc') !== -1)
    requirejs(['webSocket']);
else {
    alert('shit');
}