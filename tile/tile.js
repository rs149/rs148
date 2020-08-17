window.addEventListener('load', () => {
    var frame = document.getElementById('frame');

    var text = '';
    var x = 0;
    var y = 0;
    var width = 10;
    for (y = 0; y < width; y++)
    {
        for (x = 0; x < width; x++)
        {
            var r = Math.floor(Math.random()*256).toString(16);
            var g = Math.floor(Math.random()*256).toString(16);
            var b = Math.floor(Math.random()*256).toString(16);
            var color = '"#' + r + g + b + '"';
            text += '<font color=' + color + '>■</font>';
        }
        text += '<br>';
    }
    frame.innerHTML = text;
});
