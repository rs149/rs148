window.addEventListener('load', () => {
    var frame = document.getElementById('frame');
    var count = 0;
    var id = setInterval(function(){
        /*
        count++;
        if(count > 5){　
          clearInterval(id);　//idをclearIntervalで指定している
        }
        */
        var text = '';
        var x = 0;
        var y = 0;
        var width = 25;
        for (y = 0; y < width; y++)
        {
            for (x = 0; x < width; x++)
            {
                var r = Math.floor(Math.random()*256).toString(16);
                var g = Math.floor(Math.random()*256).toString(16);
                var b = Math.floor(Math.random()*256).toString(16);
                var color = '#' + r + g + b;
                //text += '<font color=' + color + '>■</font>';
                text += '<span style="background-color:' + color + ';"> 　 </span>';
            }
            text += '<br>';
        }
        frame.innerHTML = text;
    }, 100);
});
